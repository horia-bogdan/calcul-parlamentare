import csv
import math
import sys

NATIONAL_THRESHOLD = 0.05
CONSTITUENCY_THRESHOLD = 0.2

DISPLAY_LEVEL = 1

constituency_votes_total = 0

def read_mandates(mandates_filename):
    mandates = []
    constituency_names = []
    with open(mandates_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            constituency_names.append(row[0])
            mandates.append(int(row[1]))
    return mandates, constituency_names
    
def read_votes(filename):
    votes = []
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            for entry in list(row):
                row[entry] = int(row[entry])
            votes.append(row)

    return votes

#votes - list of dicts               
def party_cull(votes):
    total = {}    
    initial_parties = list(votes[0])
    independents = find_independents(votes)
    total_votes = 0    
    over_constituency_threshold = {}
    
    for party in initial_parties:
        total[party] = 0
        over_constituency_threshold[party] = 0
    
    for constituency in votes:
        constituency_votes = 0
        for party in initial_parties:
            total[party] += constituency[party]
            constituency_votes += constituency[party]
        for party in initial_parties:
            if constituency[party] / constituency_votes >= CONSTITUENCY_THRESHOLD:
                over_constituency_threshold[party]+=1
        total_votes += constituency_votes
            
    remaining_parties = []

    print("Totalul voturilor exprimate a fost de " + str(total_votes))    
    for party in initial_parties:
        if party in independents:
            continue
        print("Voturi " + party + ": " + str(total[party]))
        if total[party] / total_votes >= NATIONAL_THRESHOLD:
            remaining_parties.append(party)
            print("Partidul " + party + " a trecut pragul electoral national")
            
        elif over_constituency_threshold[party] >= 4:
            remaining_parties.append(party)
            print("Partidul " + party + " a trecut pragul de circumscriptie in 4 circumscriptii")
        else:
            print ("Partidul " + party + " nu a intrunit pragul si nu va fi considerat la alocarea mandatelor")
    
    return remaining_parties, independents
    
#votes - list of dicts               
def find_independents(votes):
    minus_counts = {}
    initial_parties = list(votes[0])
    for party in initial_parties:
        minus_counts[party] = 0
    
    for constituency in votes:
        for party in initial_parties:
            if constituency[party] < 0:
                minus_counts[party] += 1
    
    independents = []
    for party in initial_parties:
        if minus_counts[party] == len(votes) - 1:
            for i in range(0, len(votes)):
                if votes[i][party] >= 0:
                    independents.append(party)
    
    return independents
    
#constituency - dict   
def allocate_direct(constituency, constituency_mandates, relevant_parties, independents):
    global constituency_votes_total
    directly_allocated = {}
    remainders = {}
    remaining_mandates = constituency_mandates
    
    total_relevant_votes = 0
    for party in relevant_parties:
        total_relevant_votes += constituency[party]
    
    relevant_independents = []
    for independent in independents:
        if constituency[independent] > 0:
            relevant_independents.append(independent)
            total_relevant_votes += constituency[independent]
            
    electoral_coeff = math.floor(total_relevant_votes / constituency_mandates)
    print("Coeficientul electoral de circumscriptie este: " + str(electoral_coeff))
    
    for party in relevant_parties:
        allocated = math.floor(constituency[party] / electoral_coeff)
        remaining_mandates -= allocated
        directly_allocated[party] = allocated
        remainders[party] = constituency[party] - allocated * electoral_coeff
        constituency_votes_total += allocated * electoral_coeff
        if allocated > 0:
            print("Partidului " + party + " i-au fost alocate " + str(allocated) + " mandate prin alocare directa")
        
    for independent in independents:
        if constituency[independent] >= electoral_coeff:
            directly_allocated[independent] = 1
            remaining_mandates -= 1
            print("Candidatul independent " + independent + " a fost ales")
            
    return directly_allocated, remainders, remaining_mandates
    
def dHondt(votes, mandates):
    allocation = {}
    
    remainder_list = []
    for party in list(votes):
        for i in range(1, mandates+1):
            remainder_list.append(votes[party] / i)

    remainder_list.sort(reverse=True)
    national_electoral_coeff = remainder_list[mandates-1]
    
    for party in list(votes):
        allocation[party] = math.floor(votes[party] / national_electoral_coeff)

    for party in list(allocation):
        print(party + ": " + str(allocation[party]) + " mandate la redistribuire")
        
    return allocation

def redistribute_constituencies(remainders, remaining_mandates, remainders_sum, redistribution, votes):
    repartitions = []
    repartitions_constituencies = []
    repartition_coeffs = []

    total_to_redistribute = 0
    for i in range(0, len(remaining_mandates)):
        for party in list(votes):
            total_to_redistribute += remaining_mandates[i]

    for i in range(0, len(remainders)):
        repartition_constituency = []
        for party in list(redistribution):
            repartition_coefficient = (redistribution[party]*remainders[i][party])/remainders_sum[party]
            repartition_item = (party, i, repartition_coefficient)
            repartitions.append(repartition_item)
            repartition_constituency.append(repartition_item)
        repartitions_constituencies.append(repartition_constituency)
    
    repartitions.sort(key=lambda x : x[2], reverse=True)
    print("Lista sortata a repartitorilor la nivel national: ")
    for repartition in repartitions:
        print(repartition[0] + ", " + str(repartition[1] + 1) + ", " + str(repartition[2]))
    print("---------------------" + '\n')

    #print("Listele sortate ale repartitorilor la nivel de circumscriptie: ")
    for i in range(0, len(repartitions_constituencies)):
        repartitions_constituencies[i].sort(key=lambda x : x[2], reverse=True)
        #print("Circumscriptia " + str(i+1) + ": ")
        #for item in repartitions_constituencies[i]:
        #    print(item[0] + ", " + str(item[2]))
        repartition_coeff = repartitions_constituencies[i][remaining_mandates[i]-1][2]
        repartition_coeffs.append(repartition_coeff)

    current_mandates_party = {}
    current_mandates_constituency = [0]*len(remainders)
    redistributed_constituencies = []
    for party in list(redistribution):
        current_mandates_party[party] = 0

    for i in range(0, len(remainders)):
        redistributed_constituencies.append({})

    for repartition in repartitions:
        free_places = remaining_mandates[repartition[1]] - current_mandates_constituency[repartition[1]]
        if free_places < 1:
            print(repartition[0] + ", Circumscriptia " + str(repartition[1]+1) + ": Toate mandatele aferente circumscriptiei au fost alocate!")
            continue
        mandates_left = redistribution[repartition[0]] - current_mandates_party[repartition[0]];
        if current_mandates_party[repartition[0]] >= redistribution[repartition[0]]:
            print(repartition[0] + ", Circumscriptia " + str(repartition[1]+1) + ": Toate mandatele aferente partidului au fost redistribuite!")
            continue
        mandates_to_allocate = min(math.floor(repartition[2]/repartition_coeffs[repartition[1]]), free_places)
        mandates_to_allocate = max(mandates_to_allocate, 1)
        current_mandates_party[repartition[0]] += mandates_to_allocate
        current_mandates_constituency[repartition[1]] += mandates_to_allocate
        redistributed_constituencies[repartition[1]][repartition[0]] = mandates_to_allocate
        print(str(mandates_to_allocate) + " mandate au fost acordate partidului " + repartition[0] + " in circumscriptia " + str(repartition[1]+1) + "(" + constituency_names[repartition[1]] + ") ")

    return redistributed_constituencies    

#votes - list of dicts       
def allocate_constituencies(votes, n_mandates):
    relevant_parties, independents = party_cull(votes)      
    
    directly_allocated = []
    remainders = []
    remainders_sum = {}
    remaining_mandates_constituency = []
    total_remaining_mandates = 0
    for party in relevant_parties:
        remainders_sum[party] = 0

    print("---------------------" + '\n')
    
    for i in range(0, len(votes)):
        constituency_directs = {}
        constituency_remainders = {}
        remaining_mandates= 0

        print("Circumscriptia " + str(i+1) + ": " + constituency_names[i])
        print("Numarul mandatelor disponibile este " + str(n_mandates[i]))
        process_constituency = allocate_direct(votes[i], n_mandates[i], relevant_parties, independents)
        
        constituency_directs = process_constituency[0]
        constituency_remainders = process_constituency[1]
        remaining_mandates = process_constituency[2]
        
        directly_allocated.append(constituency_directs)
        remainders.append(constituency_remainders)
        remaining_mandates_constituency.append(remaining_mandates)
        
        for party in constituency_remainders:
            remainders_sum[party] += constituency_remainders[party]
            print("voturi la redistribuire pentru " + party + ": " + str(constituency_remainders[party]))
            
        total_remaining_mandates += remaining_mandates
        print(str(remaining_mandates) + " mandate nu au fost alocate si se vor redistribui national")
        print("---------------------" + '\n')


    print("Recapitulare alocare directa: ")
    print("Voturi totale utilizate: " + str(constituency_votes_total))
    total = 0
    for party in relevant_parties:
        total_party = 0
        for constituency in directly_allocated:
            total_party += constituency[party]
        total += total_party
        print(party + ": " + str(total_party))
    for independent in independents:
        for constituency in directly_allocated:
            if independent in list(constituency):
                total += 1
                print(independent + ": 1")
    print("Total alocate direct: " + str(total))
    print("La redistribuire: " + str(total_remaining_mandates))
    print("---------------------" + '\n')

    print("Redistribuire total: ")
    for party in list(remainders_sum):
        print(party + ": " + str(remainders_sum[party]) + " voturi de redistribuit")
    print("---------------------" + '\n')

    redistribution = dHondt(remainders_sum, total_remaining_mandates)
    print("---------------------" + '\n')

    print("Calcul final: ")
    total = 0
    for party in relevant_parties:
        total_party = redistribution[party]
        for constituency in directly_allocated:
            total_party += constituency[party]
        total += total_party        
        print(party + ": " + str(total_party))
    for independent in independents:
        for constituency in directly_allocated:
            if independent in list(constituency):
                total += 1
                print(independent + ": 1")
    print("Total mandate alocate: " + str(total))
    print("---------------------" + '\n')
    
    redistributed_mandates = redistribute_constituencies(remainders, remaining_mandates_constituency, remainders_sum, redistribution, votes)
    print("---------------------" + '\n')
    print("Redistribuire finală pe circumscriptii: " + '\n')
    for i in range(0, len(votes)):
        print("Circumscriptia " + str(i+1) + ": " + constituency_names[i])
        print("Numărul mandate totale disponibile " + str(n_mandates[i]))
        for party in list(directly_allocated[i]):
            if directly_allocated[i][party] > 0:
                print("Partidului " + party + " i-au fost alocate " + str(directly_allocated[i][party]) + " mandate prin alocare directa")
        print("Numărul mandatelor la redistribuire este " + str(remaining_mandates_constituency[i]))
        for party in list(redistributed_mandates[i]):
            print("Partidului " + party + " i-au fost alocate " + str(redistributed_mandates[i][party]) + " mandate prin redistribuire")
        print("---------------------" + '\n')      

    
    return directly_allocated, redistributed_mandates
        
mandates, constituency_names = read_mandates(sys.argv[1])
votes = read_votes(sys.argv[2])

constituencies, redistributed = allocate_constituencies(votes, mandates)

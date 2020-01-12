import csv
import math
import sys

NATIONAL_THRESHOLD = 0.05
CONSTITUENCY_THRESHOLD = 0.2

def read_mandates(mandates_filename):
    mandates = []
    with open(mandates_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            mandates.append(int(row[1]))
    return mandates
    
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
            print("Partidul " + party + " a trecut de pragul de circumscriptie în 4 circumscriptii")

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

#votes - list of dicts       
def allocate_constituencies(votes, n_mandates):
    relevant_parties, independents = party_cull(votes)      
    
    directly_allocated = []
    remainders = {}
    total_remaining_mandates = 0
    for party in relevant_parties:
        remainders[party] = 0

    print("---------------------" + '\n')
    
    for i in range(0, len(votes)):
        constituency_directs = {}
        constituency_remainders = {}
        remaining_mandates = 0

        print("Circumscriptia " + str(i+1))
        print("Numarul mandatelor disponibile este " + str(n_mandates[i]))
        process_constituency = allocate_direct(votes[i], n_mandates[i], relevant_parties, independents)
        
        constituency_directs = process_constituency[0]
        constituency_remainders = process_constituency[1]
        remaining_mandates = process_constituency[2]
        
        directly_allocated.append(constituency_directs)
        
        for party in constituency_remainders:
            remainders[party] += constituency_remainders[party]
            
        total_remaining_mandates += remaining_mandates
        print(str(remaining_mandates) + " mandate nu au fost alocate si se vor redistribui national")
        print("---------------------" + '\n')


    print("Recapitulare alocare directa: ")
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

    print("Redistribuire: ")
    for party in list(remainders):
        print(party + ": " + str(remainders[party]) + " voturi de redistribuit")
    print("---------------------" + '\n')

    redistribution = dHondt(remainders, total_remaining_mandates)
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
    
    return directly_allocated, redistribution
        
mandates = read_mandates(sys.argv[1])
votes = read_votes(sys.argv[2])

constituencies, redistribution = allocate_constituencies(votes, mandates)

import csv

names_cd = [
"pv_final_cnty_cd_ab.csv",
"pv_final_cnty_cd_ar.csv",
"pv_final_cnty_cd_ag.csv",
"pv_final_cnty_cd_bc.csv",
"pv_final_cnty_cd_bh.csv",
"pv_final_cnty_cd_bn.csv",
"pv_final_cnty_cd_bt.csv",
"pv_final_cnty_cd_bv.csv",
"pv_final_cnty_cd_br.csv",
"pv_final_cnty_cd_bz.csv",
"pv_final_cnty_cd_cl.csv",
"pv_final_cnty_cd_cs.csv",
"pv_final_cnty_cd_cj.csv",
"pv_final_cnty_cd_ct.csv",
"pv_final_cnty_cd_cv.csv",
"pv_final_cnty_cd_db.csv",
"pv_final_cnty_cd_dj.csv",
"pv_final_cnty_cd_gl.csv",
"pv_final_cnty_cd_gr.csv",
"pv_final_cnty_cd_gj.csv",
"pv_final_cnty_cd_hr.csv",
"pv_final_cnty_cd_hd.csv",
"pv_final_cnty_cd_il.csv",
"pv_final_cnty_cd_is.csv",
"pv_final_cnty_cd_if.csv",
"pv_final_cnty_cd_mm.csv",
"pv_final_cnty_cd_mh.csv",
"pv_final_cnty_cd_ms.csv",
"pv_final_cnty_cd_nt.csv",
"pv_final_cnty_cd_ot.csv",
"pv_final_cnty_cd_ph.csv",
"pv_final_cnty_cd_sj.csv",
"pv_final_cnty_cd_sm.csv",
"pv_final_cnty_cd_sb.csv",
"pv_final_cnty_cd_sv.csv",
"pv_final_cnty_cd_tr.csv",
"pv_final_cnty_cd_tm.csv",
"pv_final_cnty_cd_tl.csv",
"pv_final_cnty_cd_vl.csv",
"pv_final_cnty_cd_vs.csv",
"pv_final_cnty_cd_vn.csv",
"pv_final_cnty_cd_s1.csv",
"pv_final_cnty_cd_s2.csv",
"pv_final_cnty_cd_s3.csv",
"pv_final_cnty_cd_s4.csv",
"pv_final_cnty_cd_s5.csv",
"pv_final_cnty_cd_s6.csv",
"pv_final_cnty_cd_sr.csv",
"pv_final_cnty_cdc_sr.csv"]

names_s = [
"pv_final_cnty_s_ab.csv",
"pv_final_cnty_s_ar.csv",
"pv_final_cnty_s_ag.csv",
"pv_final_cnty_s_bc.csv",
"pv_final_cnty_s_bh.csv",
"pv_final_cnty_s_bn.csv",
"pv_final_cnty_s_bt.csv",
"pv_final_cnty_s_bv.csv",
"pv_final_cnty_s_br.csv",
"pv_final_cnty_s_bz.csv",
"pv_final_cnty_s_cl.csv",
"pv_final_cnty_s_cs.csv",
"pv_final_cnty_s_cj.csv",
"pv_final_cnty_s_ct.csv",
"pv_final_cnty_s_cv.csv",
"pv_final_cnty_s_db.csv",
"pv_final_cnty_s_dj.csv",
"pv_final_cnty_s_gl.csv",
"pv_final_cnty_s_gr.csv",
"pv_final_cnty_s_gj.csv",
"pv_final_cnty_s_hr.csv",
"pv_final_cnty_s_hd.csv",
"pv_final_cnty_s_il.csv",
"pv_final_cnty_s_is.csv",
"pv_final_cnty_s_if.csv",
"pv_final_cnty_s_mm.csv",
"pv_final_cnty_s_mh.csv",
"pv_final_cnty_s_ms.csv",
"pv_final_cnty_s_nt.csv",
"pv_final_cnty_s_ot.csv",
"pv_final_cnty_s_ph.csv",
"pv_final_cnty_s_sj.csv",
"pv_final_cnty_s_sm.csv",
"pv_final_cnty_s_sb.csv",
"pv_final_cnty_s_sv.csv",
"pv_final_cnty_s_tr.csv",
"pv_final_cnty_s_tm.csv",
"pv_final_cnty_s_tl.csv",
"pv_final_cnty_s_vl.csv",
"pv_final_cnty_s_vs.csv",
"pv_final_cnty_s_vn.csv",
"pv_final_cnty_s_s1.csv",
"pv_final_cnty_s_s2.csv",
"pv_final_cnty_s_s3.csv",
"pv_final_cnty_s_s4.csv",
"pv_final_cnty_s_s5.csv",
"pv_final_cnty_s_s6.csv",
"pv_final_cnty_s_sr.csv",
"pv_final_cnty_sc_sr.csv"]


def add_candidates(names):
    candidates = []
    for name in names:
        with open(name) as csv_file:
            csvr = csv.reader(csv_file)
            row1 = next(csvr)
            for item in row1:
                if "voturi" in item and item not in candidates:
                    candidates.append(item)
    return candidates

def add_data(candidates, names):
    data = []
    data.append(candidates)

    constituency_BUC = {}
    constituency_Diaspora = {}
    for candidate in candidates:
        constituency_BUC[candidate] = 0
        constituency_Diaspora[candidate] = 0

    for name in names:
        constituency_data = {}
        for candidate in candidates:
            constituency_data[candidate] = 0
        with open(name) as csv_file:
            csvr = csv.DictReader(csv_file)
            for row in csvr:
                for candidate in candidates:
                    if candidate in list(row):
                        constituency_data[candidate] += int(row[candidate])
        for candidate in candidates:
            if constituency_data[candidate] == 0:
                if "INDEPENDENT" in candidate:
                    constituency_data[candidate] = -1

        should_append = False
        should_append_BUC = False
        should_append_Diaspora = False
        for candidate in candidates:
            if "_s1" in name or "_s2" in name or "_s3" in name or "_s4" in name or "_s5" in name:
                constituency_BUC[candidate] += constituency_data[candidate]
            elif "_s6" in name:
                constituency_BUC[candidate] += constituency_data[candidate]
                should_append_BUC = True
            elif "_sr" in name:
                constituency_Diaspora[candidate] += constituency_data[candidate]
                if "c_sr" in name:
                    should_append_Diaspora = True
            else:
                should_append = True
        
        if should_append:
            data.append(constituency_data.values())
        elif should_append_BUC:
            data.append(constituency_BUC.values())
        elif should_append_Diaspora:
            data.append(constituency_Diaspora.values())
    

    return data

candidates_cd = add_candidates(names_cd)
data_cd = add_data(candidates_cd, names_cd)

with open('cdep2020.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data_cd)

candidates_s = add_candidates(names_s)
data_s = add_data(candidates_s, names_s)

with open('senat2020.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data_s)

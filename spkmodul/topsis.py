import math, pprint
from prettytable import PrettyTable


class Spk:
    def __init__(self) -> None:
        pass

    def topsis(self, alternatif):
        res = []

        # membuat tabel nilai bobot

        pt = PrettyTable()

        nilai_bobot = {
            "c1":15,
            "c2":15,
            "c3":15,
            "c4":55,
            "total":0
        }

        nilai_bobot["total"] = sum([
            nilai_bobot["c1"],
            nilai_bobot["c2"],
            nilai_bobot["c3"],
            nilai_bobot["c4"],
        ])

        pt.field_names = ["No", "TABEL BOBOT", "NILAI"]
        for i, data_nilai_bobot in enumerate(list(nilai_bobot)):
            if data_nilai_bobot != "total":
                pt.add_row([i + 1, data_nilai_bobot, nilai_bobot[data_nilai_bobot]])
        pt.add_row(["---", "TOTAL", nilai_bobot["total"]])
        
        res.append(pt.get_string())

        # membua tabel alternatif & kriteria

        bobot = {
            "c1":nilai_bobot["c1"] / nilai_bobot["total"],
            "c2":nilai_bobot["c2"] / nilai_bobot["total"],
            "c3":nilai_bobot["c3"] / nilai_bobot["total"],
            "c4":nilai_bobot["c4"] / nilai_bobot["total"],
        }

        cost_benefit = {
            "c1":"cost",
            "c2":"cost",
            "c3":"cost",
            "c4":"cost",
        }

        pt = PrettyTable()
        pt.field_names = ["No", "ALTERNATIF" ,"C1", "C2", "C3", "C4"]
        for i, x in enumerate(list(alternatif)):
            pt.add_row([i + 1, x.upper(), (alternatif[x])[0], (alternatif[x])[1], (alternatif[x])[2], (alternatif[x])[3]])
        pt.add_row(["---", "---", cost_benefit["c1"].upper(), cost_benefit["c2"].upper(),cost_benefit["c3"].upper(), cost_benefit["c4"].upper()])
        pt.add_row(["---", "BOBOT", bobot["c1"], bobot["c2"], bobot["c3"], bobot["c4"]])

        res.append("TABEL ALTERNATIF & KRITERIA\n"+pt.get_string())

        # membuat MATRIX TERNORMALISASI (R)

        pembagi = {
            "c1":math.sqrt(
                ((alternatif["a1"])[0] ** 2) +
                ((alternatif["a2"])[0] ** 2) +
                ((alternatif["a3"])[0] ** 2)
            ),
            "c2":math.sqrt(
                ((alternatif["a1"])[1] ** 2) +
                ((alternatif["a2"])[1] ** 2) +
                ((alternatif["a3"])[1] ** 2)
            ),
            "c3":math.sqrt(
                ((alternatif["a1"])[2] ** 2) +
                ((alternatif["a2"])[2] ** 2) +
                ((alternatif["a3"])[2] ** 2)
            ),
            "c4":math.sqrt(
                ((alternatif["a1"])[3] ** 2) +
                ((alternatif["a2"])[3] ** 2) +
                ((alternatif["a3"])[3] ** 2)
            ),
        }

        normalize_mtrx = []

        pt = PrettyTable()
        pt.field_names = ["No", "PEMBAGI", pembagi["c1"], pembagi["c2"], pembagi["c3"], pembagi["c4"]]
        for i, normalize in enumerate(list(alternatif)):
            nrmlz = [
                ((alternatif[normalize])[0] / pembagi["c1"]),
                ((alternatif[normalize])[1] / pembagi["c2"]),
                ((alternatif[normalize])[2] / pembagi["c3"]),
                ((alternatif[normalize])[3] / pembagi["c4"]),
            ]
            pt.add_row([i + 1,"R"] + nrmlz)
            normalize_mtrx.append(nrmlz)
        
        res.append("MATRIX TERNORMALISASI (R)\n\n"+pt.get_string())

        # membuat MATRIX TERNORMALISASI TERBOBOT (Y) 

        normalize_weight_mtrx = []   

        pt = PrettyTable()
        for i, normalize_weight in enumerate(normalize_mtrx):
            nrmlzw = [
                (normalize_weight[0] * bobot["c1"]),
                (normalize_weight[1] * bobot["c2"]),
                (normalize_weight[2] * bobot["c3"]),
                (normalize_weight[3] * bobot["c4"]),
            ]
            pt.add_row([i + 1,"Y"] + nrmlzw)
            normalize_weight_mtrx.append(nrmlzw)
        
        res.append("MATRIX TERNORMALISASI TERBOBOT (Y)\n\n"+pt.get_string())

        normalize_weight_mtrx_vert = {
            "c1":[],
            "c2":[],
            "c3":[],
            "c4":[],
        }

        for x in normalize_weight_mtrx:
            for i, y in enumerate(x):
                normalize_weight_mtrx_vert[f"c{i+1}"].append(y)
        
        # membuat SOLUSI IDEAL POSITIF
        
        pt = PrettyTable()
        positif_idela_solution = []
        
        for x in list(normalize_weight_mtrx_vert):
            if cost_benefit[x] == "benefit":
                positif_idela_solution.append(max(normalize_weight_mtrx_vert[x]))
            else:
                positif_idela_solution.append(min(normalize_weight_mtrx_vert[x]))
        
        pt.add_row(positif_idela_solution)
        res.append("SOLUSI IDEAL POSITIF (Y+ / A+)\n\n"+pt.get_string())

        pt = PrettyTable()
        negatif_ideal_solution = []

        for x in list(normalize_weight_mtrx_vert):
            if cost_benefit[x] == "cost":
                negatif_ideal_solution.append(max(normalize_weight_mtrx_vert[x]))
            else:
                negatif_ideal_solution.append(min(normalize_weight_mtrx_vert[x]))
        
        pt.add_row(negatif_ideal_solution)
        res.append("SOLUSI IDEAL NEGATIF (Y- / A-)\n\n"+pt.get_string())

        distance_positif_ideal_solution = {
            "d1+":self.distance_ideal_solution_proc(normalize_weight_mtrx[0], positif_idela_solution),
            "d2+":self.distance_ideal_solution_proc(normalize_weight_mtrx[1], positif_idela_solution),
            "d3+":self.distance_ideal_solution_proc(normalize_weight_mtrx[2], positif_idela_solution),
        }

        pt = PrettyTable()
        pt.field_names = ["No.", "D+", "NILAI"]
        for i, dpis in enumerate(list(distance_positif_ideal_solution)):
            pt.add_row([i + 1, dpis.upper(), distance_positif_ideal_solution[dpis]])

        res.append("JARAK ANTARA NILAI TERBOBOT TERHADAP SOLUSI IDEAL POSITIF (D+)\n\n"+pt.get_string())

        distance_negative_ideal_solution = {
            "d1-":self.distance_ideal_solution_proc(negatif_ideal_solution, normalize_weight_mtrx[0]),
            "d2-":self.distance_ideal_solution_proc(negatif_ideal_solution, normalize_weight_mtrx[1]),
            "d3-":self.distance_ideal_solution_proc(negatif_ideal_solution, normalize_weight_mtrx[2]),
        }

        pt = PrettyTable()
        pt.field_names = ["No.", "D-", "NILAI"]
        for i, dnis in enumerate(list(distance_negative_ideal_solution)):
            pt.add_row([i + 1, dnis.upper(), distance_negative_ideal_solution[dnis]])

        res.append("JARAK ANTARA NILAI TERBOBOT TERHADAP SOLUSI IDEAL NEGATIF (D-)\n\n"+pt.get_string())

        refrence_value = {
            "v1":distance_negative_ideal_solution["d1-"] / (distance_negative_ideal_solution["d1-"] + distance_positif_ideal_solution["d1+"]),
            "v2":distance_negative_ideal_solution["d2-"] / (distance_negative_ideal_solution["d2-"] + distance_positif_ideal_solution["d2+"]),
            "v3":distance_negative_ideal_solution["d3-"] / (distance_negative_ideal_solution["d3-"] + distance_positif_ideal_solution["d3+"]),
        }

        refrence_value_rank = dict(sorted(refrence_value.items(), key=lambda item: item[1], reverse=True))

        pt = PrettyTable()
        pt.field_names = ["REFERENCE" ,"NILAI", "RANK"]
        for i, ref in enumerate(list(refrence_value_rank)):
            pt.add_row([f"{ref.upper()} (Image {chr(66+(int(ref[1:])-1))})", refrence_value_rank[ref], i + 1])

        res.append("NILAI PREFERENSI (V)\n\n"+pt.get_string())

        return res, refrence_value_rank

    def distance_ideal_solution_proc(self, x, y):
        total = 0
        for i, data in enumerate(x):
            total += ((y[i] - data) ** 2)
        
        return math.sqrt(total)

    

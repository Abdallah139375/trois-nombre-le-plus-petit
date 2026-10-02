# Exercice 13 - Assurances
print("Entrez le montant des dommages (en euros) :")
dommages = float(input())
franchise = dommages * 10 / 100
if franchise > 4000:
    franchise = 4000
rembourse = dommages - franchise
print("Franchise :", franchise, "euros")
print("Montant remboursé :", rembourse, "euros")

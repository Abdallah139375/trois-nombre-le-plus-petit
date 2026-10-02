# Exercice 12 - Admission
print("Entrez la note :")
note = float(input())
if note < 8:
    print("ajourné")
elif note < 10:
    print("oral")
else:
    print("admis")

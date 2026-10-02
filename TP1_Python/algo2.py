# Mini projet - Algorigramme 2 : valeur correspondant à une couleur
print("Entrez une couleur :")
couleur = input().lower().strip()
if couleur == "noir":
    valeur = 0
elif couleur == "marron":
    valeur = 1
elif couleur == "rouge":
    valeur = 2
elif couleur == "orange":
    valeur = 3
elif couleur == "jaune":
    valeur = 4
elif couleur == "vert":
    valeur = 5
elif couleur == "bleu":
    valeur = 6
elif couleur == "violet":
    valeur = 7
elif couleur == "gris":
    valeur = 8
elif couleur == "blanc":
    valeur = 9
else:
    valeur = -1
if valeur == -1:
    print("Couleur inconnue")
else:
    print("La valeur de la couleur", couleur, "est", valeur)

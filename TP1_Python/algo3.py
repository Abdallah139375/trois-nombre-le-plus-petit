# Mini projet - Algorigramme 3 : convertir 3 couleurs en valeur R = X * 10^Y


def valeur_couleur(couleur):
    couleur = couleur.lower().strip()
    if couleur == "noir":
        return 0
    elif couleur == "marron":
        return 1
    elif couleur == "rouge":
        return 2
    elif couleur == "orange":
        return 3
    elif couleur == "jaune":
        return 4
    elif couleur == "vert":
        return 5
    elif couleur == "bleu":
        return 6
    elif couleur == "violet":
        return 7
    elif couleur == "gris":
        return 8
    elif couleur == "blanc":
        return 9
    else:
        return -1


print("Couleur de l'anneau 1 :")
c1 = valeur_couleur(input())
print("Couleur de l'anneau 2 :")
c2 = valeur_couleur(input())
print("Couleur de l'anneau 3 :")
c3 = valeur_couleur(input())

if c1 == -1 or c2 == -1 or c3 == -1:
    print("Erreur : couleur inconnue")
else:
    x = c1 * 10 + c2
    y = c3
    r = x * 10 ** y
    print("R =", r, "ohms")

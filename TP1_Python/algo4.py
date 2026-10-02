# Mini projet - Algorigramme 4 : valeur et tolérance d'une résistance


# Sous-programme 1 (algorigramme 1) : saisie des 4 couleurs
def saisir_couleurs():
    print("Couleur de l'anneau 1 :")
    c1 = input()
    print("Couleur de l'anneau 2 :")
    c2 = input()
    print("Couleur de l'anneau 3 :")
    c3 = input()
    print("Couleur de l'anneau 4 (tolérance) :")
    c4 = input()
    return c1, c2, c3, c4


# Sous-programme 2 (algorigramme 2) : couleur -> chiffre
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


# Sous-programme 3 (algorigramme 3) : 3 couleurs -> valeur de R
def valeur_resistance(c1, c2, c3):
    v1 = valeur_couleur(c1)
    v2 = valeur_couleur(c2)
    v3 = valeur_couleur(c3)
    if v1 == -1 or v2 == -1 or v3 == -1:
        return -1
    x = v1 * 10 + v2
    y = v3
    return x * 10 ** y


# Nouveau sous-programme : 4e couleur -> tolérance (tableau de l'énoncé)
def tolerance(couleur):
    couleur = couleur.lower().strip()
    if couleur == "marron":
        return "1%"
    elif couleur == "rouge":
        return "2%"
    elif couleur == "vert":
        return "0,25%"
    elif couleur == "bleu":
        return "0,2%"
    elif couleur == "violet":
        return "0,1%"
    elif couleur == "or":
        return "5%"
    elif couleur == "argent":
        return "10%"
    else:
        return "inconnue"


# Programme principal
c1, c2, c3, c4 = saisir_couleurs()
r = valeur_resistance(c1, c2, c3)
t = tolerance(c4)
if r == -1:
    print("Erreur : une des trois premières couleurs est inconnue")
else:
    print("Valeur de la résistance : R =", r, "ohms")
    print("Tolérance :", t)

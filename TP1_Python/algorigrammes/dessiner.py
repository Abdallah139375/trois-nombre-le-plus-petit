# Génère les algorigrammes (images PNG) de chaque exercice du TP1
import os
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

CW, LH, GAP = 0.17, 0.42, 0.55   # largeur d'un caractère, hauteur de ligne, espace
UNIT = 0.5                         # 1 unité = 0,5 pouce
DOSSIER = os.path.dirname(os.path.abspath(__file__))


class Noeud:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    @property
    def top(self):
        return (self.x, self.y + self.h / 2)

    @property
    def bot(self):
        return (self.x, self.y - self.h / 2)

    @property
    def left(self):
        return (self.x - self.w / 2, self.y)

    @property
    def right(self):
        return (self.x + self.w / 2, self.y)


class Point(Noeud):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 0)


class Algo:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.pts = []
        self.prims = []

    def taille(self, texte, forme):
        lignes = texte.split("\n")
        tw = max(len(l) for l in lignes) * CW
        th = len(lignes) * LH
        if forme == "test":
            b = th / 2 + 0.45
            a = (tw / 2) / (1 - (th / 2) / b) + 0.25
            return 2 * a, 2 * b
        w, h = tw + 0.5, th + 0.35
        if forme == "sp":
            w += 0.5
        return w, h

    def noeud(self, texte, x, y, forme="rect"):
        w, h = self.taille(texte, forme)
        n = Noeud(x, y, w, h)
        self.prims.append({"t": "forme", "forme": forme, "x": x, "y": y, "w": w, "h": h, "texte": texte})
        ax = self.ax
        if forme == "test":
            ax.add_patch(Polygon([n.top, n.right, n.bot, n.left], closed=True,
                                 fc="#fff4d6", ec="k", lw=1.3))
        else:
            couleur = {"rect": "#e8f0ff", "debut": "#dff5df", "sp": "#f3e6ff"}[forme]
            ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=couleur, ec="k", lw=1.3))
            if forme == "sp":
                for dx in (0.18, w - 0.18):
                    ax.plot([x - w / 2 + dx] * 2, [y - h / 2, y + h / 2], "k", lw=1.1)
        ax.text(x, y, texte, ha="center", va="center", fontsize=10, family="DejaVu Sans",
                linespacing=1.25)
        self.pts += [(x - w / 2, y - h / 2), (x + w / 2, y + h / 2)]
        return n

    def placer(self, texte, x, haut, forme="rect"):
        """Place une boîte dont le haut est à l'ordonnée 'haut'."""
        w, h = self.taille(texte, forme)
        return self.noeud(texte, x, haut - h / 2, forme)

    def ligne(self, pts, fleche=True):
        self.pts += pts
        self.prims.append({"t": "ligne", "pts": [list(p) for p in pts], "fleche": fleche})
        xs, ys = zip(*pts)
        if fleche and len(pts) >= 2:
            self.ax.plot(xs[:-1], ys[:-1], "k", lw=1.2)
            self.ax.annotate("", xy=pts[-1], xytext=pts[-2],
                             arrowprops=dict(arrowstyle="-|>", lw=1.2, color="k",
                                             shrinkA=0, shrinkB=0, mutation_scale=14))
        else:
            self.ax.plot(xs, ys, "k", lw=1.2)

    def etiquette(self, texte, x, y):
        self.prims.append({"t": "etiquette", "texte": texte, "x": x, "y": y})
        self.ax.text(x, y, texte, fontsize=9, color="#b00000", style="italic",
                     ha="left", va="center")

    def suite(self, prec, y, elements, x=0):
        """Enchaîne des boîtes les unes sous les autres."""
        for texte, forme in elements:
            n = self.placer(texte, x, y, forme)
            if prec is not None:
                self.ligne([prec.bot, n.top])
            prec, y = n, n.bot[1] - GAP
        return prec, y

    def selon(self, prec, y, branches, sinon, x=0):
        """Chaîne de tests si / sinon si / sinon. Retourne le point de jonction."""
        tests = []
        for i, (cond, _) in enumerate(branches):
            d = self.placer(cond, x, y, "test")
            self.ligne([prec.bot, d.top])
            if i > 0:
                self.etiquette("non", x + 0.12, prec.bot[1] - 0.22)
            tests.append(d)
            prec, y = d, d.bot[1] - GAP
        xr = max(d.right[0] for d in tests) + 0.9
        actions = []
        for d, (_, act) in zip(tests, branches):
            w, _ = self.taille(act, "rect")
            a = self.noeud(act, xr + w / 2, d.y)
            self.ligne([d.right, a.left])
            self.etiquette("oui", d.right[0] + 0.1, d.y + 0.2)
            actions.append(a)
        e = self.placer(sinon, x, y)
        self.ligne([prec.bot, e.top])
        self.etiquette("non", x + 0.12, prec.bot[1] - 0.22)
        ym = e.bot[1] - 0.45
        xm = max(a.right[0] for a in actions) + 0.4
        for a in actions:
            self.ligne([a.right, (xm, a.y)], fleche=False)
        self.ligne([(xm, actions[0].y), (xm, ym), (x, ym)])
        self.ligne([e.bot, (x, ym)], fleche=False)
        return Point(x, ym), ym - GAP

    def sauver(self, nom):
        xs, ys = zip(*self.pts)
        m = 0.4
        x0, x1, y0, y1 = min(xs) - m, max(xs) + m, min(ys) - m, max(ys) + m
        self.ax.set_xlim(x0, x1)
        self.ax.set_ylim(y0, y1)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.fig.set_size_inches((x1 - x0) * UNIT, (y1 - y0) * UNIT)
        with open(os.path.join(DOSSIER, nom + ".json"), "w", encoding="utf-8") as f:
            json.dump({"bornes": [x0, x1, y0, y1], "prims": self.prims}, f, ensure_ascii=False)
        chemin = os.path.join(DOSSIER, nom + ".png")
        self.fig.savefig(chemin, dpi=200, facecolor="white")
        plt.close(self.fig)
        return chemin


D, R, T, SP = "debut", "rect", "test", "sp"


def exo10():
    a = Algo()
    n, y = a.suite(None, 0, [
        ("Début", D),
        ("float val1\nfloat val2\nfloat val3\nfloat moy", R),
        ('val1 ← "Entrez la valeur 1"', R),
        ('val2 ← "Entrez la valeur 2"', R),
        ('val3 ← "Entrez la valeur 3"', R),
        ("moy ← (val1 + val2 + val3) / 3", R),
        ('Afficher "La moyenne est :", moy', R),
        ("Fin", D)])
    return a.sauver("exo10")


def exo11():
    a = Algo()
    a.suite(None, 0, [
        ("Début", D),
        ("float longueur\nfloat largeur\nfloat surface", R),
        ('longueur ← "Entrez la longueur"', R),
        ('largeur ← "Entrez la largeur"', R),
        ("surface ← longueur × largeur", R),
        ('Afficher "La surface est :", surface', R),
        ("Fin", D)])
    return a.sauver("exo11")


def exo12():
    a = Algo()
    n, y = a.suite(None, 0, [("Début", D), ("float note", R),
                             ('note ← "Entrez la note"', R)])
    n, y = a.selon(n, y, [("note < 8 ?", 'Afficher "ajourné"'),
                          ("note < 10 ?", 'Afficher "oral"')],
                   'Afficher "admis"')
    a.suite(n, y, [("Fin", D)])
    return a.sauver("exo12")


def exo13():
    a = Algo()
    n, y = a.suite(None, 0, [
        ("Début", D),
        ("float dommages\nfloat franchise\nfloat rembourse", R),
        ('dommages ← "Entrez le montant des dommages"', R),
        ("franchise ← dommages × 10 / 100", R)])
    d = a.placer("franchise > 4000 ?", 0, y, T)
    a.ligne([n.bot, d.top])
    xr = d.right[0] + 0.9
    w, _ = a.taille("franchise ← 4000", R)
    b = a.noeud("franchise ← 4000", xr + w / 2, d.y)
    a.ligne([d.right, b.left])
    a.etiquette("oui", d.right[0] + 0.1, d.y + 0.2)
    ym = d.bot[1] - 0.6
    a.ligne([b.bot, (b.x, ym), (0, ym)])
    a.ligne([d.bot, (0, ym)], fleche=False)
    a.etiquette("non", 0.12, d.bot[1] - 0.25)
    a.suite(Point(0, ym), ym - GAP, [
        ("rembourse ← dommages − franchise", R),
        ('Afficher "Franchise :", franchise', R),
        ('Afficher "Montant remboursé :", rembourse', R),
        ("Fin", D)])
    return a.sauver("exo13")


def exo14():
    a = Algo()
    n, y = a.suite(None, 0, [("Début", D), ("int n\nint i", R),
                             ('n ← "Entrez la valeur de n"', R), ("i ← 0", R)])
    yj = y
    y -= 0.5
    a.ligne([n.bot, (0, y)])
    d = a.placer("i ≤ 10 ?", 0, y, T)
    b1, y2 = a.suite(d, d.bot[1] - GAP, [
        ('Afficher n, "x", i, "=", n × i', R), ("i ← i + 1", R)])
    a.etiquette("oui", 0.12, d.bot[1] - 0.22)
    xl = -max(b1.w, 4) / 2 - 1.0
    yb = b1.bot[1] - 0.4
    a.ligne([b1.bot, (0, yb), (xl, yb), (xl, yj - 0.25), (-0.05, yj - 0.25)])
    xr = d.right[0] + 1.6
    f = a.placer("Fin", 0, yb - 0.9, D)
    a.ligne([d.right, (xr, d.y), (xr, f.top[1] + 0.35), (0, f.top[1] + 0.35), f.top])
    a.etiquette("non", d.right[0] + 0.1, d.y + 0.2)
    return a.sauver("exo14")


def algo1():
    a = Algo()
    a.suite(None, 0, [
        ("Début", D),
        ("chaîne couleur1\nchaîne couleur2\nchaîne couleur3\nchaîne couleur4", R),
        ('couleur1 ← "Couleur de l\'anneau 1"', R),
        ('couleur2 ← "Couleur de l\'anneau 2"', R),
        ('couleur3 ← "Couleur de l\'anneau 3"', R),
        ('couleur4 ← "Couleur de l\'anneau 4"', R),
        ('Afficher "Couleurs enregistrées :",\ncouleur1, couleur2, couleur3, couleur4', R),
        ("Fin", D)])
    return a.sauver("algo1")


COULEURS = ["noir", "marron", "rouge", "orange", "jaune",
            "vert", "bleu", "violet", "gris", "blanc"]


def algo2():
    a = Algo()
    n, y = a.suite(None, 0, [("Début", D), ("chaîne couleur\nint valeur", R),
                             ('couleur ← "Entrez une couleur"', R)])
    n, y = a.selon(n, y, [(f'couleur = "{c}" ?', f"valeur ← {i}")
                          for i, c in enumerate(COULEURS)], "valeur ← -1")
    n, y = a.selon(n, y, [("valeur = -1 ?", 'Afficher "Couleur inconnue"')],
                   'Afficher "La valeur est", valeur')
    a.suite(n, y, [("Fin", D)])
    return a.sauver("algo2")


def algo3():
    a = Algo()
    n, y = a.suite(None, 0, [
        ("Début", D),
        ("chaîne c1, c2, c3\nint v1, v2, v3\nint X, Y, R", R),
        ('c1 ← "Couleur de l\'anneau 1"', R),
        ('c2 ← "Couleur de l\'anneau 2"', R),
        ('c3 ← "Couleur de l\'anneau 3"', R),
        ("v1 ← valeur_couleur(c1)", SP),
        ("v2 ← valeur_couleur(c2)", SP),
        ("v3 ← valeur_couleur(c3)", SP)])
    n, y = a.selon(n, y, [("v1 = -1 ou v2 = -1\nou v3 = -1 ?",
                           'Afficher "Erreur :\ncouleur inconnue"')],
                   "X ← v1 × 10 + v2\nY ← v3\nR ← X × 10^Y\nAfficher \"R =\", R")
    a.suite(n, y, [("Fin", D)])
    return a.sauver("algo3")


def algo4():
    a = Algo()
    n, y = a.suite(None, 0, [
        ("Début", D),
        ("chaîne c1, c2, c3, c4\nint R\nchaîne T", R),
        ("c1, c2, c3, c4 ← saisir_couleurs()\n(algorigramme 1)", SP),
        ("R ← valeur_resistance(c1, c2, c3)\n(algorigramme 3, qui utilise l'algo 2)", SP),
        ("T ← tolerance(c4)\n(sous-programme tolérance)", SP)])
    n, y = a.selon(n, y, [("R = -1 ?", 'Afficher "Erreur :\ncouleur inconnue"')],
                   'Afficher "R =", R\nAfficher "Tolérance :", T')
    a.suite(n, y, [("Fin", D)])
    return a.sauver("algo4")


def tolerance():
    a = Algo()
    n, y = a.suite(None, 0, [("Début tolerance(couleur)", D)])
    tol = [("marron", "1%"), ("rouge", "2%"), ("vert", "0,25%"), ("bleu", "0,2%"),
           ("violet", "0,1%"), ("or", "5%"), ("argent", "10%")]
    n, y = a.selon(n, y, [(f'couleur = "{c}" ?', f'T ← "{t}"') for c, t in tol],
                   'T ← "inconnue"')
    a.suite(n, y, [("Retourner T", D)])
    return a.sauver("tolerance")


if __name__ == "__main__":
    for f in (exo10, exo11, exo12, exo13, exo14, algo1, algo2, algo3, algo4, tolerance):
        print(f())


## Gestions des positions, et coups valides sur une position :

## Bienvenu dans la zone de test :

# -----------------------------------------------

nom_fichier =r"C:\Users\Fantôme\OneDrive\Bureau\TIPE\TIPE2\DATA\data_lenny_pos_lose.txt"
nom_fichier_n =r"C:\Users\Fantôme\OneDrive\Bureau\TIPE\TIPE2\DATA\fichier_data_"
##
# ------------------------------------------------------------------

# On choisis ces symboles pour représenter la fin des structures
Char_End_Boundary = '.'
Char_End_Region = '|'
Char_End_Land =   '+'
Char_Empty_Position = '!'

# Traduction Anglais <-> Français (faites par moi...): 
# Boundary = delimitation
# Region = region
# Land = terre
# Position = position

# Vecteurs temporaires réservé pour ensuite être renommé
Child_vtx_1="4"
Child_vtx_2="5"
Child_vtx_3="6"

# ------------------------------------------------------------------
# Donneés intéressantes pour savoir quoi optimiser :
# ------------------------------------------------------------------

Duree_can = 0
#-----Inclu dans durée can ------
Duree_suppr_mort = 0
Duree_transfo_simple = 0
Duree_transfo_simple_simple = 0
Duree_tri_sup = 0
Duree_tri_prio = 0
Duree_compa_pere_fils = 0
# -------------------------------
present_3_fois = 0
Duree_sep = 0
Duree_ordre_ligne = 0
# -------------------------------
Duree_recherche = 0
Duree_cal_enfant = 0
Duree_nbr_vie = 0


# ------------------------------------------------------------------
# Fonctions générales
# ------------------------------------------------------------------

def est_une_lettre(a):
    return ((64 < ord(a) < 91) or (96 < ord(a) < 123))

def est_minuscule(a):
    return (96 < ord(a) < 123)

def est_majuscule(a):
    return (64 < ord(a) < 91)

def ordreligne(ligne1,ligne2):
    """retourne l'ordre entre deux positions d'une region selon le pseudo-ordre 0<1<2<a=b=c...<A=B=C..."""
    a = time()
    global Duree_ordre_ligne
    for i in range(len(ligne1)):
        if not(est_une_lettre(ligne1[i])) or not(est_une_lettre(ligne2[i])) :
            if ligne1[i] != ligne2[i] :
                Duree_ordre_ligne += time() - a
                return (ligne1[i]<ligne2[i])
        else :
            if est_minuscule(ligne1[i]) and est_majuscule(ligne2[i]):
                Duree_ordre_ligne += time() - a
                return True
            elif est_majuscule(ligne1[i]) and est_minuscule(ligne2[i]) :
                Duree_ordre_ligne += time() - a
                return False
    Duree_ordre_ligne += time() - a
    return ligne1<ligne2


def position_tri_permut(delimitation:str):
    """Retourne la permutation d'une delimitation la plus propice selon le pseudo-ordre"""
    taille_position = len(delimitation)
    if taille_position < 3 :
        return delimitation

    delimitation = delimitation[:-1]
    rotation = delimitation

    def rotation_de_1(string):
        out = str(string[-1])
        for i in range(len(string)-1):
            out += string[i]
        return out

    for i in range(1,taille_position-1):
        rotation = rotation_de_1(rotation)
        if ordreligne(rotation,delimitation) == True :
            delimitation = rotation
    delimitation += Char_End_Boundary

    return delimitation



def position_retourne(delimitation):
    """Retourne l'orientation d'une delimitation"""
    delimitation = delimitation[:-1]
    delimitation = delimitation[::-1]
    delimitation += Char_End_Boundary
    return delimitation



def position_tri(delimitation):
    """Tri la delimitation dans la meilleure postion qui soit"""
    delimitation = position_tri_permut(delimitation)
    sauv = delimitation
    delimitation = position_tri_permut(position_retourne(delimitation))
    if (ordreligne(sauv,delimitation) == True) :
        return sauv
    return delimitation


def Est_Un_Simple_Point(delimitation):
    """Indique si la delimitation est un simple point"""
    if delimitation == "0." :
        return True
    return False

def suppr_doublons(Liste):
    Stock = []
    for i in Liste :
        if not(i in Stock) :
            Stock.append(i)
    return Stock

# ------------------------------------------------------------------
# Partie calculs des enfants de delimitations (structure la plus petite)
# ------------------------------------------------------------------


def remplace_string(string,lettre,indice):
    """remplace l'element d'indice i d'une liste par la lettre entrée"""
    new_string = ""
    for i in range(indice):
        new_string += string[i]
    new_string += lettre
    for i in range(indice+1,len(string)):
        new_string += string[i]
    return new_string


def insertion_rapide(string_a_inserer,string,i1,i2):
    for i in range(i1,i2):
        string_a_inserer += string[i]
    return string_a_inserer

#Type de coup 1 : lier une delimitation à elle-même
# On définit un enfant comme une couple de delimitation : la delimitation intérieure et la region extérieure

def calcul_enfant_type_1(delimitation,Liste_des_sucesseurs):
    #Remarque : la delimitation ne devrait pas être vide à cause de la canonization
    # On traitera différement les positions avec un seul point (0. ; 1. ; 2.) des autres.

    if len(delimitation) < 2 :
        print("erreur, la delimitation est vide")
        return

    #Cas où la delimitation n'a qu'un seul point : seul coup possible : relier le point à lui-même, ce qui peut se faire uniquement si il a 0. ou 1.
    if len(delimitation) == 2 :
        v = delimitation[0]
        if v == "0" or v == "1" :
            if v == "0" :
                Liste_des_sucesseurs.append(("46.","46."))
            if v == "1" :
                Liste_des_sucesseurs.append(("36.","36."))
        return Liste_des_sucesseurs

##    if len(delimitation) == 3 :
##        enfant0 = delimitation[0] + Child_vtx_3
##        Liste_des_sucesseurs.append((enfant0 + positi on[1]+ Char_End_Boundary,delimitation[0] + Child_vtx_3 + delimitation[1]+ Char_End_Boundary))
##        return Liste_des_sucesseurs

    # On enlève le caractère de fin de postition
    delimitation = delimitation[:-1]

    # On fait une double boucle afin d'essayer toutes les combinaisons de liaison de points possibles
    for s1 in range(len(delimitation)):
        for s2 in range(s1,len(delimitation)):
            if (not(s1==s2 and delimitation[s1]=="2")) and (not(delimitation[s1]==delimitation[s2] and not(delimitation[s1] == "0" or delimitation[s1] == "1" or delimitation[s1] == "2"))):
                new_pos = delimitation
                v1 = delimitation[s1]
                v2 = delimitation[s2]
                if s1 != s2 :
                    #les vecteur de degré 1 deviennent des lettres
                    if v1 == "1" :
                        v1 = "4"
                        new_pos = remplace_string(new_pos,"4",s1) #"4" = Child_vtx_1
                    if v2 == "1" :
                        v2 = "5"
                        new_pos = remplace_string(new_pos,"5",s2) #"5" = Child_vtx_2
                    #Les vecteurs de degré 2 deviennent de degré 3
                    if v1 == "2" :
                        v1 = "3"
                        new_pos = remplace_string(new_pos,"3",s1)
                    if v2 == "2" :
                        v2 = "3"
                        new_pos = remplace_string(new_pos,"3",s2)
                else : #On lie un point à lui-même -> son degré passe de 1 à 3
                    if v1 == "1":
                        v1 = "3"
                        v2 = "3"
                        new_pos = remplace_string(new_pos,"3",s1)


                temp0,temp1 = "",""
                # Region exterieure
                temp0 = insertion_rapide(temp0,new_pos,s2,len(new_pos))
                temp0 = insertion_rapide(temp0,new_pos,0,s1)
                temp0 += v1 + "6" + Char_End_Boundary #"6" = Child_vtx_3

                # Region intérieure
                temp1 = insertion_rapide(temp1,new_pos,s1,s2)
                temp1 += v2 + "6" + Char_End_Boundary #"6" = Child_vtx_3
                Liste_des_sucesseurs.append((temp0,temp1))

    delimitation += Char_End_Boundary
    return suppr_doublons(Liste_des_sucesseurs)

def rotation_de_1(string):
            out = str(string[-1])
            for i in range(len(string)-1):
                out += string[i]
            return out

def calcul_enfant_type_2(delimitation,Liste_des_sucesseurs):

    if len(delimitation) < 2 :
        print("erreur, la region est vide")
        return

    def rotation_de_1(string):
            out = str(string[-1])
            for i in range(len(string)-1):
                out += string[i]
            return out

    boundary = delimitation[:-1]

    for i in range(len(delimitation)):
        v = boundary[0]

        if v == "0" :
            boundary = remplace_string(boundary,"1",0)
            Liste_des_sucesseurs.append(boundary)
            boundary = remplace_string(boundary,"0",0)
        elif v == "1":
            boundary = remplace_string(boundary,"4",0) #"4" = Child_vtx_1
            boundary += "4"
            Liste_des_sucesseurs.append(boundary)
            boundary = boundary[:-1]
            boundary = remplace_string(boundary,"1",0)
        elif v == "2":
            boundary = remplace_string(boundary,"3",0)
            Liste_des_sucesseurs.append(boundary)
            boundary = remplace_string(boundary,"2",0)
        else :
            boundary += v
            Liste_des_sucesseurs.append(boundary)
            boundary = boundary[:-1]

        boundary = rotation_de_1(boundary)

    return suppr_doublons(Liste_des_sucesseurs)

# ------------------------------------------------------------------
# Fonction utiles pour accélérer la vitesse de computation
# ------------------------------------------------------------------

def Possede_six_zeros(position):
    """Pas encore utilisée, une conjecture stipule que les positions qui sont gagnantes / perdantes en supprimant 6 points (ie 6 zéros) de la position le sont aussi sans les supprimer 
    (fausse dans le cas général mais vraie dans 90% des cas) on pourrait donc imaginer un programme qui les priorise"""
    if len(position) < 13 :
        return False
    s = 0
    for i in range(6):
        if position[s] != 0 :
            return False
        s += 1
        if position[s] != Char_End_Boundary :
            return False
        s += 1
    return True


def Supprime_six_zeros(region):
    """La fonction qui permettrait de supprimer 6 zéros si je décide d'utiliser la conjecture mentionnée au-dessus, on sait que les 0 sont devant par la canonization"""
    reg = region[12:]

    if reg[0] == Char_Empty_Position :
        while reg[0] != Char_End_Region :
            reg = reg[:-1]

    if reg[0] == Char_End_Region :
        reg = reg[:-1]

    return reg


def EstMorte(region):
    """indique si une region est morte (donc s'il y a moins de 2 nodes permettant de connecter), donc très utile pour simplifier des terres"""
    vie = 0
    s_save = 0

    for i in range(len(region)-1):
        if vie < 2 :
            if (est_une_lettre(region[i])) and (region[i] != s_save):
                vie += 1
                s_save = region[i]
            elif (region[i] == "2") or (region[i] == "0") or (region[i] == "1") :
                vie += 3-int(region[i])

    return (vie<2)

# ------------------------------------------------------------------
# Separation et reformations des différentes structures
# ------------------------------------------------------------------

def separation_de_la_region_a_partir_du_dernier_zero(region):
    """prend une region et renvoie une liste des positions à l'intérieur, sans compter tous les "0." a l'avant à part 1"""
    a = time()
    Liste = []
    pos = ""
    for i in range(len(region)-1):
        if region[i] == Char_End_Boundary :
            if len(pos) > 0 :
                pos += Char_End_Boundary
                Liste.append(pos)
                pos = ""
            else :
                pos = ""
        else :
            pos += region[i]
    if pos != "" :
        pos += Char_End_Boundary
        Liste.append(pos)
    if len(Liste) > 1 :
        i = 0
        while i < len(Liste)-1 and Liste[i+1] == "0." :
            i += 1
        Liste = Liste[i:]
    global Duree_sep
    Duree_sep += time() - a
    return Liste

def separation_de_la_region_a_partir_de_lavant_dernier_zero(region):
    """prend une region et renvoie une liste des positions à l'intérieur, sans compter tous les "0." a l'avant à part 2"""
    a = time()
    Liste = []
    pos = ""
    for i in range(len(region)-1):
        if region[i] == Char_End_Boundary :
            if len(pos) > 0 :
                pos += Char_End_Boundary
                Liste.append(pos)
                pos = ""
            else :
                pos = ""
        else :
            pos += region[i]
    if pos != "" :
        pos += Char_End_Boundary
        Liste.append(pos)
    if len(Liste) > 1 :
        i = 0
        while i < len(Liste)-1 and Liste[i+1] == "0." :
            i += 1
        if i == 0 :
            Liste = Liste[i:]
        else :
            Liste = Liste[i-1:]
    global Duree_sep
    Duree_sep += time() - a
    return Liste

def separation_de_la_region(region):
    """prend une region et renvoie une liste des positions à l'intérieur,"""
    Liste = []
    a = time()
    pos = ""
    for i in range(len(region)-1):
        if region[i] == Char_End_Boundary :
            if len(pos) > 0 :
                pos += Char_End_Boundary
                Liste.append(pos)
                pos = ""
            else :
                pos = ""
        else :
            pos += region[i]
    if pos != "" :
        pos += Char_End_Boundary
        Liste.append(pos)
    global Duree_sep
    Duree_sep += time() - a
    return Liste


def separation_de_la_terre(terre):
    """prend une terre et renvoie une liste des regions à l'intérieur,"""
    if terre == '' :
        return []
    a = time()
    terre = terre[:-2]
    Liste = terre.split('|')
    for i in range(len(Liste)):
        Liste[i] += '|'
    global Duree_sep
    Duree_sep += time() - a
    return Liste


def separation_de_la_position(position):
    """prend une position et renvoie une liste des regions à l'intérieur,"""
    Liste = []
    a = time()
    pos = ""
    for i in range(len(position)-1):
        if position[i] == Char_End_Land :
            pos += Char_End_Land
            Liste.append(pos)
            pos = ""
        else :
            pos += position[i]
    if pos != "" :
        pos += Char_End_Land
        Liste.append(pos)
    global Duree_sep
    Duree_sep += time() - a
    return Liste

def recompose_region(Liste_pos):
    """prend une liste de délimitations et la recompose en une region"""
    a = time()
    s = ""
    for ci in Liste_pos :
        s += ci
    if s != "" :
        s += Char_End_Region
    global Duree_sep
    Duree_sep += time() - a
    return s

def recompose_terre(Liste_reg):
    """prend une liste de region et la recompose en une terre"""
    a = time()
    s = ""
    for ci in Liste_reg :
        s += ci
    if s != "" :
        s += Char_End_Land
    global Duree_sep
    Duree_sep += time() - a
    return s

def recompose_position(Liste_terre):
    """prend une liste de region et la recompose en une terre"""
    a = time()
    s = ""
    for ci in Liste_terre :
        s += ci
    if s != "" :
        s += Char_Empty_Position
    global Duree_sep
    Duree_sep += time() - a
    return s

# ------------------------------------------------------------------
# Partie calculs enfants regions
# ------------------------------------------------------------------

def liste_des_partitions(liste_de_positions):

    partitions_possibles = []

    # Si la liste de positions est vide, la seule partition possible est ("","")
    if liste_de_positions ==  [] :
        partitions_possibles.append(("",""))
        return partitions_possibles


    Liste_des_positions_normales = [] #Liste des postions qui ne sont pas des simples points

    partitions_nulles = [] #Liste des partitions qui n'ont que des simples points
    partitions_normales = [] #Liste des partitions de positions normales

    #Etape 1 : On compte et enlève les positions "0."

    n = 0
    for bj in liste_de_positions :
        if bj == "0." :
            n += 1
        else :
            Liste_des_positions_normales.append(bj)

    #Etape 2 : On fait les partitions avec les 0. (il y en a n+1 possibles)

    if n != 0 :
        r2 = ""
        r1 = ""
        for i in range(n):
            r2 += "0."
        partitions_nulles.append((r1,r2))
        for i in range(n):
            r1 += "0."
            r2 = r2[:-2]
            partitions_nulles.append((r1,r2))


    #Etape 3 : On fait les partitions normales

    n = len(Liste_des_positions_normales)

    if n != 0 :
        q = 2**n
        for i in range(q):
            r1 = ""
            r2 = ""

            for j in range(n):
                #Ce test est un peu bizarre, c'est normal, il faut réfléchir un peu pour comprendre : On veut toutes les combinaisons donc on se sert des valeurs en bits pour le faire
                if (i & (2 ** j)) == (2 ** j):
                    r1 += Liste_des_positions_normales[j]
                else :
                    r2 += Liste_des_positions_normales[j]

            partitions_normales.append((r1,r2))


    #Etape 4 on complete l'ensemble des partitions

    if partitions_nulles == []:
        partitions_possibles = partitions_normales
        return partitions_possibles

    if partitions_normales == [] :
        partitions_possibles = partitions_nulles
        return partitions_possibles

    for ci in partitions_nulles :
        for cj in partitions_normales :
            r1 = ""
            r1 += ci[0]
            r1 += cj[0]
            r2 = ""
            r2 += ci[1]
            r2 += cj[1]

            partitions_possibles.append((r1,r2))

    return partitions_possibles


def Est_de_degre_2_region(lettre,region):
    compteur = 0
    if lettre != "0" and lettre != "1" and lettre != "2" :
        for i in region :
            if i == lettre :
                compteur += 1
    return (compteur == 2)

def Est_de_degre_2_position(lettre,position):
    compteur = 0
    if lettre != "0" and lettre != "1" and lettre != "2" :
        for i in position :
            if i == lettre :
                compteur += 1
    return (compteur == 2)

def Est_de_degre_1_position(lettre,position):
    compteur = 0
    if lettre != "0" and lettre != "1" and lettre != "2" :
        for i in position :
            if i == lettre :
                compteur += 1
    return (compteur == 1)

def Liste_des_temporaire_de_degre_2(position):
    """fonction utilisée bien plus (renome_dans_lordre) haut quels temporels sont présents dans une position"""
    #RQ : Fonctionne aussi pour les regions
    liste = [0,0,0] # premier indice pour "4", deuxième pour "5", troisième pour "6"
    for i in position :
        if i == "4" :
            liste[0] += 1
        elif i == "5" :
            liste[1] += 1
        elif i == "6" :
            liste[2] += 1
    A_remplacer = []
    for i in range(len(liste)) :
        if liste[i] == 2 or liste[i] == 1:
            if i == 0 :
                A_remplacer.append("4")
            if i == 1 :
                A_remplacer.append("5")
            if i == 2 :
                A_remplacer.append("6")
    return A_remplacer


def calcul_enfant_type_1_region(region,Liste_des_sucesseurs_region):
    """type de coup 1 : relier un boundary à lui-même"""
    Liste_des_sous_positions = separation_de_la_region_a_partir_du_dernier_zero(region)

    Sep = separation_de_la_region(region)
    for bi in Liste_des_sous_positions :
        Liste_des_sucesseurs = calcul_enfant_type_1(bi,[])
        # On crée une liste de positions non utilisées
        position_non_utilisee = []
        compteur = 0
        for bk in Sep :
            if bi != bk :
                position_non_utilisee.append(bk)
            else :
                compteur += 1
        for i in range(compteur-1):
            position_non_utilisee.append(bi)
        # On crée la partition de ces positions non utilisées
        partition = liste_des_partitions(position_non_utilisee)
        for ci in Liste_des_sucesseurs:
            for Rj in partition :
                enfant = ""
                enfant += ci[0]
                enfant += Rj[0]
                enfant += Char_End_Region
##                print(enfant)
                enfant += ci[1]
                enfant += Rj[1]
                enfant += Char_End_Region
##                print(enfant)
                Liste_des_sucesseurs_region.append(enfant)

    return Liste_des_sucesseurs_region


def  calcul_enfant_type_2_region(region,Liste_des_sucesseurs_region):
    """type de coup 2 : lier deux boundary entre-eux"""
    Liste_des_sous_positions = separation_de_la_region_a_partir_de_lavant_dernier_zero(region)
    n = len(Liste_des_sous_positions)
    Liste_des_postions_a_linterrieur = separation_de_la_region(region)
    k = len(Liste_des_postions_a_linterrieur)
    decalage = k-n
    Liste_des_sucesseurs_i = []

    #On calcule d'abord les successeurs de chaque boundary comprises dans la region, et on les stock à l'indice i de la Liste_des_sous_positions
    #Donc a Liste_des_sous_positions[i] on a une liste de tous les enfants de bi

    for i in range(len(Liste_des_sous_positions)) :
        bi = Liste_des_sous_positions[i]
        Liste_des_sucesseurs_i.append([])
        Liste_des_sucesseurs_i[i] = calcul_enfant_type_2(bi, Liste_des_sucesseurs_i[i])

    for i in range(len(Liste_des_sous_positions)):
        for j in range(i+1, len(Liste_des_sous_positions)) :
            #On va s'occuper des liens entre bi et bj
            position_non_utilisee = []

            #On crée la liste des toutes les positions qui ne sont pas bi ou bj
            for k in range(len(Liste_des_postions_a_linterrieur)) :
                if (k != i+decalage) and (k != j+decalage) :
                    position_non_utilisee.append(Liste_des_postions_a_linterrieur[k])

            #Double loop sur les enfants de bi et bj
            for ci in Liste_des_sucesseurs_i[i]:
                for cj in Liste_des_sucesseurs_i[j]:
                    #Si ci et cj ne sont pas vide, ils est positble qu'ils utilisent tout les deux Child_vtx_1 (le vecteur provisoire qui disparait au moment de la canonisation), dans ce cas là
                    #On remplace le Child_vtx_1 de cj par Child_vtx_2 (="5")
                    if not((ci == "")) and not((cj == "")) :
                        if ci[0] == "4" and cj[0] == "4" :
                            cj = remplace_string(cj,"5",0)
                            cj = remplace_string(cj,"5",len(cj)-1)

                    lim = 1

                    #Si les deux region ont un point de degré 2, alors on n'a pas à traiter le cas ou l'on relie ce point à lui-même car l'enfant aurait un point de degré 4 (absurde)
                    if not((ci == "")) and not((cj == "")) :
                        if (Est_de_degre_2_region(ci[0],region) and Est_de_degre_2_region(cj[0],region)) and ci[0] == cj[0] :
                            lim = 0


                    for i in range(0,lim):
                        enfant = ""
                        enfant += ci
                        enfant += "6"
                        enfant += cj
                        enfant += "6"
                        enfant += Char_End_Boundary

                        for pos_inut in position_non_utilisee : #On ajoute les positions non utilisées à l'enfant
                            enfant += pos_inut

                        enfant += Char_End_Region #On ajoute enfin le caractère de fin de region
                        Liste_des_sucesseurs_region.append(enfant)

    return Liste_des_sucesseurs_region

def calcul_enfant_region(region):
    """calcul les enfants d'une region, via les deux types de coups"""
    Liste_des_sucesseurs_region = []
    Liste_des_sucesseurs_region = calcul_enfant_type_1_region(region,Liste_des_sucesseurs_region)
    Liste_des_sucesseurs_region = calcul_enfant_type_2_region(region,Liste_des_sucesseurs_region)
    return Liste_des_sucesseurs_region

# ------------------------------------------------------------------
# Partie canonization
# ------------------------------------------------------------------



def simple_tri_region(region):
    """tri simplement une region (sans prendre en compte le retournement de l'orientation)"""
    Sep = separation_de_la_region(region)
    for i in range(len(Sep)) :
        Sep[i] = position_tri_permut(Sep[i])
    Sep.sort()
    new_region =""
    for bi in Sep :
        new_region += bi
    new_region += Char_End_Region
    return new_region


def tri_region(region):
    """tri une region (algorythme "complexe" (MDR) impliquant des permutations)"""
    region = simple_tri_region(region)
    region_sav = region
    Sep = separation_de_la_region(region)
    for i in range(len(Sep)) :
        Sep[i] = position_retourne(Sep[i])
    region = ""
    for bi in Sep :
        region += bi
    region += Char_End_Region
    region = simple_tri_region(region)
    if ordreligne(region_sav,region) :
        return region_sav
    return region

def tri_terre(terre):
    """Trie une terre en triant d'abord les régions à l'intérieur puis en triant ces régions"""

    Sep = [tri_region(region) for region in separation_de_la_terre(terre)]
    Sep.sort()
    new_terre = "".join(Sep)
    if new_terre != "" :
        new_terre += Char_End_Land

    return new_terre

def tri_position(position):
    """tri une position, pour cela trie les terre à l'intérieur puis sort ces terres selon la priorité du moins d'enfants"""
    Sep = separation_de_la_position(position)
    for i in range(len(Sep)) :
        Sep[i] = tri_terre(Sep[i])
    Sep = tri_selon_priorites(Sep)
    new_pos =""
    for bi in Sep :
        new_pos += bi
    if new_pos!= "" :
        new_pos += Char_Empty_Position
    return new_pos

def Liste_devient_terre(Liste):
    """transforme une liste de regions en une terre"""
    for i in range(len(Liste)) :
        Liste[i] = Liste[i] + Char_End_Land
    return Liste

##def tri_supprime(Liste_de_terres):
##    """Tri toutes les terres d'une liste selon OrdreLigne (voir au tout début), et supprime les doublons"""
##    Liste_appres_tri = []
##    for i in range(len(Liste_de_terres)):
##        ci = tri_terre(Liste_de_terres[i])
##        if not(ci in Liste_appres_tri):
##            Liste_appres_tri.append(ci)
##    return Liste_appres_tri

def tri_supprime(Liste_de_terres):
    """Tri toutes les terres d'une liste selon OrdreLigne (voir au tout début), et supprime les doublons"""
    Liste_appres_tri = set(tri_terre(terre) for terre in Liste_de_terres)
    return list(Liste_appres_tri)


def tri_supprime_position(Liste_des_positions):
    """Tri toutes les positions d'une liste selon OrdreLigne (voir au tout début), et supprime les doublons"""
    Liste_appres_tri = []
    for i in range(len(Liste_des_positions)):
        ci = tri_position(Liste_des_positions[i][0])
        if not(ci in Liste_appres_tri):
            Liste_appres_tri.append(ci)
    return Liste_appres_tri

def est_temporaire(point):
    """Regarde si un vecteur est temporaire, ie si c'est "4" our "5" our "6" """
    if point == Child_vtx_1 or point == Child_vtx_2 or point == Child_vtx_3 :
        return True
    return False

def renome_dans_lordre_liste(Liste_de_terres,n):
    """renome tous les vecteurs temporaires d'une liste de terres"""
    for i in range(len(Liste_de_terres)):
        Liste_de_terres[i] = renome_dans_lordre(Liste_de_terres[i],n)
    return Liste_de_terres

def renome_dans_lordre(terre,n):
    """renome les vecteur temporaires d'une terre et les vecteurs residuels afin de conserver les bons noms (hardcore à comprendre désolé)
    Cette fonction n'est plus utilisée car j'ai trouvé plus efficace..."""
    nouveaux_noms = []
    for i in range(124):
        nouveaux_noms.append(0) #On crée une liste avec des zéros pour indiquer quels termes ont été pris

    lettres_presentes = []
    if n == 0 or n == 1 :
        prochaine_lettre = 97
    if n == 2 :
        prochaine_lettre = 65

    TEST_BUG = 0
    for i in terre :
        if est_une_lettre(i) :
            if nouveaux_noms[ord(i)] == 0 :
                lettres_presentes.append(i)
            nouveaux_noms[ord(i)] += 1

    lettres_utilisable = []
    for i in range(26):
        new = chr(i+prochaine_lettre)
        if not(new in lettres_presentes):
            lettres_utilisable.append(new)
    prochaine_lettre = 0
    if n == 0 or n == 1 :
        if prochaine_lettre > len(lettres_utilisable) :
            print("ATTENTION OVERFLOW DES MINUSCULES")
    if n == 2 :
        if prochaine_lettre > len(lettres_utilisable) :
            print("ATTENTION OVERFLOW DES MAJUSCULES")
    if n == 1 :
        Sep = separation_de_la_terre(terre)
        for i in range(len(Sep)) :
            bi = Sep[i]
            Sep_bi = separation_de_la_region(bi)
            for j in range(len(Sep_bi)) :
                ci = Sep_bi[j]
                Liste = Liste_des_temporaire_de_degre_2(ci) #on récupère les temporaires à remplacer, s'il y en a, on note ce par quoi on doit les remplacer
                print(Liste)
                new_vector = []
                for k in range(len(Liste)):
                    new_vector.append(lettres_utilisable[prochaine_lettre])
                    prochaine_lettre += 1
                Liste.append('`')
                Liste.append('`')
                Liste.append('`')
                new_ci = ''
                for s in ci:
                    if s == Liste[0] :
                        new_ci += (new_vector[0])
                    elif s == Liste[1] :
                        new_ci += (new_vector[1])
                    elif s == Liste[2] :
                        new_ci += (new_vector[2])
                    else :
                        if est_une_lettre(s) and (nouveaux_noms[ord(s)] != 3) :
                            new_ci += s
                        elif not(est_une_lettre(s)) :
                            new_ci += s
                    if nouveaux_noms[ord(s) > 3] :
                        TEST_BUG = 1
                    Sep_bi[j] = new_ci
            Sep[i] = recompose_region(Sep_bi)
        new_terre = recompose_terre(Sep)

    elif n == 2 :
        Liste = Liste_des_temporaire_de_degre_2(terre)
        new_vector = []
        for k in range(len(Liste)):
            new_vector.append(lettres_utilisable[prochaine_lettre])
            prochaine_lettre += 1
        Liste.append('`')
        Liste.append('`')
        Liste.append('`')
        new_terre = ''
        for s in terre:
            if s == Liste[0] :
                new_terre += (new_vector[0])
            elif s == Liste[1] :
                new_terre += (new_vector[1])
            elif s == Liste[2] :
                new_terre += (new_vector[2])
            else :
                if est_une_lettre(s) and not(nouveaux_noms[ord(s)] == 3) :
                    new_terre += s
                elif s == "3" :
                    pass
                elif not(est_une_lettre(s)) :
                    new_terre += s
                if nouveaux_noms[ord(s) > 3] :
                    TEST_BUG = 1
    if TEST_BUG == 1 :
        print("Test_bug")
        return ""
    else :
        return new_terre

def liste_des_presente_3_fois(pos):
    global present_3_fois
    a = time()
    L = []
    for i in pos:
        (x,y) = (i,pos.count(i))
        if not((x,y) in L) and est_une_lettre(i) and y == 3 :
            L.append(x)
    present_3_fois += time() - a
    return L

def transforme_sous_forme_simple(terre):
    Sep = separation_de_la_terre(terre)
    Liste_des_lettres_maj = []
    Liste_des_lettres_min = []
    Liste_des_lettres = []
    Liste_des_presente3fois = liste_des_presente_3_fois(terre)
    for k in terre :
        if not((k,0) in Liste_des_lettres) and not(k in Liste_des_presente3fois) and (est_une_lettre(k) or est_temporaire(k)) :
            Liste_des_lettres.append((k,0))
    for ck in Sep :
        for j in range(len(Liste_des_lettres)):
            if Liste_des_lettres[j][0] in ck :
               Liste_des_lettres[j] = (Liste_des_lettres[j][0],Liste_des_lettres[j][1] + 1)
    for k in Liste_des_lettres :
        if k[1] == 1 :
            Liste_des_lettres_min.append(k[0])
        elif k[1] > 1 :
            Liste_des_lettres_maj.append(k[0])
    #Liste_des_lettres_maj.sort() : Je sortais à un moment mais en fait c'est stupide, ça ne servait à rien et ça ralentissait le programme pour 2 raisons différentes
    #Liste_des_lettres_min.sort()
    New_maj = []
    New_min = []
    for k in range(len(Liste_des_lettres_maj)):
        New_maj.append(chr(65+k))
    for k in range(len(Liste_des_lettres_min)):
        New_min.append(chr(97+k))
    new_terre = ""
    for s in terre :
        for j in range(len(Liste_des_lettres_maj)):
            if s == Liste_des_lettres_maj[j] :
                new_terre += New_maj[j]
        for j in range(len(Liste_des_lettres_min)):
            if s == Liste_des_lettres_min[j] :
                new_terre += New_min[j]
        if not(est_une_lettre(s) or est_temporaire(s) or s == "3" or s in Liste_des_presente3fois):
            new_terre += s
    return new_terre



def transforme_sous_forme_simple_version_simple(terre):
    Sep = separation_de_la_terre(terre)
    Liste_des_lettres_maj = []
    Liste_des_lettres_min = []
    Liste_des_lettres = []
    for k in terre :
        if not((k,0) in Liste_des_lettres) and (est_une_lettre(k) or est_temporaire(k)) :
            Liste_des_lettres.append((k,0))
    for ck in Sep :
        for j in range(len(Liste_des_lettres)):
            if Liste_des_lettres[j][0] in ck :
               Liste_des_lettres[j] = (Liste_des_lettres[j][0],Liste_des_lettres[j][1] + 1)
    for k in Liste_des_lettres :
        if k[1] == 1 :
            Liste_des_lettres_min.append(k[0])
        elif k[1] > 1 :
            Liste_des_lettres_maj.append(k[0])
##    Liste_des_lettres_maj.sort() : Je sortais à un moment mais en fait c'est stupide, ça ne servait à rien et ça ralentissait le programme pour 2 raisons différentes
##    Liste_des_lettres_min.sort()
    New_maj = []
    New_min = []
    for k in range(len(Liste_des_lettres_maj)):
        New_maj.append(chr(65+k))
    for k in range(len(Liste_des_lettres_min)):
        New_min.append(chr(97+k))
    new_terre = ""
    for s in terre :
        for j in range(len(Liste_des_lettres_maj)):
            if s == Liste_des_lettres_maj[j] :
                new_terre += New_maj[j]
        for j in range(len(Liste_des_lettres_min)):
            if s == Liste_des_lettres_min[j] :
                new_terre += New_min[j]
        if not(est_une_lettre(s) or est_temporaire(s)):
            new_terre += s
    return new_terre

def transforme_sous_forme_simple_version_simple_liste(Liste_de_terres):
    for i in range(len(Liste_de_terres)):
        Liste_de_terres[i] = transforme_sous_forme_simple_version_simple(Liste_de_terres[i])
    return Liste_de_terres

def transforme_sous_forme_simple_liste(Liste_de_terres):
    for i in range(len(Liste_de_terres)):
        Liste_de_terres[i] = transforme_sous_forme_simple(Liste_de_terres[i])
    return Liste_de_terres

def canonize_liste_terres(terre,Liste_de_terres):
    """c'est dans le nom"""

    global Duree_suppr_mort
    global Duree_transfo_simple
    global Duree_transfo_simple_simple
    global Duree_tri_sup
    global Duree_tri_prio
    global Duree_compa_pere_fils
    a = time()
##    b = time()
##    Liste_de_terres = tri_supprime(Liste_de_terres) # On trie les regions selon le pseudo ordre, puis on supprime les doublons
##    Duree_tri_sup += time() - b

    ###On remplace les vecteurs temporaires dans les 1-boundary et 2-boundary
    #b = time()
    #Liste_de_terres = renome_dans_lordre_liste(Liste_de_terres,2) #On remplace les vecteurs temporaires dans les 2-
    #Duree_renom += time() - b
    b = time()
    Liste_de_terres = transforme_sous_forme_simple_liste(Liste_de_terres)
    Duree_transfo_simple += time() - b
    b = time()
    Liste_de_terres = supprime_les_morts_Liste(Liste_de_terres) #On supprimes les regions mortes (donc celle dans lequelles on ne peut plus jouer de coups)
    Duree_suppr_mort += time() - b
    #Plus utilisé car à l'origine de bugs..
    #Liste_de_terres = renome_dans_lordre_liste(Liste_de_terres,1)
    # On trie de les regions selon le pseudo ordre car la suppression des regions mortes peut de nouveau créer des doublons
    b = time()
    Liste_de_terres = tri_supprime(Liste_de_terres)
    Duree_tri_sup += time() - b
    ###
    b = time()
    Liste_de_terres = transforme_sous_forme_simple_version_simple_liste(Liste_de_terres)
    Duree_transfo_simple_simple += time() - b
    Liste_de_terres = ajoute_les_2_terre_liste(Liste_de_terres)
    ### Critères pour améliorer la vitesse de la computation
    b = time()
    Liste_de_terres = tri_selon_priorites(Liste_de_terres) # On teste d'abord les coups qui mènent à des positions où il y a moins de coups possibles
    ### Ajouter : tri selon le degré
    Duree_tri_prio += time() - b
    b = time()
    ###La théorie stipule que tous les enfants valides ont un degré plus faible, donc pas de risque de supprimer de bons enfants, c'est une sécurité si on crée de mauvais enfants et assure la terminaison
    Liste_de_terres,Liste_des_deg = comparaison_pere_fils_liste(terre,Liste_de_terres)
    Duree_compa_pere_fils += time() - b
    global Duree_can
    Duree_can += time()-a
    return Liste_de_terres,Liste_des_deg

#def canonize_liste_positions(liste_pos):
    #"""les positions sont des couples ('position',[liste des deg des terres dans la position])"""
    #liste_pos = canonize_les_terres_liste(liste_pos)

def ajoute_les_2_terre(terre):
    new_terre = ''
    if terre == '' :
        return ''
    dernier = terre[0]
    for i in range(1,len(terre)) :
        if dernier == terre[i] and est_minuscule(dernier) and est_minuscule(terre[i]):
            new_terre += '2'
            dernier = ''
        else :
            new_terre += dernier
            dernier = terre[i]
    new_terre += Char_End_Land
    return new_terre
        
def ajoute_les_2_terre_liste(Liste_de_terres):
    """ajoute tous les 2 dans les vecteurs temporaires d'une liste de terres"""
    for i in range(len(Liste_de_terres)):
        Liste_de_terres[i] = ajoute_les_2_terre(Liste_de_terres[i])
    return Liste_de_terres

def supprime_les_morts(terre):
    """Supprime les regions mortes présentes dans une terre"""
    Sep = separation_de_la_terre(terre)
    Stock = []
    for i in range(len(Sep)) :
        ci = Sep[i]
        if EstMorte(ci) :
            for k in ci :
                if est_une_lettre(k) :
                    Stock.append(k)
            Sep[i] = ""
        elif nombre_de_vie_region(ci) <= 3 :
            new_reg = ''
            Sep_i = separation_de_la_region(ci)
            for di in Sep_i :
                new_reg += di[:-1]
            new_reg += Char_End_Boundary
            new_reg += Char_End_Region
            Sep[i] = new_reg   
    terre = recompose_terre(Sep)
    new_terre = ""
    for i in range(len(terre)-1):
        if terre[i] in Stock :
            new_terre += "2"
        else :
            new_terre += terre[i]
    if new_terre != "" :
        new_terre += Char_End_Land
    return new_terre

    return

def supprime_les_morts_Liste(Liste_de_terre):
    """renvoie une liste sans les terres mortes à l'interieur (une terre morte est une terre dans laquelle on ne peut plus jouer de coups"""
    for i in range(len(Liste_de_terre)) :
        Liste_de_terre[i] = supprime_les_morts(Liste_de_terre[i])
    return Liste_de_terre


def calcul_enfant_terre(terre):
    """Calcule les enfants d'une terre"""
    a = time()
    Liste_enfants = []
    Sep = separation_de_la_terre(terre)
    for i in range(len(Sep)) :
        it = Sep[i]
        It_Enfants = calcul_enfant_region(it)
        region_non_utilisee = []
        for j in range(len(Sep)) :
            if j != i :
                region_non_utilisee.append(Sep[j])
        for it_children in It_Enfants :
            Enfant = ""
            for cj in region_non_utilisee :
                Enfant += cj
            Enfant += it_children
            Enfant += Char_End_Land
            Liste_enfants.append(Enfant)
##    print(Liste_enfants)
    global Duree_cal_enfant
    Duree_cal_enfant += time()-a
    return Liste_enfants


def calcule_enfants_A_Z(position):
    """cette fonction n'est appellée que sur des terres, 
    on peut donc gagner pas mal de temps"""
    position = position[:-1]
    Liste,_ = calcul_et_canonize_terre(position)
    a = time()
    Enfants = []
    for i in range(len(Liste)) :
        Enfants.append(split(Liste[i]))
    Enfants = tri_selon_nbr_enfants_Liste(Enfants)
    Deg = []
    for i in range(len(Enfants)):
        Sep_i = separation_de_la_position(Enfants[i])
        Deg.append([])
        for j in range(len(Sep_i)):
            Deg[i].append(nombre_de_vie_terre(Sep_i[j]))
            
    global Duree_cal_enfant
    Duree_cal_enfant += time()-a
    return Enfants,Deg


def lier(terre1,terre2):
    """teste si deux terres sont liées, c'est à dire si elle ont un 2-region vertex commun"""
    for i in terre1 :
        if est_une_lettre(i) or est_temporaire(i):
            for j in terre2 :
                if i == j :
                    return True
    return False


def split(terre):
    indep_terre = []
    vertex_liee = ""
    sep = separation_de_la_terre(terre)
    for Ri in sep :
        new_land = True
        vertex_liee = ""
        indep_terre_relatif = [] #liste des terres indépendantes à Ri
        for Lj in indep_terre :
            if lier(Ri,Lj) :
                new_land = False
                vertex_liee += Lj
            else :
                indep_terre_relatif.append(Lj)
        if new_land :
            indep_terre_relatif.append(Ri)
        else :
            vertex_liee += Ri
        indep_terre = indep_terre_relatif
        if not(len(vertex_liee) == 0) :
            indep_terre.append(vertex_liee)

    n =len(indep_terre)
    for j in range(n) :
        indep_terre[j] = indep_terre[j] + Char_End_Land

    if n>1 :
        new_pos = ""
        for Lj in indep_terre :
            new_pos += transforme_sous_forme_simple_version_simple(Lj)
        return new_pos
    else :
        return terre

def nombre_de_vie_terre(terre):
    """renvoie le nombre de vie d'une terre (chaque chiffre à 3-n vie et chaque lettre a 1 vie au max (toutes apparitions comprises)"""
    a = time()
    total = 0
    lettres = 0
    for s in terre :
        if est_une_lettre(s):
            lettres += 1
        elif s == "0" or s == "1" or s == "2" :
            total += 3-int(s)
    total += lettres//2

    global Duree_nbr_vie
    Duree_nbr_vie += time()-a
    return total

def nombre_de_vie_region(reg):
    a = time()
    total = 0
    lettres = []
    for s in reg :
        if est_une_lettre(s) :
            if not (s in lettres) :
                lettres.append(s)
        elif s == "0" or s == "1" or s == "2" :
            total += 3-int(s)
    total += len(lettres)
    global Duree_nbr_vie
    Duree_nbr_vie += time()-a
    return total

def comparaison_pere_fils_liste(terre_pere,liste_terre_fils):
    """Compare un fils et ses enfants, si le fils a plus de vie que le père, on le supprime (permet de corriger un problème MAJEUR)"""
    nbr_vie_pere = nombre_de_vie_terre(terre_pere)
    Liste_des_deg = []
    for i in range(len(liste_terre_fils)) :
        ci = liste_terre_fils[i]
        val = nombre_de_vie_terre(ci)
        if val >= nbr_vie_pere :
            liste_terre_fils[i] = "rate"
        else :
            Liste_des_deg.append(val)
    new_list = []
    for ci in liste_terre_fils :
        if ci != "rate" :
            new_list.append(ci)
    return (new_list,Liste_des_deg)

def estime_nombre_enfants_region(region):
    estimation = 0
    Sep = separation_de_la_region(region)
    for i in range(len(Sep)):
        for j in range(i+1,len(Sep)):
            estimation+=(len(Sep[i])-1)*(len(Sep[j])-1)
    if region == '0.|' :
        return 2
    if region == '0.0.|':
        return 3
    if region != "" :
        for Bi in Sep :
            number = len(Bi)-1
            estimation += number*number//2
    return estimation

def estime_nombre_enfants_terre(terre):
    Sep = separation_de_la_terre(terre)
    total = 0
    for ci in Sep :
        total += estime_nombre_enfants_region(ci)
    return total

def tri_selon_nbr_enfants_Liste(Liste_de_pos):
    """trie les terres dans une positions et les positions afin de traiter la plus simple d'abord"""
    L = []
    for k in Liste_de_pos :
        new_k = tri_selon_nbr_enfants(k)
        L.append(new_k)
    L = tri_selon_priorites_pos(L)
    return L

def tri_selon_nbr_enfants(position):
    """trie les terres dans une positions afin de traiter la plus simple d'abord"""
    Sep = separation_de_la_position(position)
    Sep = tri_selon_priorites(Sep)
    return recompose_position(Sep)

def tri_selon_priorites_pos(Liste_de_pos):
    Liste_estime = []
    #On admet une valeur d'importance pour les priorités : d'abord le moins de zéro puis le moins d'enfants
    Liste_estime = priorité_nbr_enfants_pos(Liste_de_pos,Liste_estime)
    #Liste_estime = priorité_nbr_zeros(Liste_de_pos,Liste_estime)


    Liste_estime.sort(key=lambda x: x[1])
    New_liste_terre = []
    for k in range(len(Liste_estime)):
        New_liste_terre.append(Liste_de_pos[Liste_estime[k][0]])
    return New_liste_terre

def tri_selon_priorites(Liste_de_terres):
    Liste_estime = []
    for i in range(len(Liste_de_terres)) :
        Liste_estime.append((0,i))

    #On admet une valeur d'importance pour les priorités : d'abord le moins de zéro puis le moins d'enfants
    Liste_estime = priorité_nbr_enfants(Liste_de_terres,Liste_estime)
    #Liste_estime = priorité_nbr_zeros(Liste_de_terres,Liste_estime)


    Liste_estime.sort(key=lambda x: x[0])
    New_liste_terre = []
    for k in range(len(Liste_estime)):
        New_liste_terre.append(Liste_de_terres[Liste_estime[k][1]])
    return New_liste_terre

def priorité_nbr_enfants(Liste_de_terres,Liste_estime):
    Liste_estime_2 = []
    for i in range(len(Liste_de_terres)) :
        Liste_estime_2.append((estime_nombre_enfants_terre(Liste_de_terres[i]),i))
    Liste_estime_2.sort(key=lambda x: x[0])
    val = 0
    for k in range(len(Liste_estime_2)):
        for j in range(len(Liste_estime)):
            if Liste_estime_2[k][1] == Liste_estime[j][1] :
                if Liste_estime_2[k][0] > val :
                    val += 1
                Liste_estime[j] = (val,Liste_estime[j][1])
    return Liste_estime

def priorité_nbr_enfants_pos(Liste_de_pos,Liste_estime):
    for i in range(len(Liste_de_pos)) :
        sep_i = separation_de_la_position(Liste_de_pos[i])
        if sep_i != [] :
            Liste_estime.append((i,estime_nombre_enfants_terre(sep_i[0])))
        else :
            Liste_estime.append((i,0))
        for j in range(1,len(sep_i)):
            Liste_estime[i] = (Liste_estime[i][0], Liste_estime[i][1]*estime_nombre_enfants_terre(sep_i[j]) )

    return Liste_estime

def nombre_de_zeros(terre):
    n = 0
    for k in terre :
        if k == '0' :
            n += 1
        else :
            break
    return n

def priorité_nbr_zeros(Liste_de_terres,Liste_estime):
    Liste_estime_2 = []
    for i in range(len(Liste_de_terres)) :
        Liste_estime_2.append((nombre_de_zeros(Liste_de_terres[i]),i))
    Liste_estime_2.sort(key=lambda x: x[0])
    val = 0
    for k in range(len(Liste_estime_2)):
        for j in range(len(Liste_estime)):
            if Liste_estime_2[k][1] == Liste_estime[j][1] :
                if Liste_estime_2[k][0] > val :
                    val += 1
                Liste_estime[j] = (int((val)**1.5),Liste_estime[j][1])
    return Liste_estime

# ------------------------------------------------------------------
# Partie computation
# ------------------------------------------------------------------

def calcul_victoire_defaite(terre):
    """Donne si une position est gagnante ou perdante"""
    if terre == "" :
        return "Lose"
    Liste,_ = canonize_liste_terres(terre,calcul_enfant_terre(terre))
    if Liste == [''] or Liste == [] :
        return "Win"
    print(Liste, " <-- Liste des enfants")
    for ci in Liste :
        print(ci, "<-- Enfant étudié")
        if calcul_victoire_defaite(ci) == "Lose" :
            print("Win")
            return "Win"
    print("Lose")
    return "Lose"

def calcul_victoire_defaite_misere(terre):
    """Donne si une position est gagnante ou perdante(+ misere version)"""
    if terre == "" :
        return "Win"
    Liste,_ = canonize_liste_terres(terre,calcul_enfant_terre(terre))
    if Liste == [''] or Liste == [] :
        return "Lose"
    print(Liste, " <-- Liste des enfants")
    for ci in Liste :
        print(ci, "<-- Enfant étudié")
        if calcul_victoire_defaite_misere(ci) == "Lose" :
            print("Win")
            return "Win"
    print("Lose")
    return "Lose"

def calcul_victoire_defaite_sans_print(terre):
    """le programme est un peu plus plus rapide sans les prints, donc en dehors des tests, on utilise cette fonction"""
    if terre == "" :
        return "Lose"
    Liste,_ = canonize_liste_terres(terre,calcul_enfant_terre(terre))
    if Liste == [''] or Liste == [] :
        return "Win"
    for ci in Liste :
        if calcul_victoire_defaite_sans_print(ci) == "Lose" :
            return "Win"
    return "Lose"

def calcul_victoire_defaite_misere_sans_print(terre):
    """le programme est un peu plus rapide sans les prints, donc en dehors des tests, on utilise cette fonction (+ misere version)"""
    if terre == "" :
        return "Win"
    Liste,_ = canonize_liste_terres(terre,calcul_enfant_terre(terre))
    if Liste == [''] or Liste == [] :
        return "Lose"
    for ci in Liste :
        if calcul_victoire_defaite_misere_sans_print(ci) == "Lose" :
            return "Win"
    return "Lose"


# ------------------------------------------------------------------
# Partie gestion de fichier et computation avec fichier
# ------------------------------------------------------------------

from time import time
#from random import randint

def ecrire_info(n,terre):
    a = time()
    with open(nom_fichier_n+str(n)+".txt",'a') as f:
        f.write(terre+"\n")
        f.close()
    global Duree_recherche
    Duree_recherche += time()-a

def test_pb_degre(n):
    with open(r"C:\Users\Fantôme\OneDrive\Bureau\TIPE\TIPE2\DATA\Max_Deg.txt",'r') as f:
        lines = f.readline()
        val = int(lines)
        f.close()
    if val <= n :
        for k in range(val,n+1):
            ecrire_info(k,"|Création du doc|")
        with open(r"C:\Users\Fantôme\OneDrive\Bureau\TIPE\TIPE2\DATA\Max_deg.txt",'w') as f:
            f.writelines([str(n+1)])
            f.close()

def presence(n,terre):
    a = time()
    with open(nom_fichier_n+str(n)+".txt",'r') as f:
        lines = f.readlines()
        terre += "\n"
        global Duree_recherche
        if terre in lines :
            f.close()
            global Duree_recherche
            return True
        Duree_recherche += time()-a
        f.close()
        return False

compte2 = 0

def calcul_victoire_defaite_sans_print_stock(terre):
    """le programme est plus plus rapide sans les prints et avec le stock
     donc en dehors des tests, on utilise cette fonction"""
    #global compte
    #global compte2
    #compte += 1
    #print(terre)
    if terre == "" :
        return "Lose"
    Liste,Liste_des_deg = canonize_liste_terres(terre,calcul_enfant_terre(terre))
    #print(Liste,Liste_des_deg)
    if Liste == [''] or Liste == [] :
        return "Win"
    for i in range(len(Liste)):
        if presence(Liste_des_deg[i],Liste[i]):
            #compte2 += 1
            return "Win"
    for i in range(len(Liste)):
        ci = Liste[i]
        if calcul_victoire_defaite_sans_print_stock(ci) == "Lose" :
            ecrire_info(Liste_des_deg[i],ci)
            return "Win"
    return "Lose"

def test_du_temps(f,terre):
    """Permet de tester le temps que prend n'importe quelle fonction de terre"""
    a = time()
    print(f(terre),"<- Résultat final")
    return (time()-a)

def test_du_temps_stock(f,terre):
    """Permet de tester le temps que prend n'importe quelle fonction de terre"""
    a = time()
    b = f(terre)
    return (b,(time()-a))

import os

def supprime_fichier():
    n = 0
    while os.path.exists(nom_fichier_n+str(n)+".txt") :
        os.remove(nom_fichier_n+str(n)+".txt")
        n += 1
    with open(r"C:\Users\Fantôme\OneDrive\Bureau\TIPE\TIPE2\DATA\Max_deg.txt",'w') as f:
            f.writelines(["0"])


def old_reset_fichier():
    with open(r"C:\Users\Fantôme\OneDrive\Bureau\TIPE\TIPE2\DATA\Max_Deg.txt",'r') as f:
        lines = f.readline()
        n = int(lines)
        f.close()
    supprime_fichier()
    test_pb_degre(n-1)

def reset_val():
    global Duree_can
    global Duree_suppr_mort
    global Duree_transfo_simple
    global Duree_transfo_simple_simple
    global Duree_tri_sup
    global Duree_tri_prio
    global present_3_fois
    global Duree_compa_pere_fils
    global Duree_sep
    global Duree_ordre_ligne
    global Duree_recherche
    global Duree_cal_enfant

    Duree_can = 0
    #-----Inclu dans durée can ------
    Duree_suppr_mort = 0
    Duree_transfo_simple = 0
    Duree_transfo_simple_simple = 0
    Duree_tri_sup = 0
    Duree_tri_prio = 0
    Duree_compa_pere_fils = 0
    # -------------------------------
    present_3_fois = 0
    Duree_sep = 0
    Duree_ordre_ligne = 0
    # -------------------------------
    Duree_recherche = 0
    Duree_cal_enfant = 0

def old_reset():
    old_reset_fichier()
    reset_val()

def genere_pos_initiale(n):
    """Genere une position initale avec n points (0.0.0.[...]0.|+)"""
    out = ""
    for i in range(n):
        out += '0.'
    if out != '' :
        out += Char_End_Region + Char_End_Land
    return out

# ------------------------------------------------------------------
# Programme principal et tests
# ------------------------------------------------------------------

def old_programme_principal(n:int,bool_time:bool,bool_print:bool,mode:str):
    """Permet de lancer nimporte quel test, avec ou sans print, avec ou sans efficacité, avec ou sans affichage du temps, et peut importe le n initial"""
    #Le n correspond au nombre de points initiaux
    #Bool_time est True si l'on souhaite l'affichage du temps de calcul
    #Boul_print est True si on souhaite l'affichage des positions, des win et des enfants
    #Mode = "misere" -> variante misere, tous les autres cas corresponde au mode classique
    pos = genere_pos_initiale(n)
    if bool_time :
        if mode == "misere" :
            if bool_print :
                print(str(n),"time","print","misere")
                print(test_du_temps(calcul_victoire_defaite_misere,pos))
            else :
                print(str(n),"time","NOTprint","misere")
                print(test_du_temps(calcul_victoire_defaite_misere_sans_print,pos))
        else :
            if bool_print :
                print(str(n),"time","print","normal")
                print(test_du_temps(calcul_victoire_defaite,pos))
            else :
                #Version la plus efficace pour tester des """"grandes"""" valeurs de n (old_programme_principal(n,True,False,normal))
                #ATTENTION, il faut créer un fichier texte (.txt) vide et donner son addresse dans la variable "nom_fichier" (elle se trouve tout en haut du programme)
                #ATTENTION, pour n=8, le calcul prend plus d'une heure et pour n>9, elle prend plus de 150 heures (estimation, je n'ai pas eu le loisir de faire le calcul)
                #Pour les valeurs <=7, elle prenne 1min30 au max et moins de 5 secondes la majorité du temps
                print("Nbr de points initiaux : " + str(n)," | Time | "," | Pas de print | "," Sprouts normal")
                test_pb_degre(3*n)
                (winloss,time) = test_du_temps_stock(calcul_victoire_defaite_sans_print_stock,pos)
                print(winloss + " <- Résultat final")
                print(time)
                print('\n')
                print('Durées :')
                print(Duree_can,'Duree_can')
                print('#-----Inclu dans durée can ------')
                print(Duree_suppr_mort,'Duree_suppr_mort')
                print(Duree_transfo_simple,'Duree_transfo_simple')
                print(Duree_tri_sup,'Duree_tri_sup')
                print(Duree_transfo_simple_simple,'Duree_transfo_simple_simple')
                print(Duree_tri_prio,'Duree_tri_prio')
                print(Duree_compa_pere_fils,'Duree_compa_pere_fils')
                print('# -------------------------------')
                print(present_3_fois,"Present_3_fois")
                print(Duree_sep,"Duree_sep")
                print(Duree_ordre_ligne,'Duree_ordre_ligne')
                print(Duree_nbr_vie,'Duree_nbr_vie')
                print('# -------------------------------')
                print(Duree_recherche,'Duree_recherche')
                print(Duree_cal_enfant,'Duree_cal_enfant')
                print(compte)
                print(compte2)

    else :
        if mode == "misere" :
            if bool_print :
                print(str(n),"NOTtime","print","misere")
                print(calcul_victoire_defaite_misere(pos))
            else :
                print(str(n),"NOTtime","NOTprint","misere")
                print(calcul_victoire_defaite_misere_sans_print(pos))
        else :
            if bool_print :
                print(str(n),"NOTtime","print","normal")
                print(calcul_victoire_defaite(pos))
            else :
                #print(str(n),"NOTtime","NOTprint","normal")
                #print(calcul_victoire_defaite_sans_print_stock_misere(pos))
                return

def calcul_premier_enfants(n):
    """Calcul les enfants d'une position initiale"""
    pos = genere_pos_initiale(n)
    return canonize_liste_terres(pos,calcul_enfant_terre(pos))

def calcul_et_canonize_terre(pos):
    """renvoie les enfants d'une position après tous être passé par la canonisation"""
    return canonize_liste_terres(pos,calcul_enfant_terre(pos))

def test_pleins_de_fois(k,n):
    """Nombre de fois à tester * nombre de points initiaux"""
    old_reset()
    time_moy = 0
    Duree_can_moy = 0
    Duree_suppr_mort_moy = 0
    Duree_transfo_simple_moy = 0
    Duree_transfo_simple_simple_moy = 0
    Duree_tri_sup_moy = 0
    Duree_tri_prio_moy = 0
    present_3_fois_moy = 0
    Duree_compa_pere_fils_moy = 0
    Duree_sep_moy = 0
    Duree_ordre_ligne_moy = 0
    Duree_recherche_moy = 0
    Duree_cal_enfant_moy = 0
    Duree_nbr_vie_moy = 0

    pos = genere_pos_initiale(n)
    for i in range(k):
        (winloss,time) = test_du_temps_stock(calcul_victoire_defaite_sans_print_stock,pos)
        print(time)
        time_moy += time
        Duree_can_moy += Duree_can
        Duree_suppr_mort_moy += Duree_suppr_mort
        Duree_transfo_simple_moy += Duree_transfo_simple
        Duree_transfo_simple_simple_moy += Duree_transfo_simple_simple
        present_3_fois_moy += present_3_fois
        Duree_tri_sup_moy += Duree_tri_sup
        Duree_tri_prio_moy += Duree_tri_prio
        Duree_compa_pere_fils_moy += Duree_compa_pere_fils
        Duree_sep_moy += Duree_sep
        Duree_ordre_ligne_moy += Duree_ordre_ligne
        Duree_recherche_moy += Duree_recherche
        Duree_cal_enfant_moy += Duree_cal_enfant
        Duree_nbr_vie_moy += Duree_nbr_vie
        old_reset()

    print(winloss + " <- Résultat final")
    print(time_moy/k)
    print('\n')
    print('Durées :')
    print(Duree_can_moy/k,'Duree_can_moy')
    print('#-----Inclu dans durée can ------')
    print(Duree_suppr_mort_moy/k,'Duree_suppr_mort_moy')
    print(Duree_transfo_simple_moy/k,'Duree_transfo_simple_moy')
    print(Duree_transfo_simple_simple_moy/k,'Duree_transfo_simple_simple_moy')
    print(present_3_fois_moy,'present_3_fois_moy')
    print(Duree_tri_sup_moy/k,'Duree_tri_sup_moy')
    print(Duree_tri_prio_moy/k,'Duree_tri_prio_moy')
    print(Duree_compa_pere_fils_moy/k,'Duree_compa_pere_fils_moy')
    print('# -------------------------------')
    print(Duree_sep_moy/k,"Duree_sep_moy")
    print(Duree_ordre_ligne_moy/k,'Duree_ordre_ligne_moy')
    print(Duree_nbr_vie/k,'Duree_nbr_vie_moy')
    print('# -------------------------------')
    print(Duree_recherche_moy/k,'Duree_recherche_moy')
    print(Duree_cal_enfant_moy/k,'Duree_cal_enfant_moy')

def explore(terre):
    Liste = calcul_et_canonize_terre(terre)
    retour_arriere = True
    n = len(Liste[0])
    while retour_arriere :
        print(Liste)
        val = input("Choisir la position explorée : entre 0 et " + str(n-1) + " ou retour ou stop , pour retourner en arrière ou arrêter")
        if val == "retour" :
            retour_arriere = False
        elif val == "stop" :
            return
        else :
            k = int(val)
            print('\n' + Liste[0][k] + '\n')
            explore(Liste[0][k])

def explore_pos(pos):
    Liste = calcule_enfants_A_Z(pos)
    retour_arriere = True
    n = len(Liste[0])
    while retour_arriere :
        print(Liste)
        val = input("Choisir la position explorée : entre 0 et " + str(n-1) + " ou retour ou stop , pour retourner en arrière ou arrêter")
        if val == "retour" :
            retour_arriere = False
        elif val == "stop" :
            return 
        else :
            k = int(val)
            print('\n' + Liste[0][k] + '\n')
            explore_pos(Liste[0][k])


# Les enfants de haut degré pour n=9
##0.0.AB.|0.0.C.|0.0.C.|0.AB.|+ 1707509937.649031
##0.0.0.0.|0.0.0.|1aa.|+ 1707509937.6530635
##0.0.0.0.|0.0.|0.A.|2.A.|+ 1707509937.6649897
##0.0.0.0.|0.0.A.|0.A.|+ 1707509937.6719708
##0.0.0.0.|0.0.A.|0.|2.A.|+ 1707509937.6799493
##0.0.0.0.2.|0.|0.|1aa.|+ 1707509937.6949081
##0.0.0.0.2.|0.0.|1aa.|+ 1707509937.6988976
##0.0.0.0.2.|0.0.2.|AB.|AB.|+ 1707510059.373158
##0.0.0.0.2.|0.0.|12.|+ 1707511132.932231
##0.0.0.0.2.|0.A.|0.|1A.|+ 1707511188.1290228
##0.0.2.|0.0.AB.|0.2.|0.AB.|+ 1707511188.1539562
##0.0.0.|0.0.AB.|0.AB.|2.2.|+ 1707511200.7695203
##0.0.2.|0.0.AB.|0.2.|0.AB.|+ 1707511200.796448
##0.0.0.0.2.|0.AB.|0.|2.AB.|+ 1707511299.3691995
##0.0.0.0.2.|0.0.2.|AB.|AB.|+ 1707511416.7164128
##0.0.0.0.2.|0.A.|0.|A.BC.|BC.|+ 1707511494.0851276
##0.0.A.|0.0.BC.|0.2.A.|0.BC.|+ 1707513087.5461166
##0.0.0.0.2.|0.AB.|1CD.|AB.CD.|+ 1707513160.7991838
##0.0.2.A.|0.0.BC.|0.BC.|1aAa.|+ 1707513212.5929008
##0.0.0.0.2.|0.0.AB.|0.AB.|+ 1707513212.5938654
##0.0.A.|0.0.A.|0.0.|1aa.|+ 1707513212.6387851
##0.0.AB.|0.0.C.|0.0.C.|2.AB.|+ 1707513299.398177
##0.0.0.AB.|0.0.|0.2aa.|AB.|+ 1707513584.2384162
##0.0.2.|0.0.A.|0.0.A.|BC.|BC.|+ 1707513584.2563336
##0.0.0.2.|0.0.A.|0.BC.|A.BC.|+ 1707514247.132718
##0.0.0.AB.|0.0.|0.2aa.|AB.|+ 1707514247.1536617
##0.0.A.|0.0.B.|0.0.B.|A.CD.|CD.|+ 1707514265.0372186
##0.0.0.AB.|0.0.|11aa.|AB.|+ 1707514794.343326
##0.0.0.AB.|0.0.C.|0.0.C.|AB.|+ 1707514864.164878
##0.0.0.0.2.|0.0.AB.|0.AB.|+ 1707514864.1877837
##0.0.0.0.2.|0.0.AB.|0.AB.|+ 1707514864.2057354
##0.0.0.0.A.|0.0.BC.|A.AABC.|+ 1707521714.354827
##0.0.0.AB.|0.0.C.|0.0.C.|AB.|+ 1707521714.3787627
##0.0.AB.|0.0.|0.AB.|11aa.|+ 1707521714.432619
##0.0.0.0.|0.0.2.|12.|+ 1707521745.4919438
##0.0.0.0.|0.0.2.|12.|+ 1707521745.5049098
##0.0.0.0.|0.0.A.|12.A.|+ 1707521818.4834752
##0.0.0.0.|0.1aa.|1b1b.|+ 1707521914.340621
##0.0.A.|0.0.A.|0.0.|12.|+ 1707521914.3685474
##0.0.A.|0.0.A.|0.0.|12.|+ 1707521914.3785207
##0.0.A.|0.0.A.|0.B.|0.|1B.|+ 1707521914.3884928
##0.0.A.|0.0.A.|0.B.|0.|1B.|+ 1707521914.399464
##0.0.A.|0.0.B.|0.0.B.|1A.|+ 1707522367.5870233
##0.0.A.|0.0.A.|0.11a1a.|+ 1707527780.2509248
##0.0.0.A.|0.0.B.|0.A.|BCD.|CD.|+ 1707528383.713022
##0.0.0.A.|0.0.B.|0.A.|BCD.|CD.|+ 1707528383.7349632
##0.0.0.A.|0.A.|0.B.|0.|1B.|+ 1707528399.9240782
##0.0.0.A.|0.A.|0.B.|0.|1B.|+ 1707528399.9425492
##0.0.0.A.|0.0.B.|0.A.|BCD.|CD.|+ 1707528399.966485
##0.0.0.A.|0.0.BC.|0.A.|2BC.|+ 1707530552.0760171
##0.0.0.A.|0.11a1a.|0.A.|+ 1707531911.98058
##0.0.0.0.|0.A.|0.A.|12.|+ 1707531914.5179431
##0.0.0.0.|0.A.|0.A.|12.|+ 1707531914.5358956
##0.0.0.0.|0.AB.|1AB.|1aa.|+ 1707531914.5458689
##0.0.0.0.|0.1.|0.A.|2.A.|+ 1707531948.8118796
##0.0.0.0.|0.AB.|0.|1AB.|+ 1707532000.102592
##0.0.0.0.|0.A.|0.|12.A.|+ 1707532039.8299236
##0.0.0.0.|0.2.|0.A.|1A.|+ 1707532064.339995
##0.0.0.0.|0.AB.|1AB.|1aa.|+ 1707532125.3029292
##0.0.0.0.|0.A.B.|0.B.|1A.|+ 1707532227.7599978
##0.0.0.0.|0.A.|1BC.A.|1BC.|+ 1707532533.9267907
##0.1a1a.A.|0.A.|0.B.|0.B.|0.|+ 1707532545.9687629
##0.0.0.0.|0.A.|1aBa.|A.CD.|B.CD.|+ 1707532860.4939225
##0.0.0.0.|0.11aa.|AB.|AB.|+ 1707533037.6007414
##0.0.0.0.|0.|11a1a.|+ 1707533089.9001472
##0.0.0.0.|0.A.|0.B.|ACD.|B.CD.|+ 1707533161.5071537
##0.0.0.0.|0.A.B.|0.B.|ACD.|CD.|+ 1707533216.3913715
##0.0.0.0.|0.A.|1aBa.|A.B.CD.|CD.|+ 1707533449.486827
##0.0.A.|0.1a1a.B.|0.B.|1bAb.|+ 1707535541.0814278
##0.0.0.0.|0.AB.|0.|1AB.|+ 1707535541.1023724
##0.0.0.0.|0.A.|1BC.A.|1BC.|+ 1707535541.1243129
##0.0.0.0.|0.1a1a.A.|0.A.|+ 1707535541.1243129
##0.0.0.0.AB.|0.0.0.0.AB.|+ 1707535541.125311


#On ajoute le nimber lets go

def computation_nimber_terre(terre,deg_terre):
    """On ajoute le nimber pour améliorer le programme !"""
    n = 0
    trouve = False
    while trouve == False :
        if calcul_victoire_defaite_nimber(terre+ "!",[deg_terre],n) == 'Loss' :
            trouve = True
        else :
            n += 1
    return n
        
compte = 0
        
def calcul_victoire_defaite_nimber(position,liste_des_degre,nimber):
    """On ajoute le nimber pour améliorer le programme !"""
    #global compte
    #global compte2
    #print(position)
    #compte += 1
    if position == '!' or position == "" :
        if nimber == 0 :
            return "Loss"
        else :
            return "Win"
    Sep = separation_de_la_position(position)
    dernier_trouve = False
    dernier = "!"
    deg_dernier = 0
    for k in range(len(Sep)-1,-1,-1) :
        test,val = presence_pos(liste_des_degre[k], Sep[k])
        if test :
            #compte2 += 1
            nimber = nimber ^ val
            Sep[k] = "!"
        elif dernier_trouve == False :
            dernier = Sep[k]
            deg_dernier = liste_des_degre[k]    
            dernier_trouve = True
    if dernier_trouve == False :
        if nimber == 0 :
            return "Loss"
        else :
            return "Win"
    for k in range(len(Sep)) :
        Ck = Sep[k]
        if Ck  != "!" and Ck != dernier :
            nimber = nimber ^ computation_nimber_terre(Ck,liste_des_degre[k])
    Enfants,Degres = calcule_enfants_A_Z(dernier)
    if Enfants == [] or Enfants == [''] or Enfants == ['!'] :
        if nimber == 0 :
            return "Win"
    for i in range(len(Enfants)):
        if calcul_victoire_defaite_nimber(Enfants[i],Degres[i],nimber) == "Loss" :
            return "Win"
    for j in range(nimber):
        if calcul_victoire_defaite_nimber(dernier,[deg_dernier],j) == "Loss" :
            return "Win"
    test,_ = presence_pos(deg_dernier,dernier)
    if not(test):
        ecrire_info_pos(deg_dernier,dernier,nimber)
    return "Loss"


def ecrire_info_pos(n,pos,nimber):
    a = time()
    with open(nom_fichier_n+"_nimber"+str(n)+".txt",'a') as f:
        f.write(pos+ " " + str(nimber) +"\n")
        f.close()
    global Duree_recherche
    Duree_recherche += time()-a

def programme_principal(n):
    pos = genere_pos_initiale(n) + '!'
    deg = nombre_de_vie_terre(pos)
    test_pb_degre_pos(deg)
    a = time()
    out = calcul_victoire_defaite_nimber(pos, [deg], 0)
    print('\n')
    print('Durées :')
    print(Duree_can,'Duree_can')
    print('#-----Inclu dans durée can ------')
    print(Duree_suppr_mort,'Duree_suppr_mort')
    print(Duree_transfo_simple,'Duree_transfo_simple')
    print(Duree_tri_sup,'Duree_tri_sup')
    print(Duree_transfo_simple_simple,'Duree_transfo_simple_simple')
    print(Duree_tri_prio,'Duree_tri_prio')
    print(Duree_compa_pere_fils,'Duree_compa_pere_fils')
    print('# -------------------------------')
    print(present_3_fois,"Present_3_fois")
    print(Duree_sep,"Duree_sep")
    print(Duree_ordre_ligne,'Duree_ordre_ligne')
    print(Duree_nbr_vie,'Duree_nbr_vie')
    print('# -------------------------------')
    print(Duree_recherche,'Duree_recherche')
    print(Duree_cal_enfant,'Duree_cal_enfant')
    print(compte)
    print(compte2)
    return (time()-a),out

def presence_pos(n,terre):
    a = time()
    with open(nom_fichier_n+"_nimber"+str(n)+".txt",'r') as f:
        lines = f.readlines()
        global Duree_recherche
        for terre_nb in lines :
            pos_nimber = terre_nb.split()
            if pos_nimber[0] == terre :
                f.close()
                Duree_recherche += time()-a
                return True,int(pos_nimber[1])
        Duree_recherche += time()-a
        f.close()
        return False,0


def test_pb_degre_pos(n):
    with open(r"C:\Users\Fantôme\OneDrive\Bureau\TIPE\TIPE2\DATA\Max_Deg_nimber.txt",'r') as f:
        lines = f.readline()
        val = int(lines)
        f.close()
    if val <= n :
        for k in range(val,n+1):
            ecrire_info_pos(k,"|Création du doc|","")
        with open(r"C:\Users\Fantôme\OneDrive\Bureau\TIPE\TIPE2\DATA\Max_deg_nimber.txt",'w') as f:
            f.writelines([str(n+1)])
            f.close()

def reset():
    reset_fichier()
    
def reset_fichier():
    with open(r"C:\Users\Fantôme\OneDrive\Bureau\TIPE\TIPE2\DATA\Max_Deg_nimber.txt",'r') as f:
        lines = f.readline()
        n = int(lines)
        f.close()
    supprime_fichier_nb()
    test_pb_degre_pos(n-1)


def supprime_fichier_nb():
    n = 0
    while os.path.exists(nom_fichier_n+"_nimber"+str(n)+".txt") :
        os.remove(nom_fichier_n+"_nimber"+str(n)+".txt")
        n += 1
    with open(r"C:\Users\Fantôme\OneDrive\Bureau\TIPE\TIPE2\DATA\Max_deg_nimber.txt",'w') as f:
            f.writelines(["0"])

def compare_deux_fonction_enfants(pos):
    print(calcul_et_canonize_terre(pos))
    pos += '!'
    print(calcule_enfants_A_Z((pos)))


def forme_liste_temps(n):
    Liste = []
    Liste2 = []
    for k in range(0,n+1):
        pos = genere_pos_initiale(k)
        old_reset()
        (val,time) = test_du_temps_stock(calcul_victoire_defaite_sans_print_stock,pos)
        Liste.append(time)
        Liste2.append(val)
        print(Liste)
    return (Liste,Liste2)

def forme_liste_nb_position(n):
    """Compte le nombre de positions différentes pour tout k inférieur à n"""
    """[3, 18, 222, 4372, 35780]"""
    Liste = []
    Liste_des_pos = []
    def boucle(pos):
        L,_ = calcul_et_canonize_terre(pos)
        if not pos in Liste_des_pos :
            Liste_des_pos.append(pos)
        for k in L :
            if not(k in Liste_des_pos):
                boucle(k)
        return
    for k in range(n,n+1):
        pos = genere_pos_initiale(k)
        boucle(pos)
        Liste.append(len(Liste_des_pos))
        Liste_des_pos = []
    return Liste




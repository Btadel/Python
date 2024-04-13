
#DEVOIR 1 : Travail pratique 1-Jeu Boggle
#Noms: Madalina Frimu (Matricule:20216556), Boudia Adel Tayeb (Matricule:20260177)
###########################################################################################################
#Demander le nombre de manches, le nombre de joueurs ainsi que leurs noms, taille de la grille ############

import random
##############################################################################################################
#Creation des grilles de lettres##############################################################################
#possibilitées d'une grille 4x4, 16 dés
de= """E, T, U, K, N, O,
E, V, G, T, I, N,
D, E, C, A, M, P,
I, E, L, R, U, W,
E, H, I, F, S, E,
R, E, C, A, L, S,
E, N, T, D, O, S,
O, F, X, R, I, A,
N, A, V, E, D, Z,
E, I, O, A, T, A,
G, L, E, N, Y, U,
B, M, A, Q, J, O,
T, L, I, B, R, A,
S, P, U, L, T, E,
A, I, M, S, O, R,
E, N, H, R, I, S"""
#possibilitées d'une grille 5x5, 25 dés
de2="""E, T, U, K, N, O,
E, V, G, T, I, N,
D, E, C, A, M, P,
I, E, L, R, U, W,
E, H, I, F, S, E,
R, E, C, A, L, S,
E, N, T, D, O, S,
O, F, X, R, I, A,
N, A, V, E, D, Z,
E, I, O, A, T, A,
G, L, E, N, Y, U,
B, M, A, Q, J, O,
T, L, I, B, R, A,
S, P, U, L, T, E,
A, I, M, S, O, R,
E, N, H, R, I, S,
A, T, S, I, O, U,
W, I, R, E, B, C,
Q, D, A, H, A, U,
A, C, F, L, N, E,
P, R, S, T, U, G,
J, P, R, X, E, Z,
E, K, V, Y, B, E,
A, L, C, H, E, M,
E, D, U, F, H, K"""
#generer cette grille de lettres selon la taille selectionnée plus haut
def generer_grille(taille):
    tableau_4x4=[]
    de1=de.replace("\n"," ")

    tableau_5x5=[]
    de5=de2.replace("\n"," ")

    for i in range(16):
        sous_liste=[0]*6
        tableau_4x4.append(sous_liste)
    
    for i in range(16):
        for j in range(6):
            tableau_4x4[i][j]=de1[18*i+3*j]        
        
    for i in range(25):
        sous_liste=[0]*6
        tableau_5x5.append(sous_liste)
        
    for i in range(25):
        for j in range(6):
            tableau_5x5[i][j]=de5[18*i+3*j]  
    
    grille=[]
    x=16
    z=25
    for i in range(taille):
        sous_liste=[0]*taille
        grille.append(sous_liste)
    for i in range(taille):               
        for j in range(taille):
            if taille==4: 
                y=random.randint(0,x-1)
                grille[i][j]= tableau_4x4[y][random.randint(0,5)]
            
                select_de=tableau_4x4[y]
                x-=1
                tableau_4x4.pop(y)
    
            if taille==5: 
                y=random.randint(0,z-1)
                grille[i][j]= tableau_5x5[y][random.randint(0,5)]
                
                select_de=tableau_5x5[y] 
                z-=1
                tableau_5x5.pop(y)
            
    #imprimer le support visuel afin que les joueurs puisse entrer leurs mots
    for i in range(taille):
        print("-"*taille*4+"-")
        k=""
        for j in range(taille):
            k+="| " + grille[i][j] + " " 
        print(k+"|") 
    print("-"*taille*4+"-")
    return grille


list_p=[]
def joueur():
    #fonction qui demande les valides noms des joueurs et en fait une liste de joueurs
     joueur1= input("Entrez le nom du joueur 1: ")
     while joueur1.strip=='':
        joueur1= input("Entrez le nom du joueur valide: ")
     list_p.append(joueur1)

     joueur2= input("Entrez le nom du joueur 2: ")
     while joueur2.strip =="":
            joueur2= input("Entrez un nim: ")
     list_p.append(joueur2)


def demander_taille():
    #demander la taille de la grille que les joueurs souhaitent jouer
    taille=int(input("Quelle est la taille de grille dont vous desirez jouer? Veuillez indiquer 4 pour un grille 4x4 et 5 pour une grille 5x5"))
    while taille !=4 and taille !=5:
        taille=input("Veuillez indiquer 4pour une grille 4x4 et de 5 pour une grille 5x5")
    return taille

def motjoueur ():
    #fontion qui demande les mots trouves
    mot_equivalant=format_word(mot=input('entrer un mot:')) #prendre le mot rentre et le resortir en majuscules et sans accents
    while len(mot_equivalant)<3: #obliger le joueur de rentrer un mot de taille au moins 3 lettres
        mot_equivalant=format_word(mot=input('entrer un mot plus long:'))
        continue
    return mot_equivalant

def est_valide(mot_equivalant, grille ):#fais diagonales et mots brisés
    #cette fonction valide nos mots
    def adjacents(x,y):
        a,b=len(grille),len(grille[0])
        oui=[]
        for r in range ( max (0,x-1), min(a,x+2)):
            for c in range ( max (0,y-1), min(a,y+2)):
                if r!= x or  c!=y:
                    oui.append((r,c))
        return oui
    #recherche du mot
    def mot_grille (mot_equivalant,x,y,deja):
        if len(mot_equivalant)== 0:
            return True
        for (r,c) in adjacents (x,y):
            if (r,c) not in deja and grille [r][c]==mot_equivalant[0]:
                if mot_grille (mot_equivalant[1:],r,c, deja| {(r,c)}):
                    return True
        return False
    #cherche la premiere lettre du mot dans la grille 
    for x in range(len(grille)):
        for y in range(len(grille[0])):
            if grille [x][y]== mot_equivalant[0]:
                if mot_grille (mot_equivalant[1:],x,y , {(x,y)}):
                    return True
    return False

def format_word(mot):
    #Cette fonction retourne un mot en majuscule et sans accents
    result = ""
    for c in mot:
        result += equiv(c) #appel a la fonction suivante

    return result.upper()

def equiv(letter):
    #Cette fonction retourne la lettre équivalente sans accent
    match letter:
        case "é" | "è" | "ê" | "ë": return "e"
        case "à" | "â": return "a"
        case "ù" | "û": return "u"
        case "î" | "ï": return "i"
        case "ô": return "o"
        case "ç": return "c"
        case _: return letter

def elinimer_mot(valeur):
    approuver=input("Approuvez vous ce mots?(O/N)")
    if approuver== 'O': #pour oui on approuve on garde ce mot
        return valeur
#fonction qui set les points gagné par longeurs des mots entrer
def point(mot,taille):
    global points
    wl= len(mot)
   
    if taille ==4:
        for wl in range(3,5):
            points=len(mot)-2
        if wl >=6:
            points=len(mot)-1

    if taille ==5:
        for wl in range(3,6):
            points=len(mot)-2
        if wl==7: 
            points=len(mot)-1

    if taille ==6:
        for wl in range(3,5):
            points=len(mot)-2
        if wl==6:
            points=len(mot)-1
        elif wl==7:
            points=len(mot)
        elif wl==8:
            points=len(mot)+2
        elif wl>=9:
            points=12


    return points

#cette foncton permet de resumé le tour d'un joueur et d'alterner les tours
def jeux_al(grillle,taille): 
    
    mot_equivalent = motjoueur()
    if est_valide(mot_equivalent, grillle):
       
        score = point(mot_equivalent,taille)
        print(f"vous avez gagné {score} points avec le mot {mot_equivalent} !")
        return score
    else:
        print("vous avez entré un mot invalide.")
        return 0
    
    
#la fonction jeu qui regroupe toute les autre
def jeu(list_p):
    joueur()
    taille=int(input("entrez la taille desirer:"))
    x=int(input('Combiens de tours par joueurs voulez vous jouz?:'))
    score1=0
    score2=0
    grillle=generer_grille(taille)
   
    for i in range (x):

        print(f"Tour {i+1}")
        print(list_p[0])
        score1 += jeux_al(grillle,taille)
        print(list_p[1])
        score2 +=jeux_al(grillle,taille)
        

        
    #determine le gagnant si il y en a un
    print(f"Score final: {list_p[0]}: {score1}, {list_p[1]}: {score2}")
    if score1>score2:
        print (f"{list_p[0]}, EST LE GRAND GAGNANT!")
    elif score1<score2:
        print (f"{list_p[1]}, EST LE GRAND GAGNANT!")
    elif score1==score2:
        print (f"{list_p[0]} et {list_p[1]} , finissent à égalité")

    return score1, score2 #return pour l'affichage


#definition pas utiliser car imcomplete
def affichage(score1,score2,list_p,Mot_trouvé,list_mots):

    print("\nJOUEUR:", list_p [0])
    print("\n------------------------------")
    for Mots_trouvé in list_mots:
        if not Mots_trouvé['approuver']: 
            print(f" - {Mots_trouvé ['valeur1']} (X) -- REJETER") #regeter le mot s'il n'est pas approuve
        elif not Mots_trouvé['legal']:
            print(f" - {Mots_trouvé ['valeur1']} (X) -- ILLEGAL") #marquer comme illégal si ne suis pas les regles
        else:
            print(f" - {Mots_trouvé ['valeur1']} ({Mots_trouvé ['points par mot']})") #afficher le mot et point si tout va bien
    print("\n==============================")
    print(f"TOTAL: {score1}") #total de points calculés du joueur1 

    print("\nJOUEUR:",list_p[1])
    print("\n------------------------------")
    for Mots_trouvé in list_mots:
        if not Mots_trouvé['approuver']: 
            print(f" - {Mots_trouvé ['valeur2']} (X) -- REJETER") #regeter le mot s'il n'est pas approuve
        elif not  Mots_trouvé['legal']:
            print(f" - {Mots_trouvé ['valeur2']} (X) -- ILLEGAL") #marquer comme illégal si ne suis pas les regles
        else:
            print(f" - {Mots_trouvé ['valeur2']} ({Mots_trouvé ['points par mot']})") #afficher le mot et point si tout va bien
    print("\n=============================="),
    print(f"TOTAL: {score2}") #total #total de points calculés du joueur1 

    
    #reponse= input(f"Voulez-vous jouer une nouvelle partie? [O/N]")
    #nouvelle_partie(reponse)
#La definition n'est pas utiliser car incomplete
def ajout_mot(valeur,list_p,list_mot):
    taille= len(valeur) #trouver la taille de mot
    index = len(list_mot) + 1
    
    legal= est_valide(valeur,taille, legal=True) #verifier si le mot est legal

    Mots_trouvé = {
        "index": index,
        "valeur 1":valeur, #mots du premier joueur
        "valeur 2":valeur, #mots du deuxieme joueur
        "legal": legal,
        "points par mot": points,
        "noms des joueurs":list_p  #je voulais rajouter la liste des noms dans cette liste mais je sais pas si c<est possible
    }

    list_mot.append(Mots_trouvé)


def test():
    def test_generer_grille():
        assert generer_grille(5)!=generer_grille(5) #Pour deux appels successifs, la fonction ne génere par le meme grille 4x4.
        assert generer_grille(4)!=generer_grille(4) #Pour deux appels successifs, la fonction ne génere par le meme grille 5x5.
        assert generer_grille(9)== False #pour toutes autre tailles plus grande que 4 ou 5, le definition ne va rien generer.On nous demandra une autre taille valide plus haut dans la "def demander_taille():""
        assert generer_grille(2)== False #pour toutes autre tailles plus petites que 4 ou 5, le definition ne va rien generer.On nous demandra une autre taille valide plus haut dans la "def demander_taille():""
        assert generer_grille(10)== False #pour toutes autre tailles plus petites que 4 ou 5, le definition ne va rien generer.On nous demandra une autre taille valide plus haut dans la "def demander_taille():""

    def test_est_valide():
        assert est_valide(grille=[['V', 'I', 'R', 'S'], ['O', 'U', 'H', 'L'], ['R', 'R', 'N', 'E'], ['U', 'O', 'M', 'O']], mot="VORM")== True # Le mot est bel est bien valide selon la grille générée de 4x4
        assert est_valide(grille=[['O', 'A', 'H', 'N'], ['R', 'H', 'G', 'E'], ['E', 'S', 'B', 'Z'], ['L', 'U', 'B', 'A']], mot="AHSU")== True # Le mot est bel est bien valide selon la grille générée de 4x4
        assert est_valide(grille=[['W', 'A', 'V', 'E'], ['S', 'A', 'O', 'N'], ['M', 'K', 'T', 'J'], ['S', 'H', 'I', 'E']], mot="VORM")== False # Le mot est invalide selon la grille générée de 4x4
        assert est_valide(grille=[['I', 'D', 'B', 'O','O'], ['A', 'L', 'T', 'K','S'], ['D', 'N', 'I', 'X','M'], ['L', 'I', 'D', 'K','P'], ['A', 'U', 'M', 'G','E']], mot="ALIKE")== True # Le mot est bel est bien valide selon la grille générée de 5x5
        assert est_valide(grille=[['I', 'D', 'B', 'O','O'], ['A', 'L', 'T', 'K','S'], ['D', 'N', 'I', 'X','M'], ['L', 'I', 'D', 'K','P'], ['A', 'U', 'M', 'G','E']], mot="IDXM")== False # Le mot est invalide selon la grille générée de 5x5

 
    test_generer_grille()
    test_est_valide()
    
#test()

#jeu(list_p)





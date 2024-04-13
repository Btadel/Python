
###############################################################################
## Touché
###############################################################################
## Auteur: Boudia Adel Tayeb
## Date: 04-04-2023
## Email: boudia71habib@icloud.com
###############################################################################

from turtle import * # Enlever en commentaire en dehors de Codeboot
#
import math          # Enlever en commentaire en dehors de Codeboot
import random
import turtle


def arc(r, angle):
    """Cette fonction permet de tracer un arc de cercle

    Args:
        r (int): Rayon de l'arc
        angle (int): Angle de l'arc
    """
    longueur_arc = 2 * math.pi * r * angle / 360
    n = int(longueur_arc / 3) + 1
    longueur_etape = longueur_arc / n
    angle_etape = float(angle) / n
    for _ in range(n):
        fd(longueur_etape)
        lt(angle_etape)



def cercle(r):
    """Cette fonction permet de dessiner un cercle

    Args:
        r (int): Longueur du rayon

    """
    pd()
    pencolor(1,1,1)
    bk(8)
    for _ in range(4):
        fd(16); lt(90)
    fd(8)
    pencolor(1,0,0)
    arc(r, 360)
    pencolor(0,0,0)


def carre(cote):
    """ette fonction permet de dessiner un carré

    Args:
        cote (int): Longueur d'un coté
    """
    for _ in range(4):
        fd(cote); lt(90) 

    

def positionner(x, y):
    """Cette fonction permet de positionner la tortue relativement à son emplacement actuel

    Args:
        x (int): Nombre de pas en x
        y (int): Nombre de pas en y
    """
    pu(); fd(x); lt(90); fd(y); rt(90); pd()


def grille(cols, lignes, taille, espace):
    """Cette fonction permet de tracer une grille.
    
    Args:
        cols (int): Nombre de colonnes
        lignes (int): Nombre de lignes
        taille (int): Taille d'une case
        espace (int): Taille de l'espace entre chaque case
    """
    turtle.hideturtle()
    turtle.speed("fastest")

    
    for x in range(cols):
        for y in range(lignes):
            positionner((x * (taille + espace)), y * (taille + espace))
            carre(taille)
            positionner(-x * (taille + espace), -y * (taille + espace))

    pu(); lt(180); fd(16); rt(90); pensize(7); pd();pencolor(0,0,1) 
    fd((taille+espace)*lignes)
    
    pu();pensize(1); rt(180); fd((taille+espace)*lignes); rt(90); fd(137); lt(180);pd()
    pencolor (0,0,0)
        
        
    
    for x in range(cols):
        for y in range(lignes):
            positionner((x * (taille + espace)), y * (taille + espace))
            carre(taille)
            positionner(-x * (taille + espace), -y * (taille + espace))
    pu()
    goto (0,0)

    


def bateau():
    #cette fonction place 5 bateau sur une grille sans repetitions
    secret=[]

    while len(secret)!=5:
        
         m= random.randint(1,6)
         n= random.randint(1,6)
         if (m,n) not in secret:
            secret.append((m,n))
            
         
        
    #print(secret) si vous voulez les voir
    return secret



def check(secret,t,s):   

    
    if (t,s) in secret:
        print("TOUCHÉ!")
        return True
    else:
        print("RATÉ :( ")
        return False

def equiv(letter):
    letter_to_number = {
        "a": 1, "A": 1,
        "b": 2, "B": 2,
        "c": 3, "C": 3,
        "d": 4, "D": 4,
        "e": 5, "E": 5,
        "f": 6, "F": 6
    }
    return letter_to_number.get(letter, 0)

def turn (secret):
     #cette fonction resume le tour d'un joueur
    t,s= int(equiv(input("Valeur entre A et F dans l'axe des x: "))), int(input(" y: "))
    while  t<1  or t>6 or t==0:
       t= int(equiv(input("valeur entre de A a F: ")))
    
    while s<1 or s>6:
        s=int(input(" y: "))

    #si il trouve un bateau, le carre sur cette position  est effac/ et laisse place a un cercle rouge
    if check(secret,t,s):
        
        positionner(((t *21 )-14), ((s *21)-20))
        pensize(2.5)
        pencolor(1,0,0)
        
        cercle(7)#efface le carre et met un cercle rouge
        return ((t,s))
        
    else:
        #si les coordonnes entrer ne sont pas les coord. d'un bateau ,un carr/ vert s'affiche a cette position
        positionner(((t *21 )-21), ((s *21)-21))
        pensize(2.5)
        pencolor(0,1,0)
        carre(16)
        #x
        lt(45)
        fd(((16**2)*2)**0.5)
        lt(135)
        fd(16)
        lt(135)
        fd(((16**2)*2)**0.5)
        lt(45)
        return ((t,s))
        

# Fonction principale du programme



def jouer():
    #cette fonction regroupe toute les autres et permet de jouer
    grille(6,6,16,5)
    
    secret1=bateau()
    
    secret2=bateau()
    n=0
    v=0
    while True:

        
        print("Joueur 1:")
        r=turn(secret1)
        if r in secret1 :
            n+=1
        if n==5:
         print ("le grand gagnant est le joueur 1!")
         break
    
        pu()
        goto (-153,0)
        print("Joueur 2:")
        j=turn(secret2)
        print("score:",n)
        if j in secret2:
            v+=1
        pu()
        goto (0,0)
        print("score:",v)
        if v==5:
            print ("le grand gagnant est le joueur 2!")
            break
    
jouer()
        
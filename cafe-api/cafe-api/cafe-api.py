#Boudia Adel (20260177)
#Soumaya Benaouda (20159474)


import json
import csv
import re
from datetime import datetime
import datetime

#cette fonction permet de lire n'importe quel fichier csv qu'on lui donne
def lire_fichier_csv(nom_fichier):
    contenu= []
    with open(nom_fichier,newline='') as csvfile:
        reader=csv.reader(csvfile,delimiter='|',quotechar='"')
        for row in reader:
            contenu.append([element.strip() for element in row])
        return contenu
#cette fonction permet de lire n'importe quel fichier json qu'on lui donne
def lire_fichier_json(nom_fichier):
    with open(nom_fichier,'r') as jsonfile:
        contenu=json.load(jsonfile)
    return contenu
#cette fonction permet de dire si le matricule et mot de passe ce trouve dans le fichier comptes.csv
def validation_utilisateur(matricule, password):
    fichier=lire_fichier_csv("comptes.csv")  
    for y in fichier:
        if str(y[0]) == str(matricule) and str(y[3]) == str(password):
            return True, y[5] 
    return False , None


menu=lire_fichier_json("menu.json")

#cette fonction permet savoir quelle categorie la personne cherche
def detect_categorie(text):
    pattern = r'menu\/(.*?)\/items'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None

#cette fonction permet d'afficher tout  le menu à partir du fichier json avec les prix dispo etc
def afficher_tout(menu):
    for categorie in menu:
        print(f"Catégorie: {categorie}")

        def afficher_items(items):
            print("      id   nom                          prix  disponible")
            print("    ---- ------------------------------ ----- ----------")
            for item in items:
                print(f"    {item['id']:>4}   {item['nom']:<30}{item['prix']:<3}$ {item['disponible']}")

        def voyager_dansmenu(data):
            for x, valeur in data.items():
                if isinstance(valeur, dict):
                    print(f"  Sous-catégorie: {x}")
                    voyager_dansmenu(valeur)
                elif x == "items":
                    afficher_items(valeur)

        voyager_dansmenu(menu[categorie])
        print("\n")

#cette fonction permet d'afficher les categories (ex:boisson,fruits)
# elle est composer d'une fonction qui permet d'afficher les items de la categorie et l'autre permet de trouver la categorie recherché
def afficher_categorie(menu, categorie):
    if categorie in menu:
        print(f"Catégorie: {categorie}")
        
        def afficher_items(items):
            print("      id   nom                          prix  disponible")
            print("    ----  ----------------------------  ----- ----------")
            for item in items:
                print(f"    {item['id']:>4}   {item['nom']:<30}{item['prix']:<3}$ {item['disponible']}")

        def voyage(data):
            for x, y in data.items():
                if isinstance(y, dict):
                    print(f"  Sous-catégorie: {x}")
                    voyage(y)
                elif x == "items":
                    afficher_items(y)

        voyage(menu[categorie])



#marche pas, mais elle devait servir à afficher les sous categories (ex:boissons chaudes)
def afficher_sous_categorie(menu,sous_categorie):
    
    
    existe = False
    for categoriee, sous_categories in menu.items():
        if sous_categorie in sous_categories:
            detail = sous_categories[sous_categorie]
            print(f"{sous_categorie}:")
            for item in detail["items"]:
                print(f"    {item['id']:>4}   {item['nom']:<30}{item['prix']:<3}$ {item['disponible']}")
            existe=True
            
            break

    if not existe:
        print(f"Sous-catégorie {sous_categorie} non trouvée.")


#affiche les sous sous categories, mais n'a pas exactement la même logique que la fonction afficher categorie
#puisque elle est faite d'une fonction et une boucle et une fonction recursive qui sert parcourirs le json
def sous_sous_categorie(menu, sous_cate):
    def afficher2(data, esp=""):
        if isinstance(data, dict):
            for x, y in data.items():
                if x == sous_cate:
                    if isinstance(y, dict) and "items" in y:
                        print(f"{esp}Sous-catégorie: {sous_cate}")
                        print(f"{esp}  id   nom                          prix  disponible")
                        print(f"{esp}---- ------------------------------ ----- ----------")
                        for item in y["items"]:
                            print(f"    {item['id']:>4}   {item['nom']:<30}{item['prix']:<3}$ {item['disponible']}")
                        print()
                        return True
                if isinstance(y, (dict, list)):
                    if afficher2(y, esp + "  "):
                        return True

        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    if item['nom'] == sous_cate:
                        print(f"{esp}ID: {item['id']}")
                        print(f"{esp}Nom: {item['nom']}")
                        print(f"{esp}Prix: {item['prix']}")
                        print(f"{esp}Disponible: {item['disponible']}")
                        print()
                        return True
                    if afficher2(item, esp):
                        return True

    for x, y in menu.items():
        if isinstance(y, (dict, list)):
            if afficher2(y, "  "):
                return True
    return False

#cette fonction est composé de deux fonction.Elle reçoit l'id et le menu
#la premiere affiche les informations d'un élément id, nom, prix et dispo dans un format de tableau
#la deuxieme permet de parcourire les données(menu) de maniere recursive
def afficher_id(menu, id):
    def afficher_item(item):
        print("ID   Nom                             Prix  Disponible")
        print("---- ------------------------------ ----- ----------")
        print(f"{item['id']:>4} {item['nom']:<30} {item['prix']:<3}$ {item['disponible']}")


    def chercher_item(data):
        for key, value in data.items():
            if isinstance(value, dict):
                chercher_item(value)
            elif key == "items":
                for item in value:
                    if item["id"] == id:
                        afficher_item(item)
                        return

    chercher_item(menu)

#cette fonction permet de trouver l'id si il y en a un dans request (process_request)
def detect_id(request):
    cherche = re.search(r"items/(\d+)", request)
    if cherche:
        return int(cherche.group(1))
    else:
        return None

#cette ouvre le fichier csv pour savoir le num de la nouvelle commande a partir de la precedente 
#puis elle écrit dans le fichier csv (csv.writer)
#items et pas item car plusieurs objets peuvent être pris en compte
def ajouter_commande(matricule, items, montant_total):
    
    with open('commandes.csv', mode='r', newline='', encoding='utf-8') as csvfile:
        id_commande = sum(1 for _ in csv.reader(csvfile)) + 1

    with open('commandes.csv', mode='a', newline='', encoding='utf-8') as csvfile:
        csv = csv.writer(csvfile, delimiter='|')
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        csv.writerow([id_commande, matricule, ", ".join(items), date, montant_total])



def disponibilité(nom_produit,menu, disponible):
    for categorie in menu:
        for produit in menu[categorie]:
            if produit == "items":
                for item in menu[categorie][produit]:
                    if item["nom"] == nom_produit:
                        # modifier la valeur de "disponible"
                        item["disponible"] = disponible
                        break

    
    with open("chemin/vers/le/fichier.json", "w") as f:
        json.dump(menu, f, indent=4)

#cette  fonction permet d'ouvrir le fishier en utf-8
#parcours les lignes du csv et save pour chaque ligne les valeur
#pour finalement les imprimés sous forme de tableau
#ou si on donne un id precis elle va imprimé que la ligne de l'id demandé
#bien sur si un id est fournis la fonction va d'abord chercher l'id dans commandes,csv
def afficher_commande (id=None):
    commandes = lire_fichier_csv("commandes.csv")
    print(f"{'id'.ljust(3)} {'matricule'.ljust(20)} {'items et quantité'.ljust(40)} {'date'.ljust(10)}")
    print("-"*75)
    if id:
        commande_detecter = False
        for commande in commandes:
            if commande[0] == id:
                print(f"{commande[0].ljust(3)} {commande[1].ljust(20)} {commande[2].ljust(40)} {commande[3].ljust(10)}")
                commande_detecter = True
                break
        if not commande_detecter:
            print("Introuvable.")
    else:
        for commande in commandes:
            print(f"{commande[0].ljust(3)} {commande[1].ljust(20)} {commande[2].ljust(40)} {commande[3].ljust(10)}")
#detect l'id si besoin et est utiliser dans process_request
def detect_id_valeur(request):
    # cherche l'identifiant et la valeur dans la requete
    idchercher = r"\/api\/menu\/items\/(\d+)"
    valeurchercher = r"disponible=(\d)"

    id = re.search(idchercher, request)
    valeur = re.search(valeurchercher, request)

    if id and valeur:
        identifiant = int(id.group(1))
        valeur = int(valeur.group(1))
        return identifiant, valeur
    else:
        return None, None
#marche pas
#def modifier_disponibilite(menu, id, nouvelle_valeur):

    
    nouvelle_valeur = True if nouvelle_valeur == "0" else False

    def modifier_dispo_(menu):
        for x, y in menu.items():
            if isinstance(y, dict):
                modifier_dispo(value)
            elif x == "items":
                for item in value:
                    if item["id"] == id :
                        item["disponible"] = nouvelle_valeur
                        return True
        return False

    if modifier_dispo(menu):
        with open(menu, 'w') as jsonfile:
            json.dump(menu, jsonfile, indent=4, ensure_ascii=False)
        return True
    else:
        return False

#cette fonction prend en charge les requete en mettant tout les autre fonctions , certaines options sont slm si le role est admin 
def request_(request, menu,matricule,role):
    request = request.lower().strip()

    # Requetes pour le  public
    if request == "get/api/menu/items":
        afficher_tout(menu)
        return True
    elif request == "get/api/menu/menu":
        afficher_tout(menu)
        return True
    elif request.startswith("post /api/commandes"):
        items_str = request[len("post /api/commandes"):].strip()
        items = items_str.split()

        # Calculer le montant total
        montant_total = 0
        for item_str in items:
            id_item, quantite = item_str.split('x')
            id_item, quantite = int(id_item), int(quantite)
            prix_item = 0
            for categorie in menu.values():
                for sous_categorie, sous_categorie2 in categorie.items():
                    if isinstance(sous_categorie2, dict) and "items" in sous_categorie2:
                        for item in sous_categorie2["items"]:
                            if item['id'] == id_item:
                                prix_item = item['prix']
                                break
                    elif isinstance(sous_categorie2, list):
                        for item in sous_categorie2:
                            if item['id'] == id_item:
                                prix_item = item['prix']
                                break
                    if prix_item > 0:
                        break
                if prix_item > 0:
                    break
            montant_total += prix_item * quantite

        ajouter_commande(matricule, items, montant_total)
        print(f"Commande ajoutée avec succès. Montant total: ${montant_total:.2f}")
        return True

    categorie = detect_categorie(request)
    
    if categorie== 'boisson' or 'sandwich' or 'fruit' or 'muffin' :
        afficher_categorie(menu,categorie)
    #if categorie== 'boisson_chaude' or 'boisson_froide' or 'regulier' or 'wrap' or 'pain' or 'chausson' or 'croissant':
       # afficher_sous_categorie(menu,categorie)
   
    if categorie== 'cafe' or 'the' or 'chocolat':
        sous_sous_categorie(menu,categorie)
    
    if detect_id(request):
        afficher_id(menu,detect_id(request))
    # Requetes pour le staff
    if role == "admin":
        if request.startswith('GET') and request.endswith("commandes"):
            afficher_commande()
            return True
        if request.startswith('GET') and request.find("commandes/"):
            print('oui')
            id = ''.join([char for char in request if char.isdigit()])
            afficher_commande(id)
            return True
        if request.startswith('PUT'):
           identifiant,valeur = detect_id_valeur(request)
           #modifier_disponible_par_id(identifiant,valeur)
           print('cette partie du code ne marche pas')
           return True
            
            


    return False




#la fonction est la fonction principale qui prend le matricule et le mot de passe
#elle permet aussi d'utiliser request
def main():
    print("Bienvenue au Café étudiant de l'UdeM")

    matricule = input("Entrez votre matricule: ")
    password = input("Entrez votre mot de passe : ")

    is_valid, role = validation_utilisateur(matricule, password) 

    while not is_valid:
        print("Nom d'utilisateur ou mot de passe invalide.")
        matricule = input("Entrez votre matricule: ")
        password = input("Entrez votre mot de passe : ")
        is_valid, role = validation_utilisateur(matricule, password)

    print("Connexion réussie.")

    while True:
        requete = input("Quelle est votre requête (ou 'q' pour quitter) ?\n")
        if requete.lower() == "q":
            break

        result = request_(requete, menu,matricule, role)
        if not result:
            print("Requête non reconnue. Veuillez réessayer.")
    
    print("Déconnexion réussie.")


#def test():
    # Test 1: Afficher la catégorie "Boissons"
    afficher_categorie(menu, "boissons")

    #Test 2: Afficher la catégorie "fruit"
    afficher_categorie(menu, "fruit")

    # Test 3: Afficher une catégorie 
    afficher_categorie(menu, "sandwich")
    # Test 4: Afficher rien
    afficher_categorie(menu, "bonbons")

    matricule = "20077610"
    role = "admin"

    #affiche tout le menu
    request_("get/api/menu/menu", menu, matricule, role)

    #Ajoute une commande
    request_("post /api/commandes 1x2 3x1", menu, matricule, role)

    #affiche les commandes pour le staff
    request_("GET /api/commandes", menu, matricule, role)

    # affiche une commande spécifique pour le staff
    request_("GET /api/commandes/1", menu, matricule, role)

    #modifie la disponibilité d'un produit pour le staff
    request_("PUT /api/menu/items/1 disponible=0", menu, matricule, role)
    
    #trouver l'id dans une requete valide
    request1 = "GET /api/menu/items/3"
    result1 = detect_id(request1)
    print(f"Test 1: L'ID trouvé est {result1} (attendu: 3)")

    #ttrouver l'ID dans une requete valide avec un espace
    request2 = " GET /api/menu/items/12 "
    result2 = detect_id(request2)
    print(f"Test 2: L'ID trouvé est {result2} (attendu: 12)")

    #aucun id trouvé dans une requete invalide
    request3 = "GET /api/menu/items/"
    result3 = detect_id(request3)
    print(f"Test 3: L'ID trouvé est {result3} (attendu: None)")

    # aucun id trouvé dans une requete avec un autre format
    request4 = "GET /api/menu/items/id3"
    result4 = detect_id(request4)
    print(f"Test 4: L'ID trouvé est {result4} (attendu: None)")

    #trouver l'id dans une requete valide avec des caractères supplémentaires
    request5 = "GET /api/menu/items/45/test"
    result5 = detect_id(request5)
    print(f"Test 5: L'ID trouvé est {result5} (attendu: 45)")




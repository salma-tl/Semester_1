import time


# Gestionnaire de stock

# Dictionnaires et listes pour stocker les données
stock = {}              # {nom: (prix, quantité, catégorie)}
historique = []         # [(produit, action, quantité, date)]
compteur_ventes = {}    # {nom: nombre_ventes}


#Ajoute un nouveau produit au stock
def ajouter_article():
    nom = input("Nom de l’article : ")
    prix = float(input("Prix unitaire (DH) : "))
    qte = int(input("Quantité disponible : "))
    cat = input("Catégorie : ")

    stock[nom] = (prix, qte, cat)
    compteur_ventes[nom] = 0
    historique.append((nom, "ajout", qte, time.strftime("%Y-%m-%d %H:%M:%S")))

    print(f"✅ {nom} a été ajouté au stock.")

#Supprime ou réduit la quantité d’un produit
def supprimer_article():
    nom = input("Nom de l’article à vendre : ")

    if nom not in stock:
        print(" Cet article n’existe pas dans le stock.")
        return

    qte_retrait = int(input("Quantité à retirer : "))
    prix, qte_actuelle, cat = stock[nom]

    if qte_retrait >= qte_actuelle:
        del stock[nom]
        print(f"{nom} a été entièrement retiré du stock.")
    else:
        stock[nom] = (prix, qte_actuelle - qte_retrait, cat)
        print(f"Nouvelle quantité de {nom} : {qte_actuelle - qte_retrait}")

    compteur_ventes[nom] += qte_retrait
    historique.append((nom, "retrait", qte_retrait, time.strftime("%Y-%m-%d %H:%M:%S")))

#Calcule et affiche la valeur totale du stock
def valeur_stock():
    if not stock:
        print("Aucun article enregistré pour le moment.")
        return

    valeur = sum(p * q for p, q, _ in stock.values())
    print(f"Valeur globale du stock : {valeur:.2f} DH")


# Seuil minimum de réapprovisionnement
SEUIL_MINIMUM = 5

#Alerte si le stock d’un produit est trop bas
def verifier_niveaux():
    if not stock:
        print(" Aucun article à vérifier.")
        return

    print("\nProduits à stock faible :")
    alerte = False
    for nom, (prix, qte, cat) in stock.items():
        if qte < SEUIL_MINIMUM:
            print(f"- {nom} ({qte} unités restantes)")
            alerte = True
    if not alerte:
        print("Tous les niveaux de stock sont corrects.")

#Recherche des produits par catégorie
def filtrer_par_categorie():
    cat_recherche = input("Entrez le nom de la catégorie : ")
    trouve = False

    print(f"\nArticles dans la catégorie '{cat_recherche}' :")
    for nom, (prix, qte, cat) in stock.items():
        if cat.lower() == cat_recherche.lower():
            print(f"- {nom} : {prix} DH | {qte} en stock")
            trouve = True

    if not trouve:
        print("Aucun article trouvé dans cette catégorie.")

#Classe les produits selon leur nombre de ventes
def rapport_ventes():
    if not compteur_ventes:
        print("Aucune vente enregistrée.")
        return

    classement = sorted(compteur_ventes.items(), key=lambda x: x[1], reverse=True)
    print("\n Classement des produits les plus vendus :")
    for nom, ventes in classement:
        print(f"{nom}: {ventes} ventes")

#Affiche l'historique des operations effectuées
def afficher_historique():
    if not historique:
        print("Aucune opération enregistrée pour l’instant.")
        return

    print("\nHistorique des transactions :")
    for article, action, qte, date in historique:
        print(f"{date} | {action.upper()} | {article} ({qte} unités)")


def menu_principal():
    while True:
        print(""" 
        Menu de gestion de stock
1.  Ajouter un produit
2.  Vendre un produit
3️.  Afficher la valeur du stock
4️.  Vérifier les seuils minimaux
5️.  Rechercher par catégorie
6️.  Rapport des ventes
7️.  Consulter l’historique
8️.  Quitter
==============================
""")

        choix = input("Choisissez une option (1-8) : ")

        if choix == "1":
            ajouter_article()
        elif choix == "2":
            supprimer_article()
        elif choix == "3":
            valeur_stock()
        elif choix == "4":
            verifier_niveaux()
        elif choix == "5":
            filtrer_par_categorie()
        elif choix == "6":
            rapport_ventes()
        elif choix == "7":
            afficher_historique()
        elif choix == "8":
            print("Fin du programme. À bientôt !")
            break
        else:
            print("Option invalide, essayez encore.\n")



menu_principal()

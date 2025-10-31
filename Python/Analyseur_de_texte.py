def analyse_lexical(texte):
    #Frequence des mots
    texte = texte.lower()
    texte_propre = ""
    for car in texte:
        if car.isalnum() or car.isspace():
            texte_propre += car
    mots = texte_propre.split()
    freq={}
    for mot in mots:
        if mot in freq:
            freq[mot]+=1
        else:
            freq[mot]=1
    print("La frequence des mots est :")
    for mot, count in freq.items():
        print(f"{mot} : {count}")
    #Longeur moyenne des mots
    longeur_moyenne=sum(len(mot) for mot in mots)/len(mots)
    print("La longeur moyenne des mots est :", longeur_moyenne)
    #Les mots les plus et mots utilisés
    plus=max(freq.values())
    moins=min(freq.values())
    for mot, count in freq.items():
        if count==plus:
            print(f"{mot} est le plus utiliser avec une frequence de  : {count}")
        if count == moins:
            print(f"{mot} est le moins utiliser avec une  frequence de  : {moins}")
    #palindromes
    palindromes=[]
    for mot in mots:
        if len(mot)>1 and mot==mot[::-1]:
            palindromes.append(mot)
    print(f"\nPalindromes détectés : {palindromes}")
    return freq, mots

def analyse_gramatical(texte):
    #nombre de phrases
    phrases=[]
    phrase=""
    for car in texte:
        phrase+=car
        if car in ".!?":
            phrases.append(phrase)
            phrase=""
    if phrase.strip():
        phrases.append(phrase.strip())
    nbr_de_phrases=len(phrases)
    print("Le nombre de phrases est : ",nbr_de_phrases)
    #La longeur des phrases
    for phrase in phrases:
        print(f"La longeur de la phrase : {phrase} est : {len(phrase)} ")
    #type de ponctuation
    dic_ponc={}
    for carac in texte:
        if carac in ".,!?;:…":
            dic_ponc[carac]=1

    print(dic_ponc)
    #statistiques par type de mot
    texte = texte.lower()
    texte_propre = ""
    for car in texte:
        if car.isalnum() or car.isspace():
            texte_propre += car
    mots = texte_propre.split()
    stats={
        "verbes":0,
        "adjectifs":0,
        "adverbes":0,
        "noms":0,
        "autres":0
    }
    for mot in mots:
        if mot.endswith(("er", "é", "ée", "és", "ées")):
            stats["verbes"]+=1
        elif mot.endswith(("ment",)):
            stats["adverbes"] += 1
        elif mot.endswith(("tion", "sion", "ure", "té", "age", "eur", "esse")):
            stats["noms"] += 1
        elif mot.endswith(("eux", "euse", "able", "ible", "ant", "ante")):
            stats["adjectifs"] += 1
        else:
            stats["autres"] += 1
    print("Statistique par mot :")
    total = len(mots)
    for type_mot,count in stats.items():
        pourcentage = (count / total) * 100
        print(f"{type_mot} : {count} mots ({pourcentage:.2f}% de pourcentage)")
    return phrases
def Rapports(freq, mots, phrases):
    #Top 10 des mots
    top10=sorted(freq.items(), key=lambda x:x[1], reverse=True)[:10]
    print("\nTop 10 mots : ")
    for mot,count in top10:
        print(f"{mot} : {count}")
    #  Phrases les plus longues (par nombre de mots)
    phrases_longue=sorted(phrases, key=lambda p: len(p.split()), reverse=True)[:3]
    print("\nles 3 plus longues phrases :")
    for p in phrases_longue:
        print(f"{p} ({len(p.split())} mots)")
    #Div du vocabulaire
    vocabulaire_unique=set(mots)
    diversite=(len(vocabulaire_unique)/len(mots))*100
    print(f"\n Diversite du vocabulaire : {diversite:.2f}%")
    # pattern repititif (mots apparaissant plus que 3 fois)
    repetitifs=[mot for mot ,freq in freq.items() if freq>3]
    if repetitifs:
        print(f"\nCe mot est repetitif : {repetitifs}")
    else:
        print("\naucun mot n'est repetitif")

def menu_principal():
    texte_input = ""
    freq, mots, phrases = {}, [], []

    while True:
        print("""
1. Entrer un paragraphe
2. Analyse lexicale
3. Analyse grammaticale
4. Rapports
5. Quitter
==============================
""")
        choix = input("Choisissez une option (1-5) : ")

        if choix == "1":
            texte_input = input("Veuillez saisir un texte : \n")
            print("Texte enregistré avec succès !\n")
        elif choix == "2":
            if texte_input:
                freq, mots = analyse_lexical(texte_input)
            else:
                print("Aucun texte saisi. Veuillez d'abord entrer un paragraphe.\n")
        elif choix == "3":
            if texte_input:
                phrases = analyse_gramatical(texte_input)
            else:
                print("Aucun texte saisi. Veuillez d'abord entrer un paragraphe.\n")
        elif choix == "4":
            if texte_input:
                if not freq or not mots or not phrases:
                    # Calculer si ce n'est pas déjà fait
                    freq, mots = analyse_lexical(texte_input)
                    phrases = analyse_gramatical(texte_input)
                Rapports(freq, mots, phrases)
            else:
                print("Aucun texte saisi. Veuillez d'abord entrer un paragraphe.\n")
        elif choix == "5":
            print("Fin du programme. À bientôt !")
            break
        else:
            print("Option invalide, essayez encore.\n")



menu_principal()


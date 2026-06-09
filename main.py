
import random


tailleMot = 8
maxTentatives = 6

# Fonction qui demande le nom des joueurs
def demander_nom(x):
    while True:
        nom = input(f"Nom du joueur {x} : ").strip()

        if nom == "":
            print("❌ Le nom ne peut pas être vide")
        elif not nom.isalpha():
            print("❌ Le nom doit contenir uniquement des lettres")
        else:
            return nom

# Fonction qui lit le fichier csv
def readFichier(flux):
    tab = flux.readlines()
    flux.close()
    taille = len(tab)
    for i in range(taille):
        tab[i] = tab[i].strip("\n")
        tab[i] = tab[i].split(";")
    return tab

# Fonction qui tire aléatoirement un mot de 8 lettres dans la catégorie choisie
def motAleatoire(categorie, tab):
   
    
    # Filtrer les mots de 8 lettres
    tab2 = []
    for i in range(1, len(tab)):
        mot = tab[i][categorie - 1]  
        if len(mot) == tailleMot:
            tab2.append(mot)
    
    if len(tab2) == 0:
        print("cette categorie ne contient aucun mot")
    
    # Choisir un mot au hasard
    mot_choisi = random.choice(tab2)
    return mot_choisi.upper()

# Affiche les règles du jeu       
def afficherRegles(nbr_joueurs):
    print("\n" + "═" * 70)
    print(" " * 20 + "🎮 RÈGLES DU JEU MOTUS 🎮")
    print("═" * 70)
    
    # Règles communes
    print("\n📋 OBJECTIF :")
    print("   Deviner un mot secret de 8 lettres en un maximum de 6 tentatives")
    
    print("\n" + "═" * 70)
    print("\n🎯 COMMENT JOUER :")
     
    # Règles spécifiques selon le mode
    if nbr_joueurs == 1:
        print("\n   🤖 MODE 1 JOUEUR (Vous vs Ordinateur)")
        print("   " + "─" * 66)
        print("   • L'ordinateur choisit un mot secret de 8 lettres")
        print("   • La première lettre du mot vous est révélée")
        print("   • Vous devez deviner le mot en 6 tentatives maximum")
        
    elif nbr_joueurs == 2:
        print("\n   👥 MODE 2 JOUEURS (Joueur vs Joueur)")
        print("   " + "─" * 66)
        print("   • Le Joueur 1 choisit un mot secret de 8 lettres")
        print("   • Le Joueur 2 doit deviner le mot en 6 tentatives")
        print("   • La première lettre est révélée au Joueur 2")
    
    print("\n" + "═" * 70)
    print("\n💡 SYSTÈME D'INDICES :")
    print("\n   Après chaque proposition, chaque lettre est colorée :")
    print()
    print("   🟥 ROUGE  : Lettre bien placée (bonne position)")
    print("   🟨 JAUNE  : Lettre présente mais mal placée")
    print("   ⬜ GRIS   : Lettre absente du mot secret")
    
    print("\n" + "═" * 70)
    input("\n📌 Appuyez sur ENTRÉE pour continuer...")

# Affiche les catégories (première ligne du tableau)
def afficheCategorie(tab):
    taille = len(tab[0])
    for i in range(taille):
        print(i+1, ".", tab[0][i])

# Vérifie que l'input est un nombre valide
def verification(numDeb, numFin):
    while True:
        try:
            choix = int(input())
        except ValueError:
            print("❌ Veuillez entrer uniquement un chiffre")
        else:
            if choix < numDeb or choix > numFin:
                print(f"❌ Votre choix doit être compris entre {numDeb} et {numFin}")
            else:
                return choix

# Fonction qui demande le mot au joueur1 (jeu à 2) et l'enregistre en majuscule
def demanderMotJoueur(joueur1):
    while True:
        mot = input(f"\n{joueur1}, saisissez le mot secret (8 lettres) : ").strip()
        
        if mot == "":
            print("❌ Le mot ne peut pas être vide")
        elif " " in mot:
            print("❌ Le mot ne doit pas contenir d'espaces")
        elif not mot.isalpha():
            print("❌ Lettres uniquement (pas de chiffres)")
        elif len(mot) != 8:
            print(f"❌ 8 lettres exactement (vous: {len(mot)})")
        else:
            print("✅ le Mot est enregistré !")
            return mot.upper()

# Affiche le mot masqué (première lettre visible)
def afficherMotMasque(mot_secret):
    masque = mot_secret[0] + " _ " * 7
    print("Mot à deviner : ", masque)

# Compte les occurrences d'une lettre dans un mot
def compterOccurrences(mot, lettre):
    return mot.count(lettre)

# Analyse la proposition et retourne les états (ROUGE, JAUNE, GRIS)
def analyserProposition(mot_secret, proposition):
   
    etats = []
    for i in range(8):
        etats.append('GRIS')
    
    # Copier les lettres dans des tableaux pour pouvoir les modifier
    lettres_secret = []
    lettres_proposition = []
    for i in range(8):
        lettres_secret.append(mot_secret[i])
        lettres_proposition.append(proposition[i])
    
    # ÉTAPE 1 : Chercher les lettres ROUGES (bien placées)
    for i in range(8):
        if lettres_proposition[i] == lettres_secret[i]:
            etats[i] = 'ROUGE'
            lettres_secret[i] = '*'  # Marquer comme déjà utilisée
            lettres_proposition[i] = '*'
    
    # ÉTAPE 2 : Chercher les lettres JAUNES (mal placées)
    for i in range(8):
        if lettres_proposition[i] != '*':  
            # Chercher si la lettre existe ailleurs dans le mot secret
            for j in range(8):
                if lettres_secret[j] == lettres_proposition[i]:
                    etats[i] = 'JAUNE'
                    lettres_secret[j] = '*'  
                    break
    
    return etats

# Colore une lettre selon son état
def colorerLettre(lettre, etat):
    if etat == 'ROUGE':
        # Code pour rouge
        lettre_coloree = "\033[91m" + lettre + "\033[0m"
        return lettre_coloree
    elif etat == 'JAUNE':
        # Code pour jaune
        lettre_coloree = "\033[93m" + lettre + "\033[0m"
        return lettre_coloree
    else:
        # Code pour gris
        lettre_coloree = "\033[90m" + lettre + "\033[0m"
        return lettre_coloree

# Affiche une ligne colorée
def afficherLigneColoree(proposition, etats):
    ligne = ""
    for i in range(tailleMot):
        lettre = proposition[i]
        etat = etats[i]
        lettre_coloree = colorerLettre(lettre, etat)
        ligne = ligne + lettre_coloree + " "
    print(ligne)

# Affiche toute la grille des tentatives
def afficherGrille(historique):
    
    print("─" * 40)
    for i in range(len(historique)):
        proposition =  historique[i][0]
        etats = historique[i][1]
        print(f"Essai {i+1}: ", end="")
        afficherLigneColoree(proposition, etats)

# Valide une proposition
def validerProposition(proposition, mot_secret):
    if proposition == "":
        print("❌ La proposition ne peut pas être vide")
        return False
    elif " " in proposition:
        print("❌ Pas d'espaces dans la proposition")
        return False
    elif not proposition.isalpha():
        print("❌ Lettres uniquement")
        return False
    elif len(proposition) != 8:
        print(f"❌ Le mot doit contenir 8 lettres (vous: {len(proposition)})")
        return False
    return True

# Demande une proposition au joueur
def demanderProposition(mot_secret, tentative):
    while True:
        print(f" TENTATIVE {tentative}/{maxTentatives}")
        proposition = input(f"Proposez un mot commençant par '{mot_secret[0]}' : ").strip().upper()
        
        if validerProposition(proposition, mot_secret):
            return proposition
        
# Vérifie si le joueur a gagné
def verifierVictoire(proposition, mot_secret):
    return proposition == mot_secret

# Affiche le message de victoire
def afficherVictoire(tentatives):
    print(" " * 20 + "🏆 FÉLICITATIONS ! 🏆")
    print(f"\n✅ Vous avez trouvé le mot en {tentatives} tentative(s) !")
  

# Affiche le message de défaite
def afficherDefaite(mot_secret):
    
   
    print(f"\n Le mot était : {mot_secret}")
    print(" Vous ferez mieux la prochaine fois !")
   

# Lance une partie complète
def lancerPartie(mot_secret, joueur):
    print(f"  {joueur}, c'est parti ! Bonne chance !")
  
    
    afficherMotMasque(mot_secret)
    
    historique = []
    tentatives = 0
    
    
    
    
    while tentatives < maxTentatives:
        tentatives += 1
        
        if len(historique) > 0:
            afficherGrille(historique)
        
        proposition = demanderProposition(mot_secret, tentatives)
        etats = analyserProposition(mot_secret, proposition)#retourne un tableau avec rouge,jaune,gris
        historique.append((proposition, etats))
        
        
        print("\nRésultat : ", end="")
        afficherLigneColoree(proposition, etats)
        
        if verifierVictoire(proposition, mot_secret):
            afficherGrille(historique)
            afficherVictoire(tentatives)
            return True
    
    afficherGrille(historique)
    afficherDefaite(mot_secret)
    return False

# Demande si le joueur veut rejouer
def demanderRejouer():
    while True:
        reponse = input("\n🔄 Voulez-vous rejouer ? (O/N) : ").strip().upper()
        if reponse == 'O':
            return True
        elif reponse == 'N':
            return False
        else:
            print("❌ Réponse invalide. Tapez O (Oui) ou N (Non)")



# PARTIE PRINCIPALe

fileCsv = readFichier(open('./mot.csv', 'r'))
tailleLigne = len(fileCsv[0])
    

print(" " * 20 + "🎮 BIENVENUE DANS LE JEU DU MOTUS 🎮")


# Demander le nombre de joueurs
print("\nCombien de joueurs pour cette partie ?")
print("1. Un joueur (contre l'ordinateur)")
print("2. Deux joueurs")
nbr_joueurs = verification(1, 2)

# Demander les noms
if nbr_joueurs == 1:
    jj1 = demander_nom(1)
else:
    jj1 = demander_nom(1)
    jj2 = demander_nom(2)

# Menu règles ou démarrer
print("\nMenu :")
print("1. Afficher les règles du jeu")
print("2. Démarrer la partie")
choix = verification(1, 2)

if choix == 1:
    afficherRegles(nbr_joueurs)

# Démarrer la partie
if nbr_joueurs == 1:
    # Mode 1 joueur : choisir catégorie
    print("\nQuelle catégorie choisissez-vous ?")
    afficheCategorie(fileCsv)
    categorie = verification(1, tailleLigne)
    
    # Choisir un mot aléatoire
    mot_secret = motAleatoire(categorie, fileCsv)
    
    
    lancerPartie(mot_secret, jj1)

else:
    # Mode 2 joueurs : joueur 1 choisit le mot
    mot_secret = demanderMotJoueur(jj1)
    
  
    
    # Joueur 2 devine
    lancerPartie(mot_secret, jj2)

# Demander si rejouer
rejouer = demanderRejouer()

print("\n👋 Merci d'avoir joué ! À bientôt ! 🎮")
print("═" * 70)


    



    
 





import csv
from urllib import response
import requests
from math import*
import shutil
from functions import scrap_article, scrap_categories, scrap_site, creation_repertoire


url = "https://books.toscrape.com/index.html"


compteur_pourcent = 0 # variable pour la console, pour l'affichage du pourcentage 

shutil.rmtree('img_articles', ignore_errors=True) # efface le repertoire 'img_articles'
shutil.rmtree('scrap_CSV', ignore_errors=True) #  efface le repertoire 'scrap_CSV'

creation_repertoire('scrap_CSV') # création repertoire pour les fichiers CSV 
creation_repertoire('img_articles') # création repertoire pour les fichiers CSV

for e in scrap_site(url): # recupere les categorie présentent sur le site
    print("Catégorie : " + e[52:-13])

    nom_fichier = "scrap_CSV/" + e[52:-13] + ".csv" # creation du nom des fichiers
    entete = ["product_page_url","universal_ product_code (upc)",
              "title","price_including_tax","price_excluding_tax",
              "number_available","product_description","category",
              "review_rating","image_url"] # liste avec les informations de l'entete


    with open( nom_fichier,"a+", newline='',encoding="UTF8") as ligne_un: #cree le fichier et l'entete
        csvwriter = csv.writer(ligne_un)
        csvwriter.writerow(entete)

        for n in scrap_categories(e): # pour chaques catégories, recupere les URL de tous les articles
            print("Livre scrapé : " + n[37:-15]) 

            liste_infos_articles = [] # reset de la liste sur le scrap d'article

            compteur_pourcent += 1
            
            print("Avancée scraping : " + str(compteur_pourcent/10) + "%") # affiche le pourcentage d'avncement

            for d in scrap_article(n): # avec l'URL de chaques article, recupere les informations de l'article

                liste_infos_articles.append(d) # met les info de l'article dans une liste pour les ajouter au tableau apres
                
            csvwriter.writerow(liste_infos_articles) # ajoute les lignes scrapees

            # ---------------------
            # ---- scrap image ----
            # ---------------------

            creation_repertoire("img_articles/" + liste_infos_articles[7]) # création repertoire pour les images 
            
            if len(liste_infos_articles[0][37:-15]) > 120 : # diminue les noms trop long pour qu'ils puissent être écris si limitation sur longueure
                f = open("img_articles/" + liste_infos_articles[7] + "/" + str(compteur_pourcent) + "_" + liste_infos_articles[0][37:-65] + ".jpg",'wb') # nomage et chemin
            else :
                f = open("img_articles/" + liste_infos_articles[7] + "/" + str(compteur_pourcent) + "_" + liste_infos_articles[0][37:-15] + ".jpg",'wb') # nomage et chemin
            
            response = requests.get(liste_infos_articles[9]) # recuperation du .jpg 
            f.write(response.content) # ecriture du .jpg
            f.close()
            
       


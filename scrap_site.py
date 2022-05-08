import csv
from math import*
import shutil
from functions import scrap_article, scrap_categories, scrap_site, creation_repertoire


url = "https://books.toscrape.com/index.html"


#liste_infos_articles = []
compteur_pourcent = 0

shutil.rmtree('img_articles', ignore_errors=True) # efface le repertoire 'img_articles'
shutil.rmtree('scrap_CSV', ignore_errors=True) # efface le repertoire 'scrap_CSV'

creation_repertoire('scrap_CSV')

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
            
            print("Avancée scraping : " + str(compteur_pourcent/10) + "%") # retour console sur l'avancement

            for d in scrap_article(n): # avec l'URL de chaques article, recupere les informations de l'article 

                liste_infos_articles.append(d) # met les info de l'article dans une liste pour les ajouter au tableau apres
                
            csvwriter.writerow(liste_infos_articles) # ajoute les lignes scrapees
            

       


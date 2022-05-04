import csv
import requests
from bs4 import BeautifulSoup
import shutil
from functions import scrap_article, creation_repertoire # importation des mes fonctions

shutil.rmtree('img_articles', ignore_errors=True) # efface le repertoire 'img_articles' existant
shutil.rmtree('scrap_CSV', ignore_errors=True) # # efface le repertoire 'scrap_CSV' existant


url_article = "https://books.toscrape.com/catalogue/bitch-planet-vol-1-extraordinary-machine-bitch-planet-collected-editions_882/index.html"


response =  requests.get(url_article) #objet requete dans 'response'
soup = BeautifulSoup(response.text, 'lxml') #lxml pour le parseur 

article_scrap = scrap_article(url_article) #recuperation des informations d'un article

# ---- Retour console sur le scrap ---
print("UPC : " + article_scrap[1] + "\n" +
      "Titre : " + article_scrap[2] + "\n" +
      "Prix avec taxes : " + article_scrap[3] + "\n" +
      "Prix hors taxes : " + article_scrap[4] + "\n" +
      "Stocks : " + article_scrap[5] + "\n" +
      "Desciption du produit : " + article_scrap[6] + "\n" +
      "Genre : " + article_scrap[7] + "\n" +
      "Note : " + article_scrap[8] + "\n" +
      "Url de l'image : " + article_scrap[9])

# --------------------------------------------------------------------
# -------------------------------- CSV -------------------------------
# --------------------------------------------------------------------

nom_fichier = "scrap_CSV/" + article_scrap[2].replace(":"," ") + ".csv" # creation du nom des fichiers

entete = ["product_page_url","universal_ product_code (upc)",
          "title","price_including_tax","price_excluding_tax",
          "number_available","product_description","category",
          "review_rating","image_url"] # liste avec les informations de l'entete

info_page = [article_scrap[0],article_scrap[1],article_scrap[2],
             article_scrap[3],article_scrap[4],article_scrap[5],
             article_scrap[6],article_scrap[7],article_scrap[8],
             article_scrap[9]] # creation d'une liste avec les informations recuperees au dessus

creation_repertoire('scrap_CSV')

with open( nom_fichier,"a+", newline='',encoding="UTF8") as file_object: #ecrit un fichier CSV avec les informations d'une page
    csvwriter = csv.writer(file_object)
    csvwriter.writerow(entete)
    csvwriter.writerow(info_page)





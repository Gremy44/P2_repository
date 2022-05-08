import csv
from math import*
import shutil
from functions import scrap_article, scrap_categories,creation_repertoire


url_category = "https://books.toscrape.com/catalogue/category/books/childrens_11/index.html"


shutil.rmtree('img_articles', ignore_errors=True) # efface le repertoire 'img_articles'
shutil.rmtree('scrap_CSV', ignore_errors=True) # efface le repertoire 'scrap_CSV'

lst_url_articles = scrap_categories(url_category) # recupere la liste des url d'une categorie dans la liste lst_url_artciles

print("Liens de la categorie scrapee :") # retour console de la liste des url d'une categorie
for i in lst_url_articles:
    print(i)


# --------------------------------------------------------------------
# -------------------------------- CSV -------------------------------
# --------------------------------------------------------------------

nom_fichier = "scrap_CSV/" + scrap_article(lst_url_articles[0])[7] + ".csv" # creation du nom des fichiers
entete = ["product_page_url","universal_ product_code (upc)",
          "title","price_including_tax","price_excluding_tax",
          "number_available","product_description","category",
          "review_rating","image_url"] # liste avec les informations de l'entete

creation_repertoire('scrap_CSV')

print("")
print("Chargement des elements du fichier CSV en cours...") # retour console pour l'avance

with open( nom_fichier,"a+", newline='',encoding="UTF8") as file_object: # creation fichier CSV
    csvwriter = csv.writer(file_object)
    csvwriter.writerow(entete)

    for page in lst_url_articles:#remplis chaques lignes avec les valeurs de la list lst_url_articles
        csvwriter.writerow(scrap_article(page))

# retour console pour l'avance
print("\nCategorie scrapee\n")
 




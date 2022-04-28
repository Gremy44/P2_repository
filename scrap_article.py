import csv
import requests
from bs4 import BeautifulSoup
import lxml
import os

def rating_convert(rate): # converti la note en anglais => francais avec chiffre
    rating = 0
    if rate == "One":
        rating = "1 étoile"
    elif rate == "Two":
        rating = "2 étoiles"
    elif rate == "Three":
        rating = "3 étoiles"
    elif rate == "Four":
        rating = "4 étoiles"
    else:
        rating = "5 étoiles"
    return str(rating)

url_article = "https://books.toscrape.com/catalogue/bitch-planet-vol-1-extraordinary-machine-bitch-planet-collected-editions_882/index.html"

response =  requests.get(url_article) #objet requete dans 'response'
soup = BeautifulSoup(response.text, 'lxml') #lxml pour le parseur 

# ---- Exctraction product_page_url ---- 
product_page_url = url_article

# ---- Exctraction universal_ product_code ----
universal_product_code = soup.findAll("td")[0].text

# ---- Exctraction title ----
title = soup.find("ul",{"class":"breadcrumb"}).findAll("li",{"class":"active"})[0].text.replace("," , " ") # extrait la valeur de la liste, retire les balises, remplace les "," par des espaces si présentent pour csv

# ---- Exctraction price_including_tax ----
price_including_tax = soup.findAll("td")[2].text[1:] # extrait le valeur a l'index [2] de la list, retire les balises, slice le premier caratère de la chaine car illisible

# ---- Exctraction price_excluding_tax ----
price_excluding_tax = soup.findAll("td")[3].text[1:] # extrait le valeur a l'index [3] de la list, retire les balises, slice le premier caratère de la chaine car illisible

# ---- Exctraction number_available ----
number_available = soup.findAll("td")[5].text # extrait le valeur a l'index [5] de la list, retire les balises

# ---- Exctraction product_description ---- 
product_description = soup.findAll("p")[3].text.replace("," , " ")# extrait le valeur a l'index [3] de la list, retire les balises, remplace les "," par des espaces si présentent pour csv

# ---- Exctraction category ----
category = soup.find("ul",{"class":"breadcrumb"}).findAll("a")[2].text

# ---- Exctraction review_rating ----
rate = soup.find("div",{"class":"col-sm-6 product_main"}).findAll("p")[2].get("class")[1]
review_rating = rating_convert(rate) # passe dans la fonction rating_convert pour traduire le nombre d'étoile

# ---- Exctraction image_url ----
image_url = "http://books.toscrape.com/" + soup.findAll("img")[0].get("src")[6:] # création de l'url de l'image

print("Url du livre : " + product_page_url)
print("UPC : " + universal_product_code)
print("Titre : " + title)
print("Prix avec taxes : " + price_including_tax)
print("Prix hors taxes : " + price_excluding_tax)
print("Stocks : " + number_available)
print("Desciption du produit : " + product_description)
print("Genre : " + category)
print("Note : " + review_rating)
print("Url de l'image : " + image_url)

# --------------------------------------------------------------------
# -------------------------------- CSV -------------------------------
# --------------------------------------------------------------------
nom_fichier = "scrap_CSV/" + title.replace(":"," ") + ".csv"
entete = ["product_page_url","universal_ product_code (upc)","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url"]
info_page = [product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url]

'''if not os.path.exists('/mydirectory'):
    os.makedirs('scrap_CSV')'''

try:
    os.makedirs('scrap_CSV')
except FileExistsError:
    pass
    
with open( nom_fichier,"a+", newline='',encoding="UTF8") as file_object: #ecrit un fichier CSV Pour chacune des catégories
    csvwriter = csv.writer(file_object)
    csvwriter.writerow(entete)
    csvwriter.writerow(info_page)

print(nom_fichier)




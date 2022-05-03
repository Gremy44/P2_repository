import csv
import requests
from bs4 import BeautifulSoup
import lxml
from math import*
import os


url = "https://books.toscrape.com/index.html"


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

def scrap_article(url_article): # retourne les information d'un livre
    
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
    
    if product_description.isspace():
        product_description = "Pas de description"
    
    # ---- Exctraction category ----
    category = soup.find("ul",{"class":"breadcrumb"}).findAll("a")[2].text

    # ---- Exctraction review_rating ----
    rate = soup.find("div",{"class":"col-sm-6 product_main"}).findAll("p")[2].get("class")[1]
    review_rating = rating_convert(rate) # passe dans la fonction rating_convert pour traduire le nombre d'étoile

    # ---- Exctraction image_url ----
    image_url = "http://books.toscrape.com/" + soup.findAll("img")[0].get("src")[6:] # création de l'url de l'image

    return product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating,image_url

def scrap_categories(url_category): # retourne une liste des URL d'une categorie 
    #url_category = "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"

    response =  requests.get(url_category) # requete
    soup = BeautifulSoup(response.text, 'lxml') # requete

    lst_url_articles = []

    page_nb_livres = int(soup.find("form",{"class":"form-horizontal"}).findAll("strong")[0].text) # retourne le nombre d'elements par page
    page_nb_pages = ceil(int(page_nb_livres)/20) # retourne le nombre de pages 

    if page_nb_livres <= 20 :#page de moins de 20 ou 20 livres

        for link in soup.find_all("div",{"class":"image_container"}): #retourne une liste avec toutes les URL des livres de la page
            
            lst_url_articles.append("https://books.toscrape.com/catalogue" + link.find("a")["href"][8:])

    else : #pages de plus de 20 livres
        for i in range(0,page_nb_pages):#genere les nouvelles url et envoi une nouvelle requete a chaque nouvelle iteration
            
            url_category_nvl = url_category[:-11] + "/page-" + str(i+1) + ".html" # cree la nouvelle URL

            response =  requests.get(url_category_nvl) # nouvelle requete avec le nouveau nom de page
            soup = BeautifulSoup(response.text, 'lxml') # nouvelle requete avec le nouveau nom de page    

            for link in soup.find_all("div",{"class":"image_container"}): #retourne une liste avec toutes les URL des livres de la page
                
                lst_url_articles.append("https://books.toscrape.com/catalogue" + link.find("a")["href"][8:])    
                
                info_page = "https://books.toscrape.com/catalogue" + link.find("a")["href"][8:]

                #retourne lst_url_articles, une liste de toutes les URL pour une categorie
    
    return lst_url_articles

def scrap_site(url): # retourne une liste des URL de chaque genre

    response =  requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    genre = []

    for link in range(51):
        #print("https://books.toscrape.com/" + soup.find("ul",{"class":"nav nav-list"}).findAll("a")[link]["href"])
        genre.append("https://books.toscrape.com/" + soup.find("ul",{"class":"nav nav-list"}).findAll("a")[link]["href"])
    
    genre = genre[1:] # enleve l'index de la liste 

    return genre

def creation_repertoire(chemin_repertoire): # cree un repertoire avec le chemin en argument
    try:
        os.makedirs(chemin_repertoire)
    except FileExistsError:
        pass


liste_infos_articles = []
compteur_pourcent = 0 # variable pour la console, pour l'affichage du pourcentage 

creation_repertoire('scrap_CSV') # création repertoire pour les fichiers CSV 

for e in scrap_site(url):
    print("Catégorie : " + e[52:-13])

    nom_fichier = "scrap_CSV/" + e[52:-13] + ".csv"
    entete = ["product_page_url","universal_ product_code (upc)","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url"]

    with open( nom_fichier,"a+", newline='',encoding="UTF8") as ligne_un: #cree le fichier et l'entete
        csvwriter = csv.writer(ligne_un)
        csvwriter.writerow(entete)

    for n in scrap_categories(e):
        print("Livre scrapé : " + n[37:-15]) 

        liste_infos_articles = [] # reset de la liste sur le scrap d'article

        compteur_pourcent += 1
        
        print("Avancée scraping : " + str(compteur_pourcent/10) + "%") # affiche le pourcentage d'avncement

        for d in scrap_article(n):

            liste_infos_articles.append(d)
            
        with open( nom_fichier,"a+", newline='',encoding="UTF8") as ligne_deux: #cree les lignes d'apres
            csvwriter = csv.writer(ligne_deux)
            csvwriter.writerow(liste_infos_articles)

        # scrap image 

        creation_repertoire("img_articles/" + liste_infos_articles[7]) # création repertoire pour les images 
        
        if len(liste_infos_articles[0][37:-15]) > 120 : # diminue les noms trop long pour qu'ils puissent être écris 
            f = open("img_articles/" + liste_infos_articles[7] + "/" + str(compteur_pourcent) + "_" + liste_infos_articles[0][37:-65] + ".jpg",'wb') # nomage et chemin
        else :
            f = open("img_articles/" + liste_infos_articles[7] + "/" + str(compteur_pourcent) + "_" + liste_infos_articles[0][37:-15] + ".jpg",'wb') # nomage et chemin
        
        response = requests.get(liste_infos_articles[9]) # recuperation de l'URL de l'image
        f.write(response.content)
        f.close()
       


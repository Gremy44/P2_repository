import csv
from distutils.filelist import findall
from distutils.log import info
from unicodedata import category
import requests
from bs4 import BeautifulSoup
from soupsieve import escape

url = "https://books.toscrape.com/index.html"
url_2 = "https://books.toscrape.com/catalogue/category/books/romance_8/index.html"
url_3 = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

def scraping(url): # retourne 1 list de 10 élements / Prend url de cat_to_page

    #url = "http://books.toscrape.com/catalogue/rip-it-up-and-start-again_986/index.html"
    str_product_description = ""

    response =  requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    #--extraction url--
    #print("URL : ",url)
        
    #--extraction UPC--
    universal_product_code = soup.findAll("td")
    #print("UPC :", universal_product_code[0].text)

    #--extraction titre--
    title_lst = soup.find("ul",{"class":"breadcrumb"}).findAll("li",{"class":"active"})
    title = title_lst[0]
    title = title.text
    title = title.replace("," , " ")
    #print("Title : ", title.text)

    #--extraction price_including_tax--
    price_including_tax = universal_product_code[2]
    #print("Price including tax : ", price_including_tax.text[1:])

    #--extraction price_excluding_tax--
    price_excluding_tax = universal_product_code[3]
    #print("Price excluding tax : ", price_excluding_tax.text[1:])

    #--extraction number_available--
    number_available = universal_product_code[5]
    #print("Number_available : ", number_available.text)

    #--extraction product_description--
    product_description_lst = soup.findAll("p")
    product_description = product_description_lst[3]
    product_description = product_description.text
    product_description = product_description.replace("," , " ")
        
    #print("Product_description : ", product_description)
    #print(type(product_description))
    #--extraction category--
    category = soup.find("ul",{"class":"breadcrumb"}).findAll("a")
    #print("Category :", category[2].text)

    #--extraction review_rating--
    review_rating_full = soup.find("div",{"class":"col-sm-6 product_main"}).findAll("p")
    review_rating_str = review_rating_full[2].get("class")
        
    #Conversion string en chiffre
    #print("Review_Rating :",rating_convert(review_rating_str))

    #--extraction image_url--
    image_url_full = soup.findAll("img")

    image_url = image_url_full[0].get("src")
        
    image_url = image_url[6:] # retrait des 6 premiers caracteres de l'url pour concatenation

    image_url = "http://books.toscrape.com/"+ image_url

    #print("image_url : ",image_url)

    return url, universal_product_code[0].text, title, price_including_tax.text[1:],price_excluding_tax.text[1:], number_available.text,product_description, category[2].text, rating_convert(review_rating_str), image_url

def rating_convert(rate):
    rating = 0
    if rate[1] == "One":
        rating = 1
    elif rate[1] == "Two":
        rating = 2
    elif rate[1] == "Tree":
        rating = 3
    elif rate[1] == "Four":
        rating = 4
    else:
        rating = 5
    return str(rating)

def id_page(url):

    response =  requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    results = soup.find("form",{"class":"form-horizontal"}).findAll("strong")

    results = results[0].text

    results = int(results)

    #ID page sera l'id de la page dans l'url
    if results%20 != 0 : 
        id_page = int(results/20+1)
        
    else :
        id_page = int(results/20)
        
    
    return id_page,results

def scrap_pages(url_3): # retourne 2 list : lien de chacunes des pages de tout le site / Catégories + page / Prend : url = "http://books.toscrape.com/index.html" en argument

    #url = "http://books.toscrape.com/index.html"

    liste_pages = []
    info_pages = []

    id_page_res_1 = id_page(url_3)

    #inc_01 = 1
    #print(id_page_res_1)

    response =  requests.get(url_3)

    soup = BeautifulSoup(response.text, 'lxml')

    genre = soup.find("ul",{"class":"nav nav-list"}).findAll("a")
    genre_page =[]
    nb_page = []

    id_page_res_1 = id_page(url_3)

    inc_02 = 1 #compteur categories

    
    for i in genre:

        i = i.text
        i = i.replace(" ","-") #remplacement des espaces par des "-"
        i = i[62:-53] #retrait des '-' sur les côtés
        i = i.replace("\n","") # suppression des retours à la ligne 
        i = i.lower() #passe la chaine en minuscules

        #condition pour le premier style de livre qui n'a pas le mot'book' dans son URL
        if inc_02 == 1:
            url_3 = "http://books.toscrape.com/catalogue/category/" + i + "_" + str(inc_02) + "/index.html"
        else:
            url_3 = "http://books.toscrape.com/catalogue/category/books/" + i + "_" + str(inc_02) + "/index.html" 
            
        id_page_res_1 = id_page(url_3)

        if inc_02 > 1 and id_page_res_1[1] > 20 : # Renome les page avec plus de 20 livres pour rechercher les autres pages 
            url_3 = "http://books.toscrape.com/catalogue/category/books/" + i + "_" + str(inc_02) + "/page-1.html"

            for a in range(id_page_res_1[0]): # quand plusieurs pages, les ressort
                url_3 = "http://books.toscrape.com/catalogue/category/books/" + i + "_" + str(inc_02) + "/page-"+ str(a+1) + ".html"
                genre_page.append(i + " page " + str(a+1))
                if genre != 'http://books.toscrape.com/catalogue/category/books_1/index.html':
                    liste_pages.append(url_3)
                     

            #if genre != 'http://books.toscrape.com/catalogue/category/books_1/index.html':
                #liste_pages.append(url_3)
                #genre_page.append(i + " page 1")
                #nb_page.append(id_page_res_1[0])
            
            
        else :
            url_3 = "http://books.toscrape.com/catalogue/category/books/" + i + "_" + str(inc_02) + "/index.html"
            liste_pages.append(url_3)
            genre_page.append(i + " page 1")
            nb_page.append(id_page_res_1[0])

        #info_pages = [genre_page,liste_pages,nb_page]
        info_pages = liste_pages

        inc_02 += 1

        #print(info_pages)
    return info_pages, genre_page # retourne 2 list : lien de chacunes des pages de tout le site / Catégories + page  

def cat_to_page(url_2): # Retourne 1 list : lien de chacun des livres d'une page / Prend l'url de scrap_page

    url_livre=[]
    lst_url_livre = []
    livres = []

    response =  requests.get(url_2)

    soup = BeautifulSoup(response.text, 'lxml') 

    for link in soup.find_all("div",{"class":"image_container"}):#recupere le href des a
        url_livre = link.find("a")
        lst_url_livre = url_livre["href"]

        lst_url_livre = lst_url_livre[8:]#suppression des caractères inutiles
        lst_url_livre = "https://books.toscrape.com/catalogue" + lst_url_livre #reconstitution de l'url

        livres.append(lst_url_livre)#creation de la liste avec les urls
        #print(lst_url_livre)
        
    return livres # retourne la liste des livres par categorie


categorie = scrap_pages(url)[1]
url_1 = scrap_pages(url)[0] # liste pages global du site 

info_livre = []
entete = ["product_page_url","universal_ product_code (upc)","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url"]

for index_01 in range(len(url_1)): # boucle sur le nombre de pages contenue sur le site 
    cat = categorie[index_01]
    with open(categorie[index_01] +".csv", "a+", encoding="UTF8") as file_object: #ecrit un fichier CSV Pour chacune des catégories
        csvwriter = csv.writer(file_object)
        csvwriter.writerow(cat)
        csvwriter.writerow(entete)
    
    url_11 = url_1[index_01]
    pages_livre = cat_to_page(url_11) # liste url par categorie 

    for index_02 in range(len(pages_livre)): # boucle le nombre de livres par categorie

        url_12 = pages_livre[index_02]
        livres = scraping(url_12)

        with open(categorie[index_01] +".csv", "a+", newline='', encoding="UTF8") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(livres)

        print(livres)
        

    
    
    
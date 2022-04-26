import csv
import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/index.html"

#fonction de convertion des note lettre/chiffre
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
    return rating

def scraping(url):

    #url = "http://books.toscrape.com/catalogue/rip-it-up-and-start-again_986/index.html"

    response =  requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    #--extraction url--
    print("URL : ",url)
        
    #--extraction UPC--
    universal_product_code = soup.findAll("td")
    print("UPC :", universal_product_code[0].text)

    #--extraction titre--
    title_lst = soup.find("ul",{"class":"breadcrumb"}).findAll("li",{"class":"active"})
    title = title_lst[0]
    print("Title : ", title.text)

    #--extraction price_including_tax--
    price_including_tax = universal_product_code[2]
    print("Price including tax : ", price_including_tax.text[1:])

    #--extraction price_excluding_tax--
    price_excluding_tax = universal_product_code[3]
    print("Price excluding tax : ", price_excluding_tax.text[1:])

    #--extraction number_available--
    number_available = universal_product_code[5]
    print("Number_available : ", number_available.text)

    #--extraction product_description--
    product_description_lst = soup.findAll("p")
    product_description = product_description_lst[3]
    print("Product_description : ", product_description.text)

    #--extraction category--
    category = soup.find("ul",{"class":"breadcrumb"}).findAll("a")
    print("Category :", category[2].text)

    #--extraction review_rating--
    review_rating_full = soup.find("div",{"class":"col-sm-6 product_main"}).findAll("p")
    review_rating_str = review_rating_full[2].get("class")
        
    #Conversion string en chiffre
    print("Review_Rating :",rating_convert(review_rating_str))

    #--extraction image_url--
    image_url_full = soup.findAll("img")

    image_url = image_url_full[0].get("src")
        
    image_url = image_url[6:] # retrait des 6 premiers caracteres de l'url pour concatenation

    image_url = "http://books.toscrape.com/"+ image_url

    print("image_url : ",image_url)

    return url, universal_product_code[0].text, title.text, price_including_tax.text[1:],price_excluding_tax.text[1:], number_available.text,product_description.text, category[2].text, rating_convert(review_rating_str), image_url

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

def scrap_pages(url):
    #url = "http://books.toscrape.com/index.html"

    liste_pages = []
    info_pages = []

    id_page_res_1 = id_page(url)

    #inc_01 = 1
    #print(id_page_res_1)

    response =  requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    genre = soup.find("ul",{"class":"nav nav-list"}).findAll("a")

    id_page_res_1 = id_page(url)

    inc_02 = 1 #compteur categories

    
    for i in genre:

        i = i.text
        i = i.replace(" ","-") #remplacement des espaces par des "-"
        i = i[62:-53] #retrait des '-' sur les côtés
        i = i.replace("\n","") # suppression des retours à la ligne 
        i = i.lower() #passe la chaine en minuscules

        #condition pour le premier style de livre qui n'a pas le mot'book' dans son URL
        if inc_02 == 1:
            url = "http://books.toscrape.com/catalogue/category/" + i + "_" + str(inc_02) + "/index.html"
        else:
            url = "http://books.toscrape.com/catalogue/category/books/" + i + "_" + str(inc_02) + "/index.html" 
            
        id_page_res_1 = id_page(url)

        if inc_02 > 1 and id_page_res_1[1] > 20 : # Renome les page avec plus de 20 livres pour rechercher les autres pages 
            url = "http://books.toscrape.com/catalogue/category/books/" + i + "_" + str(inc_02) + "/page-1.html"

            for a in range(id_page_res_1[0]): # quand plusieurs pages, les ressort
                url = "http://books.toscrape.com/catalogue/category/books/" + i + "_" + str(inc_02) + "/page-"+ str(a+1) + ".html"
                if genre != 'http://books.toscrape.com/catalogue/category/books_1/index.html':
                    liste_pages.append(url)
                    
                    
            if genre != 'http://books.toscrape.com/catalogue/category/books_1/index.html':
                liste_pages.append(url)

            info_pages = [i,liste_pages]

        inc_02 += 1
    return info_pages
    

''' FIchier csv
#creation fichier csv
with open('Scraping_book_to_scrap.csv','w') as f:

    retour = scraping("http://books.toscrape.com/catalogue/rip-it-up-and-start-again_986/index.html")

    f.write("url, universal_product_code, title.text, price_including_tax,price_excluding_tax, number_available,product_description, category, review_rating, image_url \n")

    for i in retour:
        f.write(str(i)+', ')'''
''' Recuperation genres

url = "http://books.toscrape.com/index.html"

response =  requests.get(url)

soup = BeautifulSoup(response.text, 'lxml')

genre = soup.find("ul",{"class":"nav nav-list"}).findAll("a")

print("Genre : ", genre[3].text)'''
'''url = "http://books.toscrape.com/catalogue/category/books/fantasy_19/page-1.html"

response =  requests.get(url)

soup = BeautifulSoup(response.text, 'lxml')

#print(id_page(url))

livres_liste = []

#liste contenant le nom des livre
'''
'''for n in range(id_page(url)):
    url = url[:-6]
    url = url + str(n+1) + ".html" 
    response =  requests.get(url)
    nb_livres = id_page(url)
    for i in range(20) : # tourne 20x car 20 livres par page 
        soup = BeautifulSoup(response.text, 'lxml')
        url_livres = soup.find("ol",{"class":"row"}).findAll("a") # recupère en gros
        url_livres_href = url_livres[i*2].get("href") # récupère l'url compressé
        url_livres_href = url_livres_href[8:] # retire les ../.. au début
        url_livres_href = "http://books.toscrape.com" + url_livres_href # ajoute le début de l'url
        print(url_livres_href)
        #url = url_livres_href
        #livres_liste.append(url_livres_href) # ajoute chaque nom à la liste livres_liste[]'''
'''for i in range(id_page_res_1[1]):

    response =  requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    url_livres = soup.find("ol",{"class":"row"}).findAll("a") # recupère en gros
    url_livres_href = url_livres[i%20*2].get("href") # récupère l'url compressé
    url_livres_href = url_livres_href[8:] # retire les ../.. au début
    url_livres_href = "http://books.toscrape.com/catalogue" + url_livres_href # ajoute le début de l'url
    print(url_livres_href)
    n = (i+1)%21
    print(n)

    #response =  requests.get(url_livres_href)
    #soup = BeautifulSoup(response.text, 'lxml')

    if n == 20:
        url = url[:-6]
        url = url + str(inc_01+1) + ".html" 
        response =  requests.get(url)
        inc_01 += 1
        print("passe dans le if")
        print(url)
        print(inc_01)
        #nb_livres = id_page(url)
'''

print(scrap_pages(url))

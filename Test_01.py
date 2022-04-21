from calendar import c
import csv
from ctypes import cdll
from this import d
from tkinter import E
import requests
from bs4 import BeautifulSoup

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
    ##print("URL : ",url)
        
    #--extraction UPC--
    universal_product_code = soup.findAll("td")
    ##print("UPC :", universal_product_code[0].text)

    #--extraction titre--
    title_lst = soup.find("ul",{"class":"breadcrumb"}).findAll("li",{"class":"active"})
    title = title_lst[0]
    ##print("Title : ", title.text)

    #--extraction price_including_tax--
    price_including_tax = universal_product_code[2]
    ##print("Price including tax : ", price_including_tax.text[1:])

    #--extraction price_excluding_tax--
    price_excluding_tax = universal_product_code[3]
    ##print("Price excluding tax : ", price_excluding_tax.text[1:])

    #--extraction number_available--
    number_available = universal_product_code[5]
    ##print("Number_available : ", number_available.text)

    #--extraction product_description--
    product_description_lst = soup.findAll("p")
    product_description = product_description_lst[3]
    ##print("Product_description : ", product_description.text)

    #--extraction category--
    category = soup.find("ul",{"class":"breadcrumb"}).findAll("a")
    ##print("Category :", category[2].text)

    #--extraction review_rating--
    review_rating_full = soup.find("div",{"class":"col-sm-6 product_main"}).findAll("p")
    review_rating_str = review_rating_full[2].get("class")
        
    #Conversion string en chiffre
    ##print("Review_Rating :",rating_convert(review_rating_str))

    #--extraction image_url--
    image_url_full = soup.findAll("img")

    image_url = image_url_full[0].get("src")
        
    image_url = image_url[6:] # retrait des 6 premiers caracteres de l'url pour concatenation

    image_url = "http://books.toscrape.com/"+ image_url

    ##print("image_url : ",image_url)

    return url, universal_product_code[0].text, title.text, price_including_tax.text[1:],price_excluding_tax.text[1:], number_available.text,product_description.text, category[2].text, rating_convert(review_rating_str), image_url

#creation fichier csv
with open('Scraping_book_to_scrap.csv','w') as f:

    retour = scraping("http://books.toscrape.com/catalogue/rip-it-up-and-start-again_986/index.html")

    f.write("url, universal_product_code, title.text, price_including_tax,price_excluding_tax, number_available,product_description, category, review_rating, image_url \n")

    for i in retour:
        f.write(str(i)+', ')

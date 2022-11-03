import streamlit as st
import requests
from bs4 import BeautifulSoup as bs
import unidecode
import csv
import urllib.request
from .Image import get_link_image
import csv



def get_url_horror(url_horror):  # fonction recupére la page catégorie horror
    # Telechargement de la page url horror
    page = requests.get(url_horror)
    # création de l'objet Soup
    soup = bs(page.text, "lxml")
    return soup


def get_all_links_book_to_horror(soup):
    # Récupération de tous les liens des livres dans la catégorie horror
    links_horror = []
    listings = soup.find_all(class_="product_pod")
    # A partir de chaques liens récupérer on peut obtenir le lien de livres
    for listing in listings:
        target_lnk_horror = listing.find("h3").a.get("href")
        base_url = "https://books.toscrape.com/catalogue/category/books/horror_31/"
        complete_lnk = base_url + target_lnk_horror
        # print(complete_lnk) # A partir de là nous avons tous les liens pour les livres répétorier sur la page actuelle
        links_horror.append(complete_lnk)
    return links_horror

def info_extract(links_horror,all_books_horror):
    # Extraire les informations de chaques livres dans horror
    for link_horror in links_horror:
        response_info_horror = requests.get(link_horror).text
        book_soup = bs(response_info_horror, "lxml")
        product_page_url = link_horror
        table = book_soup.findAll('td')
        title = book_soup.find('h1').text
        universal_product_code = table[0].text
        price_including_tax = table[2].text.replace('£', '£').replace('Â', '')
        price_excluding_tax = table[3].text.replace('£', '£').replace('Â', '')
        number_available = table[5].text.removeprefix('In stock (').removesuffix('available)')
        product_description_unicode = book_soup.select_one('article > p').text
        product_description = unidecode.unidecode(product_description_unicode)
        category = book_soup.find('ul', class_="breadcrumb").findAll('a')[2].text
        review_rating = book_soup.find('p', class_='star-rating').get('class').pop()
        image = book_soup.find('div', class_="item active").find('img')

        book_horror = {"product_page_url": product_page_url,
                       "title": title,
                       "product_description": product_description,
                       "universal_product_code": universal_product_code,
                       "price_including_tax": price_including_tax,
                       "price_excluding_tax": price_excluding_tax,
                       "category": category,
                       "review_rating": review_rating,
                       "image": image['src'],
                       "number_available": number_available}
        # "number_available":number_available}
        all_books_horror.append(book_horror)
    return all_books_horror



def etape2(url_horror):
    st.subheader("📚 🧛  Catégorie HORROR 🧛 📚")
    # -- Création variable : un tableau avec tous les livres dedans
    all_books_horror = []
    all_links_horror = get_all_links_book_to_horror(get_url_horror(url_horror))
    all_books_horror = info_extract(all_links_horror, all_books_horror)
    print("h")

    # --------------- Fichier CSV pour la catg Horror  -----------------
    # Créer une liste pour les en-têtes
    en_tete_horror = ['product_page_url',
                      'title',
                      'product_description',
                      'universal_product_code',
                      'price_including_tax',
                      'price_excluding_tax',
                      'category',
                      'review_rating',
                      'image',
                      'number_available']

    # Créer un nouveau fichier pour écrire dans le fichier appelé « data.csv »
    with open('Horror/data_horror.csv', 'w') as fichier_csv:
        # Créer un objet writer (écriture) avec ce fichier
        writer = csv.writer(fichier_csv, delimiter=';')
        writer.writerow(en_tete_horror)


        # Boucle en passant les param's !
        for books_horror in all_books_horror:
            writer.writerow([books_horror['product_page_url'],
                             books_horror['title'],
                             books_horror['product_description'],
                             books_horror['universal_product_code'],
                             books_horror['price_including_tax'],
                             books_horror['price_excluding_tax'],
                             books_horror['category'],
                             books_horror['review_rating'],
                             get_link_image(books_horror, 2),
                             books_horror['number_available']])
        print("hello")

        image_url = get_link_image(books_horror, 2)
        filename = 'Horror/' + books_horror['title'].replace("?", "") + ".jpg"
        urllib.request.urlretrieve(image_url, filename)
    clé2 = "2"


    with open('Horror/data_horror.csv') as g:
        button =  st.download_button(label='Download Horror CSV', data=open('Horror/data_horror.csv'), file_name='data_horror.csv',
                       mime='text/csv', key=clé2)
    #     st.download_button(label = 'Heloise', data = g, file_name='data_horror.csv', mime='text/csv', key= clé2)
        st.text("💾 🧛  Votre fichier CSV sur la catégorie HORROR viens d'être crée.")
        st.text("Vous pouvez le télécharger !")

    #print(" 💾 🧛  Votre fichier CSV sur la catégorie HORROR viens d'être crée. Vous pouvez le télécharger !")





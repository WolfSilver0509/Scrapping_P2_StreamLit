import requests
from bs4 import BeautifulSoup as bs
import unidecode
import csv
import urllib.request

from .Image import get_link_image



def get_url_category(url_category):  # fonction recupére la page catégorie horror
    # Telechargement de la page url horror
    page = requests.get(url_category)
    # création de l'objet Soup
    soup = bs(page.text, "lxml")
    #print(url_category)
    return soup

def get_all_links_book_to_category(soup):
    # Récupération de tous les liens des livres dans la catégorie horror
    links_categorys = []
    listings = soup.find_all(class_="product_pod")
    # A partir de chaques liens récupérer on peut obtenir le lien de livres
    for listing in listings:
        target_link_catg = listing.find("h3").a.get("href")
        base_url = "https://books.toscrape.com/catalogue/category/books"
        complete_lnk = base_url + target_link_catg
        links_categorys.append(complete_lnk)
    return links_categorys


def info_extract(links_categorys,csv_created):
    #print(csv_created)
    already_init = 0
    # Extraire les informations de chaques livres dans horror
    for links_cats in links_categorys:
        response = requests.get(links_cats)
        response.encoding = 'UTF-8'
        response_info_catgs = response.text
        book_soup = bs(response_info_catgs, "lxml")
        product_page_url = links_cats
        table = book_soup.findAll('td')
        title = book_soup.find('h1').text
        universal_product_code = table[0].text
        price_including_tax = table[2].text #.replace('£', '£').replace('Â', '')
        price_excluding_tax = table[3].text #.replace('£', '£').replace('Â', '')
        number_available = table[5].text.removeprefix('In stock (').removesuffix('available)')
        product_description_unicode = book_soup.select_one('article > p').text
        product_description = unidecode.unidecode(product_description_unicode)
        category = book_soup.find('ul', class_="breadcrumb").findAll('a')[2].text
        category = category.replace(" ", "")
        review_rating = book_soup.find('p', class_='star-rating').get('class').pop()
        image = book_soup.find('div', class_="item active").find('img')

        book_of_catg = {"product_page_url": product_page_url,
                        "title": title,
                        "product_description": product_description,
                        "universal_product_code": universal_product_code,
                        "price_including_tax": price_including_tax,
                        "price_excluding_tax": price_excluding_tax,
                        "category": category,
                        "review_rating": review_rating,
                        "image": image['src'],
                        "number_available": number_available}

        #all_books_categorys.append(book_of_catg)
        en_tete_catg = ['product_page_url',
                        'title',
                        'product_description',
                        'universal_product_code',
                        'price_including_tax',
                        'price_excluding_tax',
                        'category',
                        'review_rating',
                        'image',
                        'number_available']

        # Créer un nouveau fichier pour écrire dans le fichier appelé « data.csv
        if (already_init == 0 and not csv_created):
            with open('category/' + category + '/data_' + category + '.csv', 'w') as fichier_csv:

                writer = csv.writer(fichier_csv, delimiter=';')
                writer.writerow(en_tete_catg)
                writer.writerow([product_page_url,
                                        title,
                                        product_description,
                                        universal_product_code,
                                        price_including_tax,
                                        price_excluding_tax,
                                        category,
                                        review_rating,
                                        get_link_image(image, 3),
                                        number_available])
            already_init = 1
        else:
            with open('category/' + category + '/data_' + category + '.csv', 'a') as fichier_csv:

                writer_object = csv.writer(fichier_csv, delimiter=';')
                writer_object.writerow([product_page_url,
                                        title,
                                        product_description,
                                        universal_product_code,
                                        price_including_tax,
                                        price_excluding_tax,
                                        category,
                                        review_rating,
                                        get_link_image(image, 3),
                                        number_available])


        image_url = get_link_image(image, 3)
        filename = 'category/' + category + '/' + title.replace(":", "").replace("/", " ").replace('"', '').replace(
            'Ã©', 'é').replace(",", "").replace(".", "").replace("&", "").replace("*", "").replace("?", "") + ".jpg"
        urllib.request.urlretrieve(image_url, filename)


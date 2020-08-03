import requests
from bs4 import BeautifulSoup

def get_product_price(link):
    try:
        page = requests.get(link).text
    except requests.exceptions.MissingSchema:
        return "Invalid URL"
    except requests.exceptions.ConnectionError:
        return "No Connection"
    else:
        soup = BeautifulSoup(page, 'lxml')
        product = soup.find(class_="_35KyD6").text
        price = soup.find(class_="_1vC4OE _3qQ9m1").text
        return [product, price]

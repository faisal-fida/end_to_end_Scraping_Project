import pandas as pd 
import firebase_admin
import requests_html as r 
from firebase_admin import firestore
from firebase_admin import credentials

URL = 'https://books.toscrape.com/catalogue/page-50.html'
session = r.HTMLSession()
response = session.get(url=URL).html

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_data(data):
    titles = [i.text for i in response.find('article.product_pod h3')]
    instock = [i.text for i in response.find('p.instock.availability')]
    prices = [i.text.replace('£','') for i in response.find('p.price_color')]
    links = [i.attrs['href'] for i in response.find('article.product_pod h3 a')]
    objectId = list(range(1,len(titles)))
    keys = ['objectId','titles','instock','prices','links']
    data = [dict(zip(keys,l)) for l in zip(objectId,titles,instock,prices,links)]
    return data

def upload_data(data):
    for i in data:
        db.collection('books').document(f'bookid_{i["objectId"]}').set(i)

def download_data():
    #database retrieve
    print('')


def main():
    data = []
    data = get_data(data)
    upload_data(data)

main()

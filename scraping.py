from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup

from pymongo import MongoClient

from webdriver_manager.chrome import ChromeDriverManager

from enum import Enum

#from selenium.webdriver.common.by import By



class web_sites(Enum):
    kitapyurdu = {'collection': 'kitapyurdu', 'url': 'https://www.kitapyurdu.com/index.php?route=product/search&filter_name=python&fuzzy=0&filter_in_shelf=1&filter_in_stock=0',
                  'main_class': 'product-cr', 'title': 'name', 'publisher': 'publisher', 'author': 'author',
                  'price': 'price'}
    kitapsepeti = {'collection': 'kitapsepeti', 'url': 'https://www.kitapsepeti.com/arama?q=python&stock=1',
                   'main_class': 'productDetails', 'price': 'discountedPrice'}


class Scraping:

    def __init__(self, web_site):
        self.website = web_sites[web_site].value #Scraping class'ı örneklendirilirken website değişkeni atanır.

    def get_data(self):
        client = MongoClient("mongodb://aslihan:123456@localhost:27017/smartmaple")#mongoya bağlanılır.
        db = client['smartmaple']
        coll = db[self.website['collection']]
        books = self.get_python_books()#get_python_books metodu çağırılır.
        coll.insert_many(books)#get_python_books metodundan dönen veriler mongoya yazılır.
        # cursor = coll.find({})
        # for document in cursor:
        #     print('>>', document, '\n')
        client.close()#bağlantı kapatılır

    def get_python_books(self):
        import re
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(self.website['url'])
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, features="html.parser")
        books = []
        matches = soup.body.find_all("div", {"class": self.website['main_class']})#siteden html bilgilerine göre kazıma yapılır
        if self.website['collection'] == "kitapyurdu":
            for result in matches: #veriler bir listeye eklenir.
                price = result.find("div", {"class": self.website['price']}).get_text().strip().replace(',', '.')
                price = re.findall("\d+\.\d+", price)[0]
                writer = result.find("div", {"class": self.website['publisher']}).get_text().strip().split("Yazar:")[0]
                book = {'title': result.find("div", {"class": self.website['title']}).get_text().strip(),
                        'publisher': writer,
                        'author': result.find("div", {"class": self.website['author']}).get_text().strip(),
                        'price': price}
                books.append(book)
            return books
        else:
            for result in matches: #veriler bir listeye eklenir.
                data = result.find_all('a')
                price = result.find("div", {"class": self.website['price']}).get_text().strip().split('\n')[0]
                book = {'title': data[0].get_text().strip(),
                        'publisher': data[1].get_text().strip(),
                        'author': data[2].get_text().strip(),
                        'price': price}
                books.append(book)
            return books


from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from pymongo import MongoClient

from webdriver_manager.chrome import ChromeDriverManager

from enum import Enum


class web_sites(Enum):
    kitapyurdu = {'db': 'kitapyurdu', 'url': 'https://www.kitapyurdu.com/kategori/kitap-cocuk-kitaplari/2.html',
                  'main_class': 'product-cr', 'title': 'name', 'publisher': 'publisher', 'author': 'author',
                  'price': 'price'}
    kitapsepeti = {}


class Scraping:

    def __init__(self, web_site):
        self.website = web_sites[web_site].value #Scraping class'ı örneklendirilirken website değişkeni atanır.

    def get_data(self):
        client = MongoClient("mongodb://aslihan:123456@localhost:27017/smartmaple")#mongoya bağlanılır.
        db = client['smartmaple']
        coll = db[self.website['db']]
        child_books = self.get_child_books()#get_child_books metodu çağırılır.
        coll.insert_many(child_books)#get_child_books metodundan dönen veriler mongoya yazılır.
        # cursor = coll.find({})
        # for document in cursor:
        #     print('>>', document, '\n')
        client.close()#bağlantı kapatılır

    def get_child_books(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(self.website['url'])
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, features="html.parser")
        child_books = []
        matches = soup.body.find_all("div", {"class": self.website['main_class']})#siteden html bilgilerine göre kazıma yapılır
        for result in matches: #veriler bir listeye eklenir.
            book = {'title': result.find("div", {"class": self.website['title']}).get_text().strip(),
                    'publisher': result.find("div", {"class": self.website['publisher']}).get_text().strip(),
                    'author': result.find("div", {"class": self.website['author']}).get_text().strip(),
                    'price': result.find("div", {"class": self.website['price']}).get_text().strip()}
            child_books.append(book)
        return child_books

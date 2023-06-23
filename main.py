
from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from pymongo import MongoClient

from webdriver_manager.chrome import ChromeDriverManager

from enum import Enum

class web_sites(Enum):
    kitapyurdu = {'db': 'kitapyurdu', 'url': 'https://www.kitapyurdu.com/kategori/kitap-cocuk-kitaplari/2.html', 'main_class': 'product-cr', 'title': 'name', 'publisher': 'publisher', 'author': 'author', 'price': 'price'}
    kitapsepeti = {}

def get_database():
    website = web_sites.kitapyurdu
    client = MongoClient("mongodb://aslihan:123456@localhost:27017/smartmaple")
    db = client['smartmaple']
    coll = db['smartmaple']
    child_books = get_child_books(website.value)
    coll.insert_many(child_books)
    cursor = coll.find({})
    for document in cursor:
        print('>>', document, '\n')
    client.close()


def get_child_books(website):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)
    driver.get(website['url'])
    wait.until(EC.url_to_be(website['url']))
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, features="html.parser")
    child_books = []
    matches = soup.body.find_all("div", {"class": website['main_class']})
    for result in matches:
        book = {}
        book['title'] = result.find("div", {"class": website['title']}).get_text().strip()
        book['publisher'] = result.find("div", {"class": website['publisher']}).get_text().strip()
        book['author'] = result.find("div", {"class": website['author']}).get_text().strip()
        book['price'] = result.find("div", {"class": website['price']}).get_text().strip()
        child_books.append(book)
    return child_books


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_database()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

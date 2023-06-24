import scraping
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrap = scraping.Scraping("kitapyurdu") #Scraping class örneklendirilir.
    scrap.get_data()#Scraping class'ın get_data metodu çağırılır.
mongosh komutu ile mongo shelle geçilip use komutu ile veritabanı kurulur. createCollection komutu ile collection oluşturulur. main.py çalıştırılarak proje başlatılır.
Scraping sınıfı main.py'de website adı ile örneklendirilip get_data metodu çağırılır.
get_data metodunda öncelikle mongo veritabanına bağlanılır.
Daha sonra get_python_books metodu çağırılıp selenium ile html parse edilerek içinden kitap özellikleri html tag ve class isimlerine göre çekilir.
Verilerin içerisindeki fazla bilgiler ("Yazar: kelimesi gibi") silinerek şekillendirilir.
Veriler bir listede toplanarak return edilir.
Yeniden get_data metoduna gelen veriler mongo vertabanına kaydedilir.
Bağlantı kapatılarak işlem sonuçlandırılır.

Ubuntu işletim sisteminde cron sistemi kullanılarak hergün bu kodun çalışması sağlanabilir.
Terminale “crontab -e” yazılıp cron dosyası açılır.
Dosyaya “0 0 * * * /usr/bin/python ~/Desktop/data-scraping/main.py >> ~/Desktop/data-scraping/scrap_log.log 2>&1” komutu eklenip kaydedilir. Böylece kod hergün gece yarısı çalışır.

from web_scrapper import  scrape_immowelt, setup_logging, sanitize_filename 

''' 
loop ile immowelt_urls_copy (used in web scraping).csv masaüstü bu dosyadan cekecegim 
url leri teker tker basacak scrapping yapcak ve bunlari kayit edecek. ben de buna bir istatistik uygulayacagim 
ve sehir konumundan bir agirlik vereegim (ayni özelliktei evleri fiyet olaarak karsilatirarak.).
sonra bu agirlik her bir sehir icin eslesecek ve ayrica bu geospatial konumu da alip esleyecegim.
sonrasinda bunlari ilanlar icin olusturdugum db ye aktaracagim.
ve tekrardan bu db nin constraintslerini geri yükleyecegim.

'''
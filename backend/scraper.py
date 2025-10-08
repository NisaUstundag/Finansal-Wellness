import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Hedef URL'imi belirliyorum. Veri toplamak için burayı değiştireceğim.
URL = "https://eksisozluk.com/pasif-gelir--1087961"

print(f"Hedef sayfa açılıyor: {URL}")

try:
    # Selenium'u arkaplanda çalışacak şekilde ayarlıyorum.
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Sayfaya gidip içeriğin yüklenmesini bekliyorum.
    driver.get(URL)
    print("Sayfa yüklendi, 5 saniye bekleniyor...")
    time.sleep(5) 

    # Yüklenmiş sayfanın HTML'ini alıp tarayıcıyı kapatıyorum.
    html_content = driver.page_source
    driver.quit()

    # BeautifulSoup ile HTML'i işliyorum.
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Hedefimdeki entry'leri 'content' class'ı ile buluyorum.
    entry_blocks = soup.find_all("div", class_="content")
    
    if entry_blocks:
        print(f"{len(entry_blocks)} adet entry bulundu. 'raw_data.txt' dosyasına kaydediliyor...")
        
        # 'raw_data.txt' dosyasını 'ekleme' modunda ('a') açıyorum.
        with open("raw_data.txt", "a", encoding="utf-8") as f:
            # Her bir entry'nin metnini alıyorum.
            for entry in entry_blocks:
                entry_text = entry.get_text(strip=True)
                # Sadece 50 karakterden uzun olan, anlamlı entry'leri dosyaya yazdırıyorum.
                if len(entry_text) > 50:
                    f.write(entry_text + '\n') # Her cümleyi yeni bir satıra yaz.
        
        print("Veriler başarıyla kaydedildi.")

    else:
        print("Hiç entry bulunamadı.")

except Exception as e:
    print(f"Bir hata oluştu: {e}")
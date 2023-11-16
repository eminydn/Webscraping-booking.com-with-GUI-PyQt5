from login import email, password
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver import Keys

from bs4 import BeautifulSoup
import pandas as pd

import unicodedata
import time
import warnings
warnings.filterwarnings("ignore")



class Hotel:
    def __init__(self, email, password):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("disable-popup-blocking")
        self.options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(options=self.options)

        self.username = email
        self.password = password

        self.hotel_names = []
        self.prices = []
        self.extra_prices = []
        self.ratio = []
        self.ratio_count = []



    def sign_in_facebook(self):
        #booking.com'a gir
        self.browser.get('https://www.booking.com')
        time.sleep(15)

        #sayfa yüklendikten sonra tam ekran yap
        self.browser.maximize_window()
        
        #açılır pop-up kapat
        self.browser.find_element(By.CSS_SELECTOR, "button.a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.deab83296e.f4552b6561").click()
        time.sleep(1)

        #giris yap butonuna bas
        #self.browser.find_element(By.XPATH, "/html/body/div[4]/div/header/nav[1]/div[2]/div/a/span").click()
        self.browser.find_element(By.XPATH, "/html/body/div[3]/div/header/nav[1]/div[2]/div/a").click()
        #self.browser.find_element(By.CSS_SELECTOR, "span[aria-label='28 Ekim 2023']").click()
        time.sleep(3)
        
        #facebook seceneği ile giriş yap
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/form/div[4]/div[2]/a[1]").click()
        time.sleep(3)

        #açılan facebook giriş ekranına geçiş yap
        self.browser.switch_to.window(self.browser.window_handles[1])

        #kullanıcı adı ve şifre gir
        self.browser.find_element(By.ID, 'email').send_keys(self.username)
        time.sleep(1)
        self.browser.find_element(By.ID, 'pass').send_keys(self.password)
        time.sleep(1)

        #giriş butonuna bas - bekle - ana ekrana geri dön
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/button").click()
        time.sleep(15)
        
        self.browser.switch_to.window(self.browser.window_handles[0])
    
    def search(self, search_key: str, search_type: str = "default"):
        #arama metnini ver
        #1- self.browser.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/form/div[1]/div[1]/div/div/div[1]/div/div/input").clear()
        #2- self.browser.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/form/div[1]/div[1]/div/div/div[1]/div/div/input").send_keys((Keys.CONTROL , "A"))
        self.browser.find_element(By.CSS_SELECTOR, ".eb46370fe1").send_keys((Keys.CONTROL , "A"))
        time.sleep(3)
        self.browser.find_element(By.CSS_SELECTOR, ".eb46370fe1").send_keys(Keys.DELETE)
        #self.browser.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/form/div[1]/div[1]/div/div/div[1]/div/div/input").send_keys(Keys.DELETE)
        time.sleep(5)
        self.browser.find_element(By.CSS_SELECTOR, ".eb46370fe1").send_keys(search_key)
        #1- self.browser.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/form/div[1]/div[1]/div/div/div[1]/div/div/input").send_keys(search_key)
        #2- self.browser.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/form/div[1]/div[1]/div/div/div[1]/div/div/input").send_keys((Keys.CONTROL , "A"), "Alaska")
        time.sleep(3)

        #boş alana tıkla
        self.browser.find_element(By.XPATH, "//body").click()

        #tarih bas
        #self.browser.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/form/div[1]/div[2]/div/div").click()
        self.browser.find_element(By.CSS_SELECTOR, ".f73e6603bf").click()
        time.sleep(3)

        #tarih sec
        self.browser.find_element(By.CSS_SELECTOR, "span[aria-label='28 Ekim 2023']").click()
        time.sleep(3)
        
        #arama butonuna tıkla
        #self.browser.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/form/div[1]/div[4]/button").click()
        self.browser.find_element(By.CSS_SELECTOR, "button.a83ed08757.c21c56c305.a4c1805887.f671049264.d2529514af.c082d89982.cceeb8986b").click()

        #get_source ve parse_source fonksiyonlarını ilk sayfa için çalıştır
        src = self.get_source()
        self.parse_source(src)

        if search_type == "default":
            default_value = 3
            counter = 0
            while counter < default_value:
                next_button = self.browser.find_element(By.XPATH, "/html/body/div[7]/div/div[6]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div[4]/div[2]/nav/div/div[3]/button")
                if  next_button.is_enabled() == True:
                    next_button.click()
                    time.sleep(6)
                    try:
                        src = self.get_source()
                        self.parse_source(src)
                    except NoSuchElementException:
                        print("OLMADI---------")
                else:
                    break
                counter += 1


        elif search_type == "total":
            while True:
                next_button = self.browser.find_element(By.XPATH, "/html/body/div[7]/div/div[6]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div[4]/div[2]/nav/div/div[3]/button")
                if  next_button.is_enabled() == True:
                    next_button.click()
                    time.sleep(6)
                    try:
                        src = self.get_source()
                        self.parse_source(src)
                    except NoSuchElementException:
                        print("OLMADI---------")
                else:
                    break



    def get_source(self):
        #beautifulsoup ile kaynak kodunu işleme
        result = self.browser.page_source
        soup = BeautifulSoup(result, 'html.parser')
        page =  list(soup.findAll('div', {"class": "c82435a4b8 a178069f51 a6ae3c2b40 a18aeea94d d794b7a0f7 f53e278e95 c6710787a4"}))
        return page

    def parse_source(self, page):
        for i in range(0, len(page)):
            try:
                self.hotel_names.append(page[i].find("div", {"class": "f6431b446c a15b38c233"}).text)
            except:
                self.hotel_names.append("None")

            try:
                self.prices.append(unicodedata.normalize("NFKD", page[i].find("span", {"class": "f6431b446c fbfd7c1165 e84eb96b1f"}).text))
            except:
                self.prices.append("None")

            try:
                self.extra_prices.append(unicodedata.normalize("NFKD", page[i].find("div", {"data-testid": "taxes-and-charges"}).text))
            except:
                self.extra_prices.append("None")

            try:
                self.ratio.append(unicodedata.normalize("NFKD", page[i].find("div", {"class": "a3b8729ab1 d86cee9b25"}).text))
            except:
                self.ratio.append("None")

            try:
                self.ratio_count.append(unicodedata.normalize("NFKD", page[i].find("div", {"class": "abf093bdfe f45d8e4c32 d935416c47"}).text))
            except:
                self.ratio_count.append("None")

            
            #self.hotel_names.append(page[i].find("div", {"class": "f6431b446c a15b38c233"}).text)         
            #self.prices.append(unicodedata.normalize("NFKD", page[i].find("span", {"class": "f6431b446c fbfd7c1165 e84eb96b1f"}).text))
            #self.extra_prices.append(unicodedata.normalize("NFKD", page[i].find("div", {"data-testid": "taxes-and-charges"}).text))
            #self.ratio.append(unicodedata.normalize("NFKD", page[i].find("div", {"class": "a3b8729ab1 d86cee9b25"}).text))
            #self.ratio_count.append(unicodedata.normalize("NFKD", page[i].find("div", {"class": "abf093bdfe f45d8e4c32 d935416c47"}).text))

    def export_to_excel(self):
        df = pd.DataFrame({"Otel ismi":self.hotel_names, "Ücret":self.prices, "Ek Ücretler":self.extra_prices, "Puan":self.ratio, "Değerlendirme Sayısı": self.ratio_count})
        df.to_excel('otel_deneme_roma4.xlsx')
        print("BİTTİ")
otel = Hotel(email, password)
otel.sign_in_facebook()
otel.export_to_excel()

# print(otel.hotel_names)
# print(otel.extra_prices)

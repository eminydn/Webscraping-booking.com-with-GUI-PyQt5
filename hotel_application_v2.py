from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import pandas as pd

import unicodedata
import time
import dateutil
import warnings
warnings.filterwarnings("ignore")



class Hotel:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("disable-popup-blocking")
        self.options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(options=self.options, service=ChromeService(ChromeDriverManager().install()))

        self.delay = 3

        self.hotel_names = []
        self.prices = []
        self.extra_prices = []
        self.ratio = []
        self.ratio_count = []



    #methods
    def sign_in_facebook(self, email, password):
        username = email
        password = password

        #visit booking.com
        self.browser.get('https://www.booking.com')
        delay = self.delay
        try:
            checkElem = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Giriş bilgisini kapat.']")))
            print ("Pop up closed")
        except TimeoutException:
            print ("Page error")

        #maximize window after loading page
        self.browser.maximize_window()
        
        #close pop up
        try:
            self.browser.find_element(By.CSS_SELECTOR, "button[aria-label='Giriş bilgisini kapat.']").click()
            time.sleep(1)
        except:
            print("pop up not shown")

        #push login button
        try:
            checkElem = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[aria-label='Giriş yap']")))
            self.browser.find_element(By.CSS_SELECTOR, "a[aria-label='Giriş yap']").click()
            print ("Login page loaded")
        except TimeoutException:
            print ("Login page error")

        #login with facebook
        try:
            checkElem = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-provider-name='facebook']")))
            checkElem.click()
            # self.browser.find_element(By.CSS_SELECTOR, "a[data-provider-name='facebook']").click()
            print ("Loaded facebook login page")
        except TimeoutException:
            print ("Login facebook error")
        
        #switch to facebook login window
        self.browser.switch_to.window(self.browser.window_handles[1])

        #input username-password
        try:
            self.browser.find_element(By.ID, 'email').send_keys(username)
            self.browser.find_element(By.ID, 'pass').send_keys(password)
        except:
            print("Username and pass error")

        #push login facebook
        try:
            self.browser.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/button").click()
            print ("Login successfully")
        except TimeoutException:
            print ("Login error")
        
        #switch to main window
        self.browser.switch_to.window(self.browser.window_handles[0])

        #wait to load page
        time.sleep(10)
        WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='occupancy-config']")))
    


    def set_room_type(self, adult, child, room):
        delay = self.delay
        try:
            checkElem = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='occupancy-config']")))
            checkElem.click()
            
            plus_buttons = self.browser.find_elements(By.CSS_SELECTOR, "button[class='a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 deab83296e bb803d8689 f4d78af12a']")

            if adult < 2:
                self.browser.find_element(By.CSS_SELECTOR, "button[class='a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 deab83296e bb803d8689 e91c91fa93']").click()
            elif adult > 2:
                for i in range(0, adult - 2):
                    plus_buttons[0].click()

            for i in range(0, 0):
                plus_buttons[1].click()

            for i in range(0, room - 1):
                plus_buttons[2].click()

        except:
            print("Room properties cant be changed")
        


    def search(self, search_key: str, search_date: str, search_type: str = "default"):
        self.browser.find_element(By.XPATH, "//body").click()
        #take city name as a search input
        self.browser.find_element(By.CSS_SELECTOR, ".eb46370fe1").send_keys((Keys.CONTROL , "A"))
        time.sleep(3)
        self.browser.find_element(By.CSS_SELECTOR, ".eb46370fe1").send_keys(Keys.DELETE)
        time.sleep(3)
        self.browser.find_element(By.CSS_SELECTOR, ".eb46370fe1").send_keys(search_key)
        time.sleep(3)

        #click empty area
        self.browser.find_element(By.XPATH, "//body").click()

        #click date area
        self.browser.find_element(By.CSS_SELECTOR, ".f73e6603bf").click()
        time.sleep(2)

        #choose date
        self.browser.find_element(By.CSS_SELECTOR, f"span[aria-label='{search_date}']").click()
        time.sleep(2)
        
        #click search button
        self.browser.find_element(By.CSS_SELECTOR, "button.a83ed08757.c21c56c305.a4c1805887.f671049264.d2529514af.c082d89982.cceeb8986b").click()

        time.sleep(3)
        #get_source and parse_source function loop by choises
        src = self.get_source()
        self.parse_source(src)

        if search_type == "default":
            #default value that how many times pass next page
            default_value = 5
            counter = 0
            while counter < default_value:
                next_button = self.browser.find_element(By.CSS_SELECTOR, "button[aria-label='Sonraki sayfa']")
                if  next_button.is_enabled() == True:
                    next_button.click()
                    time.sleep(6)
                    try:
                        src = self.get_source()
                        self.parse_source(src)
                    except NoSuchElementException:
                        print("PROBLEM---------")
                else:
                    break
                counter += 1


        elif search_type == "total":
            while True:
                next_button = self.browser.find_element(By.CSS_SELECTOR, "button[aria-label='Sonraki sayfa']")
                if  next_button.is_enabled() == True:
                    next_button.click()
                    time.sleep(6)
                    try:
                        src = self.get_source()
                        self.parse_source(src)
                    except NoSuchElementException:
                        print("PROBLEM---------")
                else:
                    break



    def get_source(self):
        #handle sourch code data with beautifulsoup 
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



    def change_currency(self):
        try:
            currency_list_btn = self.browser.find_element(By.CSS_SELECTOR, "button[data-testid='header-currency-picker-trigger']")
            currency_list_btn.click()
        except NoSuchElementException as e:
            print("Change currency button can't find")
        
        try:
            currency_btn = self.browser.find_elements(By.CSS_SELECTOR, "div[class=' ea1163d21f']")
            for i in currency_btn:
                if i.text == "EUR":
                    i.click()
                    break
        except:
            print("Euro cant selected")
        
        time.sleep(5)
        WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='occupancy-config']")))



    def export_to_excel(self, path, city, room_selection: list, check_in_out: list):
        df = pd.DataFrame({"Otel ismi":self.hotel_names, "Ücret":self.prices, "Ek Ücretler":self.extra_prices, "Puan":self.ratio, "Değerlendirme Sayısı": self.ratio_count,
                           "Yetişkin": [room_selection[0]]*len(self.prices), "Çocuk": [room_selection[1]]*len(self.prices), "Oda": [room_selection[2]]*len(self.prices),
                           "Giriş Tarihi": [check_in_out[0]]*len(self.prices), "Çıkış Tarihi": [check_in_out[1]]*len(self.prices)})
        df.to_excel(f'{path}/otel_veri_{city}.xlsx')
        print("Excel file created")
            
            #self.hotel_names.append(page[i].find("div", {"class": "f6431b446c a15b38c233"}).text)         
            #self.prices.append(unicodedata.normalize("NFKD", page[i].find("span", {"class": "f6431b446c fbfd7c1165 e84eb96b1f"}).text))
            #self.extra_prices.append(unicodedata.normalize("NFKD", page[i].find("div", {"data-testid": "taxes-and-charges"}).text))
            #self.ratio.append(unicodedata.normalize("NFKD", page[i].find("div", {"class": "a3b8729ab1 d86cee9b25"}).text))
            #self.ratio_count.append(unicodedata.normalize("NFKD", page[i].find("div", {"class": "abf093bdfe f45d8e4c32 d935416c47"}).text))


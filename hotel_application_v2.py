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

        self.hotel_names = []
        self.prices = []
        self.extra_prices = []
        self.ratio = []
        self.ratio_count = []



    def sign_in_facebook(self, email, password):
        username = email
        password = password

        #visit booking.com
        self.browser.get('https://www.booking.com')
        delay = 1
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
            self.browser.find_element(By.CSS_SELECTOR, "a[data-provider-name='facebook']").click()
            print ("Loaded facebook login page")
        except TimeoutException:
            print ("Login facebook error")
        

        #switch to facebook login window
        self.browser.switch_to.window(self.browser.window_handles[1])

        #input username-password
        self.browser.find_element(By.ID, 'email').send_keys(username)
        self.browser.find_element(By.ID, 'pass').send_keys(password)

        #push login facebook
        try:
            self.browser.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/button").click()
            print ("Login successfully")
        except TimeoutException:
            print ("Login error")
        
        #switch to main window
        self.browser.switch_to.window(self.browser.window_handles[0])
    

    def search(self, search_key: str, search_date: str, search_type: str = "default"):
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
        time.sleep(3)

        #choose date
        self.browser.find_element(By.CSS_SELECTOR, f"span[aria-label='{search_date}']").click()
        time.sleep(3)
        
        #click search button
        self.browser.find_element(By.CSS_SELECTOR, "button.a83ed08757.c21c56c305.a4c1805887.f671049264.d2529514af.c082d89982.cceeb8986b").click()

        time.sleep(3)
        #get_source and parse_source function loop by choise
        src = self.get_source()
        self.parse_source(src)

        if search_type == "default":
            default_value = 3
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

            
            #self.hotel_names.append(page[i].find("div", {"class": "f6431b446c a15b38c233"}).text)         
            #self.prices.append(unicodedata.normalize("NFKD", page[i].find("span", {"class": "f6431b446c fbfd7c1165 e84eb96b1f"}).text))
            #self.extra_prices.append(unicodedata.normalize("NFKD", page[i].find("div", {"data-testid": "taxes-and-charges"}).text))
            #self.ratio.append(unicodedata.normalize("NFKD", page[i].find("div", {"class": "a3b8729ab1 d86cee9b25"}).text))
            #self.ratio_count.append(unicodedata.normalize("NFKD", page[i].find("div", {"class": "abf093bdfe f45d8e4c32 d935416c47"}).text))


# otel = Hotel(email, password)
# otel.sign_in_facebook()
# otel.export_to_excel()

# print(otel.hotel_names)
# print(otel.extra_prices)

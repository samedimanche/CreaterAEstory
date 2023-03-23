import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import time
from bs4 import BeautifulSoup
import datetime
import lxml
import html5lib
driver = webdriver.Chrome()

headers = {"User-Agent" : 'Mozilla/5.0'}
URL = "https://tinkoff.travelata.ru/search#?fromCity=37&toCountry=87&dateFrom=23.03.2023&dateTo=" \
      "23.03.2023&nightFrom=8&nightTo=15&adults=2&hotelClass=all&meal=all&priceFrom=6000&priceTo=200000&sid=1px7n2x8d5&sort=priceUp&f_noScore=true"

# driver.minimize_window()
driver.get(URL)
time.sleep(5)
# content = driver.page_source
# soup = BeautifulSoup(content, "html.parser")
# print(soup)
lister=[]
link = list(driver.find_elements(by=By.CLASS_NAME, value="serpHotelCard__btn"))
print(link)

for links in range(0,int(len(link))):
    link[links].click()
    window_after = driver.window_handles[1+links]
    driver.switch_to.window(window_after)
    lister.append(driver.current_url)
    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)
    time.sleep(3)


print(lister)
driver.quit()
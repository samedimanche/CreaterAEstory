import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import datetime
from selenium.common.exceptions import NoSuchElementException, ElementNotSelectableException
driver = webdriver.Chrome()

cityRus={"Krasnoyarsk":37, "Moscow":2, "Khabarovsk":80, "Vladivostok":19, "Blagoveshensk":15, "Irkutsk":28}
cityOutside={"Thailand":87, "Turkish":92, "Egypt":29, "UAE":68, "Venezuela":21, "Cuba":48, "Vietnam":22}


headers = {"User-Agent" : 'Mozilla/5.0'}

lister=[]
url_list=[]
def url_parser():
    for i in range(len(cityRus)):
        for j in range(len(cityOutside)):
            URL = f"https://tinkoff.travelata.ru/search#?fromCity={list(cityRus.values())[i]}&toCountry={list(cityOutside.values())[j]}" \
                  f"&dateFrom={format(datetime.date.today() + datetime.timedelta(weeks=2) - datetime.timedelta(days=2), '%d.%m.%Y')}" \
                  f"&dateTo={format(datetime.date.today() + datetime.timedelta(weeks=2) - datetime.timedelta(days=2), '%d.%m.%Y')}&nightFrom=8&nightTo=15" \
                  f"&adults=2&hotelClass=all&meal=all&priceFrom=6000&priceTo=180000&sid=1px7n2x8d5&sort=priceUp&f_noScore=true"
            url_list.append(URL)

def link_parser(i):
    URL = i
    driver.maximize_window()
    driver.get(URL)
    time.sleep(25)
    link = list(driver.find_elements(by=By.CLASS_NAME, value="serpHotelCard__btn"))
    print(link)
    for links in range(0, int(len(link))):
        link[links].click()
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        lister.append(driver.current_url)
        with open("test.txt", "a") as f:
            f.write(driver.current_url + "\n")
        driver.close()
        window_after = driver.window_handles[0]
        driver.switch_to.window(window_after)
        time.sleep(1)
    print(lister)


    # find_not = driver.find_elements(by=By.CLASS_NAME, value="no-tours-banner__title")
    # print(find_not)
    # if find_not!=[]:
    #     return 0
    # else:
    #     link = list(driver.find_elements(by=By.CLASS_NAME, value="serpHotelCard__btn"))
    #     print(link)
    #     for links in range(0, int(len(link))):
    #         link[links].click()
    #         window_after = driver.window_handles[1]
    #         driver.switch_to.window(window_after)
    #         lister.append(driver.current_url)
    #         driver.close()
    #         window_after = driver.window_handles[0]
    #         driver.switch_to.window(window_after)
    #         time.sleep(1)
    #     print(lister)




def main():
    url_parser()
    print(url_list)
    for i in url_list:
        link_parser(i)
    print(lister)
    driver.quit()


if __name__ == '__main__':
    main()

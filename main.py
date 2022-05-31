import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/97.0.4692.99 Safari/537.36/8mqQhSuL-09 ",
    "Accept-Language": "en-US"

}
url = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
      "%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122" \
      ".30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22" \
      "%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D" \
      "%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22" \
      "%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B" \
      "%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price" \
      "%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom" \
      "%22%3A12%7D "

response = requests.get(url=url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

s = Service("D:\Development\chromedriver_win32\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('window-size=1440,1440')
driver = webdriver.Chrome(service=s, options=options)
driver.get(url)
time.sleep(4)

for _ in range(20):
    webdriver.ActionChains(driver).key_down(Keys.TAB).perform()
for _ in range(120):
    webdriver.ActionChains(driver).key_down(Keys.ARROW_DOWN).perform()

html_data = driver.page_source
soup = BeautifulSoup(html_data, "html.parser")

check = soup.select("div #grid-search-results ul li a")
check2 = soup.select("div #grid-search-results ul li div .list-card-price")
check3 = soup.select("div #grid-search-results ul li div .list-card-addr")
hotel_link_list = []
prices = []
address = []
for i in range(0, len(check), 1):
    if i < len(check) - 1 and (check[i].get('href') != check[i + 1].get('href')):
        if check[i].get('href').startswith("/b"):
            hotel_link_list.append('https://www.zillow.com' + check[i].get('href'))
        elif check[i].get('href').startswith("https"):
            hotel_link_list.append(check[i].get('href'))

for i in range(0, len(check2)):
    prices.append(check2[i].text.strip('+1 bd/mo'))

for i in range(0, len(check3)):
    address.append(check3[i].text.split(' | ')[0])

print(hotel_link_list)
print(prices)
print(address)
print(len(address))

# s = Service("D:\Development\chromedriver_win32\chromedriver.exe")
# driver = webdriver.Chrome(service=s)


for i in range(len(hotel_link_list)):
    driver.get(
        "https://docs.google.com/forms/d/e/1FAIpQLSdP6i_5R3Ke5HBt-vsaYUe169YgqHoFa0SrMLG3xFhamYAnOQ/viewform?usp"
        "=sf_link")
    address_ans = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]')
    ActionChains(driver).move_to_element(address_ans).click(address_ans).send_keys(address[i]).perform()

    price_ans = driver.find_element(By.XPATH,
                                    '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div['
                                    '1]/div/div[1]/input')
    ActionChains(driver).move_to_element(price_ans).click(price_ans).send_keys(prices[i]).perform()

    link_ans = driver.find_element(By.XPATH,
                                   '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                   '1]/div/div[1]/input')
    ActionChains(driver).move_to_element(link_ans).click(link_ans).send_keys(hotel_link_list[i]).perform()

    submit_button = driver.find_element(By.XPATH,
                                        '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    ActionChains(driver).move_to_element(submit_button).click(submit_button).perform()

    time.sleep(2)

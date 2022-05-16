from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os
from urllib import parse
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.pap.pl/")

ok_button = driver.find_element(by="xpath", value='//*[@id="cookie"]/div/div/div/div/div/div[1]')
ok_button.click()

driver.maximize_window()
sleep(2)

english_change = driver.find_element(by="xpath", value='//*[@id="navbar"]/ul[2]/li[3]/a')
english_change.click()

business_change = driver.find_element(by="xpath", value='//*[@id="block-mainnavigationen"]/ul/li[3]/a')
business_change.click()

titles_ul = driver.find_element(by="xpath", value='/html/body/div[1]/div[2]/section[2]/div/div[2]/div[1]/div[2]/div/div/div/div[2]/div/ul')
options = titles_ul.find_elements(by="tag name", value='li')
imgs = titles_ul.find_elements(by="tag name", value='img')
titles = [option.text for option in options]
print(titles)

counter = 0
for img in imgs:
    path = os.path.join('/Users/kinatra/Desktop/PAD/PracaDomowa6/images/', f'{counter}.png')
    img.screenshot(path)
    sleep(0.2)
    counter = counter + 1

driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

last_page_button = driver.find_element(by='xpath', value='/html/body/div[1]/div[2]/section[2]/div/div[2]/div[1]/div[2]/div/nav/ul/li[5]/a')
last_page_button.click()

url = driver.current_url

o = dict(parse.parse_qsl(parse.urlsplit(url).query))
print(o['page'])
driver.quit()
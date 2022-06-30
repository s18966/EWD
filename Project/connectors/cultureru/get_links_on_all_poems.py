# This is example connector of culture.ru site with words
# Scrapes site for poems
# Created by Artem Anikieiev
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException


def main():
    time.sleep(5)
    driver = webdriver.Remote('http://localhost:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
    try:
        # vars
        all_pages = 785
        current_page = 1
        all_links = []

        # collect links loop
        while current_page <= all_pages:
            driver.get('https://www.culture.ru/literature/poems?page=' + str(current_page))
            all_divs_on_page = driver.find_elements_by_class_name("CHPy6")
            for div in all_divs_on_page:

                #author_link = div.find_element_by_xpath(".//div[@class='bMNap']/a").get_attribute('href')
                poem_link = div.find_element_by_xpath(".//div[@class='bMNap']/div[@class='_1ERrb']/a").get_attribute('href')
                all_links.append(poem_link)
                print(poem_link)

            current_page = current_page + 1

        with open('links.txt', 'w') as f:
            for line in all_links:
                f.write(line)
                f.write('\n')

        f.close()

        driver.quit()

    except NoSuchElementException as err:
        print(err)
        driver.quit()
        driver.close()

if __name__ == "__main__":
    main()
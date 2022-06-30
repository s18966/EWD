# Sends transformed poems to Kafka
# Created by Artem Anikieiev
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

from kafka import KafkaProducer
from json import dumps
import csv
class Producer:
    def __init__(self, urls, topic_name):
        self.urls = urls
        self.topic_name = topic_name
        self.producer = self.__create_producer()

    def __create_producer(self):
        producer = KafkaProducer(
            bootstrap_servers=self.urls,
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )
        return producer

    def send_poem(self, poem):
        self.producer.send(self.topic_name, value=poem)

class Poem:
    def __init__(self, author, name, poem, language, tags):
        self.author = author
        self.poem = poem
        self.language = language
        self.name = name
        self.tags = tags

def main():
    producer = Producer('localhost:9092', 'poems')
    time.sleep(5)
    driver = webdriver.Remote('http://localhost:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
    try:
        with open("links2.txt", "r") as f:
            with open("data.csv", "w") as csv_file:
                fieldnames = ["author", "poem", "language", "name", "tags"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for link in f:
                    driver.get(link)
                    #/html/body/div[1]/div/main/div/div[3]/a
                    #/html/body/div[1]/div/main/div/div[3]/div[1]
                    author = driver.find_element_by_class_name('IHYwd').text #"/html/body/div[1]/div/main/div/div[3]/div[@class='IHYwd']").text
                    title = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div[3]/div[1]").text
                    #texts = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div[3]/div[2]/div/div").find_elements_by_tag_name("p")
                    texts = driver.find_element_by_class_name('xZmPc').find_elements_by_tag_name("p")
                    tags = []
                    poem = ""
                    for text in texts:
                        t = text.text
                        poem = poem + t + "\n"
                    try:
                        tags_divs = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div[4]/div/div").find_elements_by_tag_name("div")
                        for div in tags_divs:
                            tag_text = div.find_element_by_xpath(".//a").text
                            tags.append(tag_text)
                    except NoSuchElementException:
                        tags = []
                    final_poem = Poem(author=author, name=title, poem=poem, language="RU", tags=tags)
                    producer.send_poem(final_poem.__dict__)
                    writer.writerow(final_poem.__dict__)
                    print(final_poem.__dict__)
            csv_file.close()

    except NoSuchElementException as err:
        print(err)
        driver.quit()
        driver.close()
    except KeyboardInterrupt:
        csv_file.close()

if __name__ == "__main__":
    main()
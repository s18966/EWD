# Processes poems and saves from topic to CSV
# Created by Artem Anikieiev

from kafka import KafkaConsumer
from json import loads
import csv

def main():
    with open('data.csv', mode='w') as csv_file:
        poems_writer = csv.writer(csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        poems_writer.writerow(["author", "poem", "language", "name", "tags"])
        consumer = KafkaConsumer('poems_consumer-1',
        bootstrap_servers=['localhost:9092'],
        group_id='poems-group-1',
        value_deserializer = lambda x: loads(x.decode('utf-8')))
        line_count = 0
        print("Started consuming")
        for message in consumer:
            msg = message.value
            author = msg["author"]
            poem = msg["poem"]
            language = msg["language"]
            name = msg["name"]
            tags = msg["tags"]
            poems_writer.writerow([author, poem, language, name, tags])
            print(f"conumed message {author} {poem}")
            line_count = line_count + 1

        print(f"Processed {line_count} lines")
        csv_file.close()

if __name__=="__main__":
    main()
import re
import spacy
import csv
from collections import Counter
from dewiki.parser import Parser

nlp = spacy.load("en_core_web_lg")
header = ["Title", "Named-entity", "Frequency"]

for i in range(1,21):

    with open(str(i)+".txt", "r", encoding="utf8") as file:
        title = file.readline().rstrip('\n')
        data = Parser().parse_string(file.read())
        data = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', '', data)
        data = re.sub(r'http\S+', '', data)
        data = re.sub('[\*\{\}\|\=]', '', data)
        encoded_string = data.encode("ascii", "ignore")
        data = encoded_string.decode()
        data = data.replace('\n', '')
        
    with open("out.txt", "w", encoding="utf8") as file:
        file.write(data)

    doc = nlp(data)

    entities = []
    for ent in doc.ents:
        entities.append(ent.text)
    
    ent_count = Counter(entities)

    with open(title + ".csv", "w", encoding="utf8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        for item in ent_count.items():
            writer.writerow([title, item[0], item[1]])
import re
import spacy
import csv
from collections import Counter
from dewiki.parser import Parser

nlp = spacy.load("en_core_web_lg")
header = ["Title", "Named-entity", "Sentence"]

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
        
    with open("out.txt", "w") as file:
        file.write(data)

    doc = nlp(data)

    with open(title + ".csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        for ent in doc.ents:
            writer.writerow([title, ent, ent.sent])

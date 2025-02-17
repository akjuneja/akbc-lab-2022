import re
from collections import Counter
import csv
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
from dewiki.parser import Parser

VERB = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
ADJECTIVE = ["JJ", "JJR", "JJS"]
header = ["Title", "POS Type", "POS", "Frequency"]

with open("Problem2_1.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

for i in range(1,21):

    with open(str(i)+".txt", "r", encoding="utf8") as file:
        title = file.readline().rstrip('\n')
        data = Parser().parse_string(file.read())
        data = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', '', data)
        data = re.sub(r'http\S+', '', data)
        data = re.sub('[\*\{\}\|\=\(\)\.\"\,\'\%\$\@\!]', '', data)
        encoded_string = data.encode("ascii", "ignore")
        data = encoded_string.decode()
        data = data.replace('\n', '')

    tokens = nltk.word_tokenize(data)

    tokens_lem = []
    for token in tokens:
        tokens_lem.append(wordnet_lemmatizer.lemmatize(token))

    tokens_tag = nltk.pos_tag(tokens_lem)
    tokens_tag_fd = nltk.FreqDist(tokens_tag)

    tmp = 0
    with open("Problem2_1.csv", "a", newline='') as file:
        writer = csv.writer(file)
            
        for (wt, fd) in tokens_tag_fd.most_common(): 

            if wt[1] in VERB:
                writer.writerow([title, "verb", wt[0], fd])
                tmp=tmp+1

            if wt[1] in ADJECTIVE:
                writer.writerow([title, "adjective", wt[0], fd])
                tmp=tmp+1

            if tmp >= 5:
                break
     

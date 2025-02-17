import sys
import re
import networkx as nx
import matplotlib.pyplot as plt

hypernymy_dict = {}
ENTITY = "entity"

def add_value(dict_obj, key, value, score):
    ''' Adds a key-value pair to the dictionary.
        If the key already exists in the dictionary,
        compare the score and keep the highest score'''
    if key not in dict_obj:
        dict_obj[key] = (value, score)
    elif (score > dict_obj[key][1] and value != dict_obj[key][0]):
        dict_obj[key] = (value,score)

def read_hypernymy_file():
    fin = open('webisalod-pairs.txt', 'r', encoding='utf8')

    for line in fin.readlines():
        comps = line.rstrip().split("\t")
        hypernymy = comps[0]
        score = float(comps[1])
        if(score > 0.50):
            ele = hypernymy.split(";")
            
            hyponym = ele[0]
            hyponym = re.sub("[+_]", " ", hyponym)
            hyponym = re.sub("\s+", " ", hyponym)
            hyponym = hyponym.strip()

            hypernym = ele[1].strip()
            hypernym = re.sub("[+_]", " ", hypernym)
            hypernym = re.sub("\s+", " ", hypernym)
            hypernym = hypernym.strip()
            
            add_value(hypernymy_dict, hyponym, hypernym, score)

    fin.close()

def show_taxonomy(input_file):
    G = nx.Graph()
    fin = open(input_file, 'r', encoding='utf8')

    for line in fin.readlines():
        i=0
        ele = line.rstrip()
        while ele in hypernymy_dict and i<4:
            parent = hypernymy_dict[ele][0]
            G.add_edge(parent, ele)
            ele = parent
            i+=1

        if ele != ENTITY and len(ele):
            G.add_edge(ENTITY, ele)

    fin.close()
    nx.draw(G, with_labels=True, font_size=10)
    plt.show()

'''
main function
'''
if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError('Expected exactly 1 argument: input file')
    read_hypernymy_file()    
    show_taxonomy(sys.argv[1])
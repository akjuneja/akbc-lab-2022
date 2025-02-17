'''
Created on Nov 8, 2019
Sample structure of run file run.py

@author: cxchu
'''

import sys
from sentence_transformers import SentenceTransformer, util
import torch

# collection of train file sentences
corpus = []
# collection of train file entity types
labels = []

def your_typing_function(input_file, result_file):
    '''
    This function reads the input file (e.g. test.tsv)
    and does typing all given entity mentions.
    The results is saved in the result file (e.g. results.tsv)
    '''
    print("***Model load start***")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("***Model load complete***")

    print("***Corpus encoding start***")
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
    print("***Corpus encoding complete***")

    fout = open(result_file, 'w', encoding='utf8')
    fin = open(input_file, 'r', encoding='utf8')

    for line in fin.readlines():
        comps = line.rstrip().split("\t")
        id = int(comps[0])
        entity = comps[1]
        sentence = comps[2]
        sentence_embedding = model.encode(sentence, convert_to_tensor=True)
        
        # compute similarity scores of the sentence with the corpus
        cos_scores = util.pytorch_cos_sim(sentence_embedding, corpus_embeddings)[0]
        idx = torch.argmax(cos_scores)
    
        # writing the entity type of most similar sentence(of training data)
        fout.write(str(id) + "\t" + str(labels[idx]) + "\n")

    fin.close()
    fout.close()
    print("*** Results.tsv is ready***")

'''
*** other code if needed
'''

def read_train_file():
    print("***Reading train file start***")
    
    fin = open('train.tsv', 'r', encoding='utf8')
    for line in fin.readlines():
        comps = line.rstrip().split("\t")
        entity = comps[0]
        label = comps[1]
        sentence = comps[2]
        corpus.append(sentence)
        labels.append(label)
    fin.close()

    print("***Reading train file complete***") 


'''
main function
'''
if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Expected exactly 2 argument: input file and result file')
    read_train_file()    
    your_typing_function(sys.argv[1], sys.argv[2])

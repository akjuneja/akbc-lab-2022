'''
Created on Nov 25, 2019
Sample structure of run file run.py

@author: cxchu
@editor: ghoshs
'''

import sys
import csv
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span

nlp = spacy.load("en_core_web_lg")

#Awards
matcher = Matcher(nlp.vocab)
pattern = [[{"POS": {"REGEX": "PROPN|NOUN|ADJ"}}, {"ORTH": "Prize"}], [{"POS":{"REGEX": "PROPN|NOUN|ADJ"}}, {"POS":{"REGEX": "PROPN|NOUN|ADJ"}}, {"ORTH": "Award"}],
[{"POS": {"REGEX": "PROPN|NOUN|ADJ"}}, {"ORTH": "Medal"}], [{"POS": {"REGEX": "PROPN|NOUN|ADJ"}}, {"ORTH": "Fellowship"}],  [{"ORTH": "Fellow"}, {"POS":{"REGEX": "CONJ|DET|AUX|ADP|PROPN|NOUN|ADJ"}}, {"POS":{"REGEX": "CONJ|DET|AUX|ADP|PROPN|NOUN|ADJ"}}, {"POS":{"REGEX": "CONJ|DET|ADP|PROPN|NOUN|ADJ"}}]]
matcher.add("awards", pattern)

def your_extracting_function(input_file, result_file):
    
    '''
    This function reads the input file (e.g. input.csv)
    and extracts the required information of all given entity mentions.
    The results is saved in the result file (e.g. results.csv)
    '''
    with open(result_file, 'w', encoding='utf8') as fout:
        headers = ['entity','dateOfBirth','nationality','almaMater','awards','workPlaces']
        writer = csv.writer(fout, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        
        with open(input_file, 'r', encoding='utf8') as fin:
            reader = csv.reader(fin)

            # skipping header row
            next(reader)
            
            for row in reader:
                entity = row[0]
                abstract = row[1]
                dateOfBirth, nationality, almaMater, awards, workPlace = [], [], [], [], []
                
                '''
                baseline: adding a random value 
                comment this out or remove this baseline 
                '''
                #dateOfBirth.append('1961-1-1')
                #nationality.append('United States')
                #almaMater.append('Johns Hopkins University')
                #awards.append('Nobel Prize in Physics')
                #workPlace.append('Johns Hopkins University')
                
                
                '''
                extracting information 
                '''

                dateOfBirth += extract_dob(entity, abstract)
                nationality += extract_nationality(entity, abstract)
                almaMater += extract_almamater(entity, abstract)
                awards += extract_awards(entity, abstract)
                workPlace += extract_workpace(entity, abstract)
                
                writer.writerow([entity, str(dateOfBirth), str(nationality), str(almaMater), str(awards), str(workPlace)])
        
    
'''
date of birth extraction funtion
'''    

def extract_dob(entity, abstract, **kwargs):
    dob = []
    '''
    === your code goes here ===
    '''
    doc = nlp(abstract)
    for ent in doc.ents:
        if ent.label_ == "DATE":
            dob.append(ent.text)
    return dob


'''
nationality extraction function
'''
def extract_nationality(entity, abstract, **kwargs):
    nationality = []
    '''
    === your code goes here ===
    '''
    doc = nlp(abstract)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            nationality.append(ent.text)
    return nationality
 

'''
alma mater extraction function
'''
def extract_almamater(entity, abstract, **kwargs):
    almaMater = []
    '''
    === your code goes here ===
    '''
    doc = nlp(abstract)
    for ent in doc.ents:
        if ent.label_ == "ORG":
            almaMater.append(ent.text)
    return almaMater
 

'''
awards extracttion function
'''
def extract_awards(entity, abstract, **kwargs):
    awards = []
    '''
    === your code goes here ===
    '''
    doc = nlp(abstract)
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = Span(doc, start, end, label=match_id)
        awards.append(span.text)
    return awards


'''
workplace extraction function
'''
def extract_workpace(entity, abstract, **kwargs):
    workPlace = []
    '''
    === your code goes here ===
    '''
    doc = nlp(abstract)
    for ent in doc.ents:
        if ent.label_ == "ORG":
            workPlace.append(ent.text)
    return workPlace


'''
main function
'''
if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Expected exactly 2 argument: input file and result file')
    your_extracting_function(sys.argv[1], sys.argv[2])

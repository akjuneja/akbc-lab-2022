`'''
Created on Nov 25, 2019
Sample structure of run file run.py

@author: cxchu
'''

import sys
import spacy

nlp = spacy.load("en_core_web_sm")

def your_extracting_function(input_file, result_file):
    
    '''
    This function reads the input file (e.g. sentences.tsv)
    and extracts all SPO per line.
    The results are saved in the result file (e.g. results.txt)
    '''
    with open(result_file, 'w', encoding='utf8') as fout:
        with open(input_file, 'r', encoding='utf8') as fin:
            id = 1
            for line in fin:
                line = line.rstrip()
                '''
                baseline: running dependency, return head verb, nominal subject and directed object
                comment out or remove when running your code
                verbs = {key: {'subject': text, 'object': text}}
                verbs = spo_baseline(line)
                '''
                '''
                end baseline
                '''

                '''
                Extracting SPO
                === your code goes here ===
                '''
                verbs = extract_spo(line)
                '''
                formatiing dict compatible with oie reader
                '''
                if len(verbs) > 0:
                    res = ''

                    for key, value in verbs.items():
                        if value['subject'] != '' and value['object'] != '':
                            res += str(id) + '\t"' + value["subject"] + '"\t"' + key + '"\t"' + value["object"] + '"\t0\n'
                    if res != '':
                        fout.write(line + "\n")
                        fout.write(res) 
                        id += 1
'''
baseline implementation
'''
def spo_baseline(line):
    verbs = {}
    doc = nlp(line)
    for token in doc:
        key=token.head.text;
        if(token.head.pos_ == "VERB" and key not in verbs.keys()):
            verbs[key] = {"subject":"","object":""};
        if(token.dep_ == "nsubj" and token.head.pos_ == "VERB"):
            verbs[key]["subject"] = token.text;

        elif(token.dep_ == "dobj" and token.head.pos_ == "VERB"):
            verbs[key]["object"] = token.text;
    return verbs

def extract_spo(line):
    verbs = {}
    doc = nlp(line)
    # Storing the list of tokens and their infomation
    tokens = [token for token in doc]

    # Few initailizations
    key = ""
    sub = ""
    obj = ""
    place = 0
    oldobj = ""
    temp = ""

    #Iterating over the tokens
    for i in range(len(tokens)):

        # Condition when we find a verb which is not existing in the verbs dictionary
        if (tokens[i].pos_ == "VERB" and key not in verbs.keys()):

            #if the next token is a subordinating conjunction then concatinate it with the verb
            if tokens[i + 1].pos_ == "SCONJ":
                key += tokens[i].text + " " + tokens[i + 1].text
                place = i + 2

            # if there is a verb with hypen before them like co-sponsored
            elif tokens[i-1].text == "-" and tokens[i-1].pos_ == "VERB" and tokens[i-2].pos_ == "VERB":
                key += tokens[i - 2].text + tokens[i - 1].text + tokens[i].text
                place = i + 1
                if tokens[i - 1].text in verbs:
                    verbs.pop(tokens[i - 1].text)
                if tokens[i - 2].text in verbs:
                    verbs.pop(tokens[i - 2].text)

            # else just keep the verb
            else:
                key += tokens[i].text
                place = i + 1

            # to obtain the object iterate over the token list after the verb
            tokens_temp = tokens[place:]
            for j in range(len(tokens_temp)):

                # stop if a Punctuation is encountered
                if tokens_temp[j].pos_ == "PUNCT":
                    break

                #else add all the tokens
                else:
                    obj += tokens_temp[j].text + " "

            # if the subject is empty
            if sub == "":
                # to get the subject iterate over the token list till the verb
                tokens_temp = tokens[:place]
                for j in range(len(tokens_temp)):
                    # if the current word is the verb we are working with then add the previous word as the subject
                    if tokens_temp[j].text == tokens[i].text:
                        for rev in range((j - 1), -1, -1):
                            if not tokens[rev].pos_ == "VERB":
                                sub = tokens_temp[rev].text + " " + sub
                            elif tokens[rev].pos_ == "VERB" and ((tokens[rev].text)[0]).isupper():
                                sub = tokens_temp[rev].text + " " + sub

            # writing the subject and object pair for the verb
            verbs[key] = {"subject": sub.strip(), "object": obj.strip()}

            # retaining the old subject
            oldobj = obj.strip()

            key = ""
            sub = ""
            obj = ""

        # if there is an auxiliary then we add then to the verb phrase
        elif tokens[i].pos_ == "AUX":
            key += tokens[i].text + " "

        # to obtain the subject after the verb and it should not be subordinating conjunction
        elif not tokens[i].pos_ == "SCONJ":
            sub += tokens[i].text + " "
            temp = sub
            sub = ""
            # we are cleaning the subject to remove the content of the previous verb's object
            for x in temp.split():
                if (not ((x in oldobj) or (x in ",./?><:"'{}|[]\!@#$%^&*()_+-=~'))):
                    sub += x + " "
            temp = ""

    # if the verb is at head then take the subject and object which are after the verb
    if tokens[0].pos_ == "VERB":
        key = tokens[0].text
        if key in verbs:
            verbs.pop(key)
        sub = ""
        obj = ""
        tokens_temp = tokens[1:]
        for y in range(len(tokens_temp)):
            if tokens_temp[y].pos_ == "ADP":
                tokens_temp2 = tokens_temp[y:]
                for z in range(len(tokens_temp2)):
                    if tokens_temp2[z].pos_ == "NOUN":
                        obj += tokens_temp2[z].text + " "
                        verbs[key] = {"subject": sub.strip(), "object": obj.strip()}
                        oldobj = obj.strip()
                        key = ""
                        sub = ""
                        obj = ""
                        break
                    else:
                        obj += tokens_temp2[z].text + " "
            else:
                sub += tokens_temp[y].text + " "

    # removing none verb tuples
    if '' in verbs:
        verbs.pop('')
    return verbs
    
'''
*** other code if needed
'''    
    
    
'''
main function
'''
if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Expected exactly 2 argument: input file and result file')
    your_extracting_function(sys.argv[1], sys.argv[2])

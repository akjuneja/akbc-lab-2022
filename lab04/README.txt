Taxonomy Induction

***Approach***
I have pre processed the webisalod-pairs.txt and removed the unecessary characters from the hyponym and hypernym and saved the pair in dictionary along with scores > 0.5. In case of duplication {(hyponym_1-hypernym_1) (hyponym_1-hypernym_2)}, only the highest scoring pair is saved.
Graph is constructed using these pair relations.
##############


***Required Libraries***
Name: networkx
Version: 2.5.1

Name: matplotlib
Version: 3.3.0
#########################


***Note***
Code might take 2-3 mins to run
##########


***References***
https://networkx.org/documentation/latest/tutorial.html
################
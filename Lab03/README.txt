Named Entity Recognition Classification

***Approach***
I have used the following pre-trained sentence-transformer model to maps sentences to a 384 dimensional dense vector space and used for semantic similarity.
https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L6-v2

I checked the semantic similarity score of test file sentence with all the sentences of train file and assign the entity type of sentence with highest score.
##############


***Required Libraries***
pip install -U sentence-transformers
Version: 2.2.0

pip3 install torch torchvision torchaudio
Version: torch-1.10.2 torchaudio-0.10.2 torchvision-0.11.3
#########################


***Note***
Following code might take 8-10 mins to run where it is encoding all the sentences of train file.
corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
##########


***Results***
Strict: Using exact matching:
        Macro Precision, Recall and F1: 0.4359000000000001      0.4351416666666666      0.4355205032288927
        Micro Precision, Recall and F1: 0.38001573564122737     0.38764044943820225     0.3837902264600715
Loose: Using exact matching on the lemma of the head-word of the type:
        Macro Precision, Recall and F1: 0.5027750000000001      0.5016464285714285      0.5022100802523131
        Micro Precision, Recall and F1: 0.44544708777686626     0.45174708818635606     0.4485749690210657
##############


***References***
https://www.sbert.net/docs/pretrained_models.html
https://towardsdatascience.com/semantic-similarity-using-transformers-8f3cb5bf66d6
################
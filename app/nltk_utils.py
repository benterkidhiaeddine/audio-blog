import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer


stemmer = PorterStemmer()



def tokenize(sentance):
    return nltk.word_tokenize(sentance)


def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence,all_words):
    """
    tokenized_sentence = ["hello","good","you"]
    words = ["hello","what","good","fine","you"]
    bag =          [1,0,1,0,1]
    """
    
    tokenized_sentence  = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words),dtype=np.float32)
    for idx , w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0
    
    return bag


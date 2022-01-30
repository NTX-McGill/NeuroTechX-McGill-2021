from collections import Counter
import os 
from utils import * 

def train_model(corpus_path, save_path=None, verbose=False):
    '''
    loading the probability dicts 
    :corpus_path: path to the corpus file 
    :save_path : path where to save the model (optional) 
    '''

    corpus = load_corpus(corpus_path)
    # corpus = "My name is Rebecca. I am an electrician. I am an interesting person."
    #loads all the unique words in the corpus, only [a-z] characters left 
    WORDS = re_split(corpus)
    # print(WORDS)

    #number of times of each word appears
    WORDS_MODEL = Counter(WORDS)

    #finding all (word a, word b) pairs in text
    WORD_TUPLES = list(chunks(WORDS, 2))
    print(WORD_TUPLES)
    
    #number of times each (word a, word b) pair appears 
    WORD_TUPLES_MODEL = {first: Counter()
                         for first, second in WORD_TUPLES}
    
    #populate counts 
    for tup in WORD_TUPLES:
        WORD_TUPLES_MODEL[tup[0]].update([tup[1]])
        # try:
        #     WORD_TUPLES_MODEL[tup[0]].update([tup[1]])
        # except:
        #     # hack-y fix for uneven # of elements in WORD_TUPLES
        #     pass
    if verbose: 
        print("Loaded {} unique words and {} unique tuples into models".format(len(WORDS_MODEL), len(WORD_TUPLES_MODEL)))
        
    if save_path:
        save_models(WORDS_MODEL, WORD_TUPLES_MODEL, save_path)
        print("Saved models to {}".format(save_path))

save_path = '/Users/rebeccasalganik/Documents/School/NT/model_test2.pkl'
train_model('/Users/rebeccasalganik/Documents/School/NT/NeuroTechX-McGill-2021/ML_new/text.txt', save_path, verbose=True)
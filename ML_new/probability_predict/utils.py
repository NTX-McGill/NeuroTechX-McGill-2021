import re 
import pickle 
import argparse

#used for lowercasing and removing spaces from prefix 
def norm_rsplit(text,n): return text.lower().rsplit(' ', n)[-n:]

#removing all non [a-z] characters 
def re_split(text): return re.findall('[a-z]+', text.lower()) #[a-z]+

def clean(word):
    word = word.lower()  
    regex = re.compile('[^a-z]')
    return regex.sub('', word)

#splits sentence into (word a, word b) tuple pairs 
def chunks(l, n):
    for i in range(0, len(l) - n + 1):
        yield l[i:i+n]

#load training corpus 
def load_corpus(corpus_path): 
    '''
    :param corpus_path: file path to where you have the downloaded corpus 
    '''
    with open(corpus_path, 'r', encoding='utf-8') as corpus:
        return str(corpus.read()) 
    
#saving parameters from trained models
def save_models(word_model, tuple_model, save_path):
    ''' 
    :param word_model: unique word count dict to save 
    :param tuple_model: (word a, word b) tuple count dict to save 
    :param save_path: location to save models 
    '''
    pickle.dump({'words_model': word_model,
                 'word_tuples_model': tuple_model},
                open(save_path, 'wb'),
                protocol=2)

#loads the pre-trained models for inference 
def load_models(model_path): 
    ''' 
    :param model_path: location where pre-trained models are left
    :returns: WORD_MODEL (unique word count dict) and WORD_TUPLES_MODEL (word a, word b) tuple count dict)
    '''
    mod = pickle.load(open(model_path, "rb"))
    WORDS_MODEL = mod['words_model']
    WORD_TUPLES_MODEL = mod['word_tuples_model']
    return WORDS_MODEL, WORD_TUPLES_MODEL

def process_input_prefix(prefix): 
    return clean(prefix[0])
    #remove punctuation, lowercase 
    #
    # print(prefix, prefix[0])
    # re.findall('[a-z]+', text.lower())
    # print(type(prefix), type(prefix[0]))
    # return [clean(p) for p in prefix]  

# def parse_args(): 
#     parser = argparse.ArgumentParser()
#     parser.add_argument("echo")
#     args = parser.parse_args()
#     print(args.echo)

def clean_and_parse(input):

    last_space = True if input[-1:] == " " else False
    if last_space:
        input = input[0:-1]
    split = input.split(" ")

    return ([clean(s) for s in split], last_space)


#Used to define potential mistakes for last letter of prefix to autocomplete 
NEARBY_KEYS = {
    'a': 'qwsz',
    'b': 'vghn',
    'c': 'xdfv',
    'd': 'erfcxs',
    'e': 'rdsw',
    'f': 'rtgvcd',
    'g': 'tyhbvf',
    'h': 'yujnbg',
    'j': 'uikmnh',
    'k': 'iolmj',
    'l': 'opk',
    'm': 'njk',
    'n': 'bhjm',
    'o': 'iklp',
    'p': 'ol',
    'q': 'wa',
    'r': 'edft',
    's': 'wedxza',
    't': 'rfgy',
    'u': 'yhji',
    'v': 'cfgb',
    'w': 'qase',
    'x': 'zsdc',
    'y': 'tghu',
    'z': 'asx'
    }



import re 
import pickle 
import argparse


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

def clean_and_parse(input):

    last_space = True if input[-1:] == " " else False
    if last_space:
        input = input[0:-1]
    split = input.split(" ")

    return ([clean(s) for s in split], last_space)


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
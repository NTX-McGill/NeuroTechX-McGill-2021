from utils import NEARBY_KEYS, load_models, process_input_prefix
from collections import Counter 
import sys 
import argparse 

def this_word(prefix, top_n=3):
    '''
    :prefix: one word that isn't complete to be autocompleted 
    :top_n: number of suggested words for autocompletion
    :returns: n suggested autocompletions for prefix 
    '''
    try:
        return [(k, v) for k, v in WORDS_MODEL.most_common()
                if k.startswith(prefix)][:top_n]
    except KeyError:
        raise Exception("train/load model first")


def this_word_given_last(prev_prefix, cur_prefix, top_n=3):
    '''
    :prev_prefix: last complete word of prefix 
    :cur_prefix: word that isn't complete to be autocompleted 
    :top_n: number of suggested words for autocompletion
    :returns: n suggested autocompletions for prefix 
    NOTE: Will also add common "misspellings" based on key proximity --> can be modified for frequency proximity
    '''

    possible_cur_prefixes = [cur_prefix[:-1]+char
                             for char in NEARBY_KEYS[cur_prefix[-1]]
                             if len(cur_prefix) > 1]

    possible_cur_prefixes.append(cur_prefix)

    probable_words = {w:c for w, c in
                      WORD_TUPLES_MODEL[prev_prefix.lower()].items()
                      for sec_word in possible_cur_prefixes
                      if w.startswith(sec_word)}

    return Counter(probable_words).most_common(top_n)

def predict(prefix):
    # autcomplete_options = this_word(prefix)
    autcomplete_options = this_word_given_last("my", "name")

    # print("Recieved prefix:{} \n autocomplete options:{}".format(prefix, autcomplete_options))

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", type=str, default = '/Users/rebeccasalganik/Documents/School/NT/model_test2.pkl', help= "location for pre-trained model pickle")
    parser.add_argument("-p", type=str, nargs='+', help="prefix to autocomplete")
    parser.add_argument("-v", type=bool, help="verbose setting for testing", default=True)
    args = parser.parse_args()
    WORDS_MODEL, WORD_TUPLES_MODEL = load_models(args.m)

    if args.v: 
        print("Prefix is: {}".format(args.p))
    
    prefix = process_input_prefix(args.p)
    print("cleaned prefix", prefix)

    # predict('na')
#     # prefix = process_input_prefix(args.p)
    
    # if not prefix: 
    #     raise Exception ("please feed prefix")
    # if len(prefix) == 1: 
    #     autcomplete_options = this_word(prefix)
    # else: 
    #     autcomplete_options = this_word_given_last(prefix[-2], prefix[-1])

    # if args.v: 
    #     print("Recieved prefix:{} \n autocomplete option:{}".format(prefix, autcomplete_options))
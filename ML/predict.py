from utils import NEARBY_KEYS, load_models, process_input_prefix, clean_and_parse
from collections import Counter 
import sys, os 
import argparse 
import torch
import tensorflow
from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline, set_seed

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
    autcomplete_options = this_word(prefix)
    # autcomplete_options = this_word_given_last("my", "name")
    return autcomplete_options

def next_word(prefix, num_options=5): 
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
    params = {'max_length': 10, 
          'do_sample': True, 
          'top_k': 10, 
          'no_repeat_ngram_size': 2,  
          'labels': inputs["input_ids"]}
    
    inputs = tokenizer(prefix, return_tensors="pt")
    input_len = len(inputs['input_ids'][0])
    top_k_multi_output = model.generate(**inputs, **params, num_return_sequences=5)
    
    return top_k_multi_output[:, input_len:input_len+1]

def interactive_test_loop():
    prefix = []
    print("Please type your prefix: (write 'stop' if you want to stop testing and 'clear' if you want to erase everything)") 


    while True:
        txt = input()
        cleaned, last_space = clean_and_parse(txt)
        print("result of cleaner: ", cleaned, last_space)

        if cleaned == ["stop"]:
            print("Thank you for testing!") 
            exit() 
        if cleaned == ["clear"]:
            print("***RESET***")
            prefix = []  
            print("Please type your prefix: (write 'stop' if you want to stop testing and 'clear' if you want to erase everything)")
            continue   
        prefix.extend(cleaned)  
        print("-->", prefix)
        options = predict(prefix[-1])
        print("options:", options)


        '''
        TO DO: 
        1. Write cleaning function --> lowercase and strip non [a-z]  characters 
        2. Cover all the autocompletion cases:  
            2.1. user enters a single word --> this_word() 
            2.2. user enters a second word --> this_word_given_last()
            2.3. user enters a sentence --> break it up and decide how to handle 
        3. Add a functionality for user to select the prefix (just for testing and later comparison) 
        '''
        # cleaned = clean_input(prefix)
        # options = predict(cleaned)
        

if __name__ == '__main__':

    '''
    run in probability_predict as working directory
    example command used: python predict.py -m model_test2.pk1
    '''

    PATH = os.path.dirname(os.path.realpath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="relative data path for model file")
    args = parser.parse_args()
    model_file = str(args.model)

    WORDS_MODEL, WORD_TUPLES_MODEL = load_models(os.path.join(PATH, model_file))
    interactive_test_loop()

    # parser = argparse.ArgumentParser()
    # parser.add_argument("-m", type=str, default = '/Users/rebeccasalganik/Documents/School/NT/model_test2.pkl', help= "location for pre-trained model pickle")
    # parser.add_argument("-p", type=str, nargs='+', help="prefix to autocomplete")
    # parser.add_argument("-v", type=bool, help="verbose setting for testing", default=True)
    # args = parser.parse_args()
    # WORDS_MODEL, WORD_TUPLES_MODEL = load_models(args.m)

    # if args.v: 
    #     print("Prefix is: {}".format(args.p))
    
    # prefix = process_input_prefix(args.p)
    # print("cleaned prefix", prefix)

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

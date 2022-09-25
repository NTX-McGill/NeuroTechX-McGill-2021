from dcp.ml.utils import NEARBY_KEYS, load_models, process_input_prefix, clean_and_parse
from collections import Counter 
import sys, os 
import argparse 
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline, set_seed



def autocomplete(prefix, model, top_n=3):
    '''
    :prefix: one word that isn't complete to be autocompleted 
    :top_n: number of suggested words for autocompletion
    :returns: n suggested autocompletions for given prefix 
    '''
    
    options = [k for k, v in model.most_common()
            if k.startswith(prefix)][:top_n]
    if len(options) < top_n: 
        options.extend([""]*top_n)
    return list(options)[:min(len(options), top_n)]
    
def next_word_tuple(prefix, model, top_n=3):
    '''
    :prefix: last word of the sentence  
    :top_n: number of suggested words for next words
    :returns: n suggested next words for the given last word 
    NOTE: Will also add common "misspellings" based on key proximity --> can be modified for frequency proximity
    '''
    possible_cur_prefixes = [prefix[:-1]+char
                             for char in NEARBY_KEYS[prefix[-1]]
                             if len(prefix) > 1]

    possible_cur_prefixes.append(prefix)

    options = list({w for w, c in
                model[prefix].items()
                for prefix in possible_cur_prefixes}) 
    
    #padding for length
    if len(options) < top_n: 
        options.extend([""]*top_n)
    return list(options)[:min(len(options), top_n)]

def next_word_BERT(prefix, top_n=3): 
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
    params = {'max_length': 10, 
          'do_sample': True, 
          'top_k': 10, 
          'no_repeat_ngram_size': 2,  
          'labels': inputs["input_ids"]}
    
    inputs = tokenizer(prefix, return_tensors="pt")
    input_len = len(inputs['input_ids'][0])
    top_k_multi_output = model.generate(**inputs, **params, top_n=top_n)
    
    return top_k_multi_output[:, input_len:input_len+1]

def dispatch(sentence, top_n=3):
    '''
    :sentence: sentence up till now 
    :top_n: number of options to return 
    :returns: 
        {mode: int, options: list of strings}
        - mode: autocompletion, prediction 
        - options: list of autocompletion or next word suggestion (of length top_n) --> default 3 
    '''

    WORDS_MODEL, WORD_TUPLES_MODEL = load_models("./dcp/ml/model_test3.pk1")

    prefix, last_space = clean_and_parse(sentence)
    if last_space : 
        options = next_word_tuple(prefix[-1], WORD_TUPLES_MODEL)
    else: 
        options = autocomplete(prefix[-1], WORDS_MODEL)
    mode = "completion" if last_space else "prediction" 
    return {'mode': mode, 'options': options}  


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
    

from utils import NEARBY_KEYS, load_models, process_input_prefix, clean_and_parse
from collections import Counter 
import sys, os 
import argparse 
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline, set_seed



def autocomplete(prefix, top_n=3):
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

def next_word_tuple(prev_prefix, cur_prefix, top_n=3):
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

def next_word_BERT(prefix, num_options=3): 
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

def dispatch(prefix, last_space): 
    if last_space: 
        sentence = " ".join(prefix)
        options = next_word_BERT(sentence)
    else: 
        incomplete_word = prefix[-1]
        options = this_word(incomplete_word)

    print("OPTIONS:", options)

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


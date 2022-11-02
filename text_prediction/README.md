# Text Prediction

## Dependancies 
- [Numpy](https://numpy.org/) 
- [PyTorch](https://pytorch.org/)
- [Scipy](https://www.scipy.org/)
- [Tensorflow](https://www.tensorflow.org/)
- [Transformers](https://huggingface.co/docs/transformers/index)
- [Pickle](https://docs.python.org/3/library/pickle.html)
- [Re](https://docs.python.org/3/library/re.html)

## Files

The code consists of three files: 
* `utils.py`: Contains functions for cleaning, parsing and loading pickle of models. There is also a dictionary of nearby keys for possible mistyping and bad letter prediction.

* `train.py`: Creates word tuple models based on selected dataset and saves os.file paths of models.

  * To train the model: 
    1. Load a corpus and split words into an array.
    2. Create an model of 2-tuple or bigrams of the word frequencies and one of unigrams or single words
    3. Save pickle file of models

* `predict.py`: Contains functions for next word predictions and an interative testing loop for prediction tests.

  * To test a model:
    1. Use command: python predict.py -m model_test3.pk1
    2. Follow terminal commands

### Corpora

`text.txt`:[Project Gutenberg's Moby Dick; or The Whale](https://www.gutenberg.org/files/2701/2701-h/2701-h.htm)
- 213 533 words
- Published 1851
- American
- Open Source

`tv_text.txt`:[Sample of the TV Corpus](https://www.corpusdata.org/formats.asp)
- 21 000 000 words in linear text of a completely random sample of the full corporus.
- British and American
- Works from 1950-2018
- Every 200 words, ten words are removed and are replaced with ten "@".

## Model

Bigram with Markov Chains.

This model learns the frequencies of words and pairs (bigrams) of words in a corpus to autocomplete by the most top 3 likely word by the typed letters. 

Markov chains reduce possible next words under the assumption that the current or last word is only needed to predict the next; the markov property. 

A large and diverse corpus is assumed to asymptoticlly approximate every day English.

### Features

Autocomplete:
- Autocompletes an incomplete word by the pevious prefix characters.

Next Word Prediction
- Autocomplete the next word given a previous word and an incomplete word's prefixes. 

Example:

| Incomplete Word | User Character Selection | Autocomplete Options |
| :--------------- |:--:| :----------------------------: |
| 'h'             | 'e' | (1. he , 2. her , 3. help)   |
| 'he'            | 'l' | (1. he , 2. her , 3. help)   |
| 'hel'           | '2' | (1. help, 2. hello, 3. held) |
| 'hello '        | 'w' | ( 1. alex , 2. bonjour , 3. hi ) |
| 'hello w'       | '1' | ( 1. world , 2. weekend  , 3. windchill ) |
| 'hello world '  | ''  | () |


# Machine Learning

## Dependancies 
- [Numpy](https://numpy.org/) 
- [PyTorch](https://pytorch.org/)
- [Scipy](https://www.scipy.org/)
- [Tensorflow](https://www.tensorflow.org/)
- [Transformers](https://huggingface.co/docs/transformers/index)
- [Pickle](https://docs.python.org/3/library/pickle.html)
- [Re](https://docs.python.org/3/library/re.html)

### Corpora

[Project Gutenberg's Moby Dick; or The Whale](https://www.gutenberg.org/files/2701/2701-h/2701-h.htm)
- 213 533 words
- Published 1851
- American
- Open Source

[Sample of the TV Corpus](https://www.corpusdata.org/formats.asp)
- 21 000 000 words
- British and American
- Works from 1950-2018
- Every 200 words, ten words are removed and are replaced with ten "@".

## Model

N-Gram with Markov Chains. 

### Features

Autocomplete:
- Autocompletes an incomplete word by the pevious prefix characters.

Next Word Prediction
- Autocomplete the next word given a previous word and the incomplete word's prefixes. 

Example:

| Incomplete Word | User Character Selection | Autocomplete Options |
| --------------- |--| ---------------------------- |
| 'h'             | 'e' | (1. he , 2. her , 3. help)   |
| 'he'            | 'l' | (1. he , 2. her , 3. help)   |
| 'hel'           | '2' | (1. help, 2. hello, 3. held) |
| 'hello '        | 'w' | ( 1. alex , 2. bonjour , 3. hi ) |
| 'hello w'       | '1' | ( 1. world , 2. weekend  , 3. windchill ) |
| 'hello world '  | ''  | () |

## Files

The code consists of three files: 
1. `utils.py`:
2. `train.py`: 
3. `predict.py`: 

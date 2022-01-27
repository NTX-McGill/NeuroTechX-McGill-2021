# Word prediction and completion
A Python implementation of word prediction and completion, created for CSCI 4152 Natural Language Processing. 

The program's default interactive mode takes a word or partial word as input, and provides a suggestion for completion and suggests the next word by the following logic:
- If the input word is in the dictionary, predict the next word using an ngram model.
- If the input word is not in the dictionary, check the suffix tree for a list of possible completions, and apply a metric to choose the best one.

# Sophia's Notes
I have been running the code with the command `python wordprediction.py -m interactive`, and then interacting with the command line to test various words and phrases. 
- It is currently training on the same corpus as Rebecca's (in train_big dir)
- I have been testing with inputs that have no punctuation or numbers, will possibly need some input cleaning
- A new trie is built every time it runs, so I need to change it to save it to a file and then be able to load trie in
- There are some confusing results where it thinks that single letters like "p" are a whole word. Currently trying to take a closer look at the pygtrie.CharTrie().has_key() function to understand why

Example results:

    Enter word or partial word: pow
    Partial word detected.

    Here are the word completion predictions:
    power, powers, powerful

---------------------------------------------------------------------

    Enter word or partial word: I ha
    Whole word detected. Here are the top next word predictions:
    ha, the, you

    Here are the word completion predictions:
    have, had, havent

----------------------------------------------------------------------

    Enter word or partial word: today you can
    Whole word detected. Here are the top next word predictions:
    be, only, i

    Here are the word completion predictions:
    cant, cannot


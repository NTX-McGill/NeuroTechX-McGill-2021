# Word prediction and completion
A Python implementation of word prediction and completion, created for CSCI 4152 Natural Language Processing. 

The program's default interactive mode atkes a word or partial word as input, and provides a suggestion for completion and suggests the next word by the following logic:
- If the input word is in the dictionary, predict the next word using an ngram model.
- If the input word is not in the dictionary, check the suffix tree for a list of possible completions, and apply a metric to choose the best one.

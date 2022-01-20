import pandas as pd
import numpy as np
import textdistance
import re
import time
from collections import Counter


def main():
    with open('text.txt', 'r') as f:
        file_name_data = f.read()
        file_name_data = file_name_data.lower()
        # print(file_name_data)
        # file_name_data = re.sub('\n','',file_name_data)
        # file_name_data = re.sub('[^a-zA-Z]+','',file_name_data)
        # word_pattern = "^\S*\s|\s\S*\s|\s\S*$"
        words = re.findall('\w+', file_name_data)
        # print(words)
        # exit()
    Words = set(words)
    # print(Words)
    word_freq = Counter(words)
    probs = {}
    Total = sum(word_freq.values())
    for k in word_freq.keys():
        probs[k] = word_freq[k] / Total

    input_word = "accomodate" #acheive,accross,agressive
    input_word2 = 'acheive'
    input_word3 = 'accross'
    input_word4 = 'agressive'
    input_word5 = 'yesterd'
    if input_word5 in Words:
        print ('Correct word')
    else:
        b = time.time()
        sim = [1 - (textdistance.Jaccard(qval=2).distance(v, input_word5)) for v in word_freq.keys()]
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df = df.rename(columns={'index': 'Word', 0: 'Prob'})
        df['Similarity'] = sim
        output = df.sort_values(['Similarity', 'Prob'], ascending=False).head()
        a = time.time()
        print (output)
        print("PROCESSING TOOK:{}".format(a - b))
if __name__ == "__main__":
    main()
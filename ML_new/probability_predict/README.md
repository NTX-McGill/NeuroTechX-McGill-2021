The code consists of three files: 
    1. utils.py
    2. train.py 
    3. predict.py

If you want to change the corpus on which the model is trained: 
    1. Download it and store on your computer 
    2. In train.py change the data_path variable 
    3. Run the file - you should have the "model" saved under whatever you put as save_path. 

If you want to test the model: 
    1. Make sure you have trained the model (see above)
    2. In predict.py there are two functions: 
        2.1. this_word_given_last(): 
            2.1.1. this takes a single complete word and an incomplete word and predicts possible autocompletions for second word
        2.2. this_word(): 
            2.2.1 this takes an incomplete word and suggests autocompletions for it. 

Open Projects: 
    1. Make sure the words are being cleaned properly 
    2. Write a pre-processing function for csv datasets (currently it's only compatible with txt formatting)
    3. predict() needs to take input from user and dispatch it to the two autocomplete functions 

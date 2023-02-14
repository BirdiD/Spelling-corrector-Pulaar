import re
from collections import Counter
import numpy as np
import pandas as pd

def process_data(file_name):
    """
    Input: 
        A file_name  
    Output: 
        words: a list containing all the words in the text file in lower case. 
    """
    words = [] 
    file = open(file_name).read()
    words = re.findall(r'\w+', file.lower())
    return words



def get_count(word_l):
    '''
    Input:
        word_l: a set of words representing the corpus. 
    Output:
        word_count_dict: The wordcount dictionary where key is the word and value is its frequency.
    '''   
    word_count_dict = {}  
    word_count_dict = Counter(word_l)
    return word_count_dict

def get_probs(word_count_dict):
    '''
    Input:
        word_count_dict: The wordcount dictionary where key is the word and value is its frequency.
    Output:
        probs: A dictionary where keys are the words and the values are the probability that a word will occur. 
    '''
    probs = {} 
    probs = {word: word_count_dict[word]/sum(word_count_dict.values()) for word in word_count_dict}
    return probs

def delete_letter(word, verbose=False):
    '''
    Input:
        word: the string/word for which we will generate all possible words 
                in the vocabulary which have 1 missing character
    Output:
        delete_l: a list of all possible strings obtained by deleting 1 character from word
    '''
    
    split_l = [(word[:i],word[i:]) for i in range(len(word) + 1)]
    delete_l = [L + R[1:] for L, R in split_l if R]

    if verbose: print(f"Input word {word}, \nsplit_l = {split_l}, \ndelete_l = {delete_l}")

    return delete_l


def switch_letter(word, verbose=False):
    '''
    Input:
        word: input string
     Output:
        switches: a list of all possible strings with one adjacent charater switched
    ''' 
    
    switch_l = []
    split_l = []
    
    split_l = [(word[:i],word[i:]) for i in range(len(word) + 1)]
    switch_l = [L + R[1] + R[0] + R[2:] for L, R in split_l if len(R)>1]
    
    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nswitch_l = {switch_l}") 

    return switch_l

def replace_letter(word, verbose=False):
    '''
    Input:
        word: the input string/word 
    Output:
        replaces: a list of all possible strings where we replaced one letter from the original word. 
    ''' 
    
    letters = 'abɓcdɗefghijklmnŋñoprstuwyƴz'
    
    split_l = [(word[:i],word[i:]) for i in range(len(word) + 1)]
    replace_l = [L + c + R[1:] for L, R in split_l if R for c in letters]

    replace_set = set(replace_l)
    replace_l = sorted(list(replace_set))
    
    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nreplace_l {replace_l}")   
    
    return replace_l

def insert_letter(word, verbose=False):
    '''
    Input:
        word: the input string/word 
    Output:
        inserts: a set of all possible strings with one new letter inserted at every offset
    ''' 
    letters = 'abɓcdɗefghijklmnŋñoprstuwyƴz'
    
    split_l = [(word[:i],word[i:]) for i in range(len(word) + 1)]
    insert_l = [L + c + R for L, R in split_l for c in letters]

    if verbose: print(f"Input word {word} \nsplit_l = {split_l} \ninsert_l = {insert_l}")
    
    return insert_l


def edit_one_letter(word, allow_switches = True):
    """
    Input:
        word: the string/word for which we will generate all possible wordsthat are one edit away.
    Output:
        edit_one_set: a set of words with one possible edit. Please return a set. and not a list.
    """
    
    edit_one_set = set()
        
    edit_one_set.update(delete_letter(word))
    if allow_switches:
        edit_one_set.update(switch_letter(word))
    edit_one_set.update(replace_letter(word))
    edit_one_set.update(insert_letter(word))

    return edit_one_set


def edit_two_letters(word, allow_switches = True):
    '''
    Input:
        word: the input string/word 
    Output:
        edit_two_set: a set of strings with all possible two edits
    '''
    
        
    edit_two_set = list(e2 for e1 in edit_one_letter(word) for e2 in edit_one_letter(e1))
    edit_two_set = set(edit_two_set)
    
    return edit_two_set

def get_corrections(word, probs, vocab, n=5, verbose = False):
    '''
    Input: 
        word: a user entered string to check for suggestions
        probs: a dictionary that maps each word to its probability in the corpus
        vocab: a set containing all the vocabulary
        n: number of possible word corrections you want returned in the dictionary
    Output: 
        n_best: a list of tuples with the most probable n corrected words and their probabilities.
    '''  
    suggestions = []
    n_best = []
    suggestions = list((word in vocab and word) or edit_one_letter(word).intersection(vocab) or edit_two_letters(word).intersection(vocab))
    n_best = [[s,probs[s]] for s in list(reversed(suggestions))]  
    #if verbose: print("suggestions = ", suggestions)
    return n_best, suggestions

def auto_correct(input_word):
    if input_word in vocab:
        return "This word correctly spelled"
    else:
        correction = get_corrections(input_word, probs, vocab, 2, verbose=True)
        for i, word_prob in enumerate(correction):
            print(f"word {i}: {word_prob[0]}, probability {word_prob[1]:.6f}")
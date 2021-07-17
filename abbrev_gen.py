#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 09:47:02 2021

@author: dayman
"""
import numpy as np
import re
import json
import os
from tqdm import tqdm
import operator

# TODO, make get_sims order similarities by importance
# TODO, order this mess of a code...please


def load_docs(path, no_docs: int, strip=True, lower=True, verbose=False) -> list:
    """
    Loads .json file as dictionary
    If strip, will remove all characters not in the danish alphabet
    If lower, returns all characters as lowercase
    """
    
    with open(path, "r") as outfile:
        articles = json.load(outfile)
    
    docs = [i['content'] for i in articles]
    
    if verbose: print('Stripping Documents')
    
    if lower: docs = [i.lower() for i in docs]
    if strip: docs = [re.sub('[^a-zåøæ ]+', '', i) for i in docs]
    
    docs = docs[0:no_docs]
    
    return docs

def count_unique_words(docs: list, trim: int=0, verbose=False) -> dict:
    """
        Gets unique words based on a corpora of documents
        Trim specifies how many times a word must appear before it is registered

    """
    unique_counts = {}
    
    for doc in docs:
        for word in doc.split(' '):
            if word not in unique_counts:
                unique_counts[word] = 1
            else:
                unique_counts[word] += 1
                
    if trim > 0:
        keys_to_pop = [key for key in unique_counts.keys() if unique_counts[key] <= trim]
        print('Trimming', len(keys_to_pop), ' words')
        [unique_counts.pop(key) for key in keys_to_pop]
        
        unique_counts.pop('')
    return unique_counts


def create_bag_of_words(docs: list, vocabulary: list, verbose=False) -> np.ndarray:
    """
        Takes a number of documents and list of unique words
        Returns Bag-of-Words representation with each row corresponding to a 
        word and each columna a document. The i,j element of the matrix will
        then by the appearences of the i'th word in the j'th document.
    """
    
    # vocab_size, num_doc: i, j dimensions of numpy arrays
    vocab_size = len(vocabulary)
    num_doc = len(docs)
    bag_of_words = np.zeros((vocab_size, num_doc))

    # Used to get an index from a word
    word2idx = {word: idx for idx, word in enumerate(vocabulary)}
    
    # For each document    
    if verbose:
        print('Creating bag of words')
        for doc_idx, doc in enumerate(tqdm(docs)):
            for word in doc.split():
                
                # If vocab has been trimmed, necessary to check if words are in it
                if word in vocabulary:
                    bag_of_words[word2idx[word], doc_idx] += 1
    
    else:
        for doc_idx, doc in enumerate(docs):
            # And for each word, increment the number of that in our bag of words
            # Here the word2idx is our row, and idx doc is our column
            for word in doc.split():
                
                # If vocab has been trimmed, necessary to check if words are in it
                if word in vocabulary:
                    bag_of_words[word2idx[word], doc_idx] += 1
                
    return bag_of_words

def generate_embedding(docs, trim: int=0, verbose=False):
    unique = list(count_unique_words(docs, trim).keys())
    BoW = create_bag_of_words(docs, unique, verbose=verbose)
    P_word, P_doc = get_LSA(BoW)
    
    return P_word, P_doc, unique, BoW
    

def get_random_words(length, vocabulary: list) -> str:
    """
        Gets a random series of #length# words that are bound to be in the 
        vocabulary for. For testing purposes.
    """
    rands =np.random.randint(len(vocabulary), size = length)
    rand_word = ' '.join([vocabulary[rand] for rand in rands])
    return rand_word


def get_LSA(BoW: np.ndarray,sing_vals=0, save=False) -> np.ndarray:
    """
    Takes a bag-of-words representation of a corpora and returns two matrices
    For projecting words unto a document space and a documents unto a word space
    respectively
    

    """
    
    U, sv, V = np.linalg.svd(BoW, full_matrices=False)
    P_word = V@np.diag(1./np.sqrt(sv))
    P_doc = np.diag(1./np.sqrt(sv))@U.T
    
    if sing_vals == 0:
        sing_vals = len(sv)
    
    if save:
        path = os.getcwd()
        np.save(path + '/word_projection', P_word)
        np.save(path + '/document_projection', P_doc)
        
    return P_word[:, 0:sing_vals], P_doc[:,0:sing_vals]


def recursive_combo(current_combo_words: list, to_append: dict, max_length, curr_index=0, n=10):
    # TODO: Update this stupid descriptions, use less 'words'
    """
    Generates all possible combinations of words based on word list with given
    positions of words.
    
    Max_length should be the final amount of words in the string
    produces max_length^n combinations
    
    Returns a list with combinations and expected fit for original relation.

    """ 
    
    new_list = []
    keys = list(to_append.keys())
    
    # Generate first list of 10 words
    if current_combo_words == None:
        # Expect to get word_length^n combinations, don't set n too high
        current_combo_words = [[word, score] for word, score in to_append[keys[curr_index]][0:n]]
        curr_index += 1

    # For each combination currently in the string...
    for i, combos in enumerate(current_combo_words):
        curr = current_combo_words.pop(i)
        # Add every possible word next in line.
        for r, combo in enumerate(to_append[keys[curr_index]][0:n]):
            new_string = curr[0] + ' ' + combo[0]
            new_score = curr[1] + combo[1]
            new_list.append([new_string, new_score])
            
    if (curr_index+1) != max_length:
        return recursive_combo(new_list, to_append, max_length, curr_index + 1)
    
    else:
        print('There are ', len(new_list), 'Combinations')
        return new_list
    
    
def get_sims(abbrev: str, relation : str, vocabulary: list, projected_words: np.ndarray, v=''):
    """
    Gets similar words based on a relation word and desired abbreviation
    """
    

    
    relation = relation.split(" ")
    abbrev = list(abbrev)
    
    print('abbrev is',abbrev)
    
    # Check if all words in relation are in BoW...
    wrong_words = []
    for word in relation:
        if word not in vocabulary:
            wrong_words.append(word)
        
    if len(wrong_words) > 0:
        print('Error, words', wrong_words, ' are not in the vocabulary')
        return
    
    cos_sim = lambda x, y:  np.dot(x.T, y)/np.sqrt(np.dot(x.T, x)*np.dot(y.T,y))
    word_sims = {word: [] for word in relation}

    for i, word in enumerate(relation):
        
        sim_vals = []
        words = []
        
        # Get the index of the word in our representations
        word_idx = vocabulary.index(word)

        # And get vector representation
        curr_vec = projected_words[word_idx]
        # Compare to every other word in our vocabulary
        for r, similar in enumerate(vocabulary):
            if len(similar) == 0:
                continue
            
            # Only take the ones whose first letter spell abbrev.
            if similar[0] == abbrev[i]:
                cossim = cos_sim(curr_vec, projected_words[r])
                
                sim_vals.append(cossim)
                words.append(similar)
        
        # Each word is sorted small-large by similarity values
        word_sims[word] =  [[word, sim] for sim, word in sorted(zip(sim_vals, words), reverse=True)]
        
        #word_sims[word] = [x for _,x in sorted(zip(sim_vals, words))]
    
    all_combinations = recursive_combo(None, word_sims, len(relation))
    
    # Calculate abbrev-relation-score
    for i, combo in enumerate(all_combinations):
        all_combinations[i][1] = all_combinations[i][1]/len(relation)
    
    
    # Calculate abbrev-abbrev-score
    # Score based on how well each word relates to the next word
    for i, combo in enumerate(all_combinations):
        a_a_score = 0
        words_in_combo = combo[0].split(' ')
        for r, word in enumerate(words_in_combo[0:-1]):
            word_idx = vocabulary.index(word)
            curr_vec = projected_words[word_idx]
            
            word_idx2 = vocabulary.index(words_in_combo[r + 1])
            curr_vec2 = projected_words[word_idx2]
            
            a_a_score += cos_sim(curr_vec, curr_vec2)
            
        a_a_score = a_a_score/(len(relation)-1)
        
        all_combinations[i].append(a_a_score)
    
    # Calculate final score as average of abbrev-abbrev and abbrev-relation
    final_score = [[word, (a_a+a_r)/2] for word, a_a, a_r in all_combinations]
    
    # Get sorted list of final scores
    simscores = [[word, score] for word, score in sorted(final_score,key=operator.itemgetter(1), reverse = True)]
    
    # Print top 10 
    for sim_words in simscores[0:10]:
        print(sim_words)
   
    return simscores
    #return word_sims, all_combinations    
    
def generate_abbrev(relation, similarities):
    """
    Generates abbreviations based on known similarities

    """
    
    relation = relation.split(' ')
    
    i = 0
    
    while True:
        current_abbrev = ''
        for word in relation:
            current_abbrev += similarities[word][i] + ' '
        
        print(current_abbrev)
        
        inp = input('Good enough? y\n')
        
        if inp == 'n':
            i += 1
            pass
        
        if inp == 'y':
            break

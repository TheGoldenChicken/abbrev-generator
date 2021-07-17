#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 10:42:29 2021

@author: dayman
"""


#TODO
# Fix the program fucking up abbreviations for relations with duplicate words
# Docs is none vs docs =  None
    # Check why is important

# Place all of main in a new function
# Consider making regular argparse version... (With normal argument parsing)
#

from abbrev_gen import load_docs, create_bag_of_words, count_unique_words, get_LSA, generate_embedding, get_sims
from abbrev_gen import generate_abbrev
import argparse
import numpy as np

def list_options():
    print('1: Load new dataset')
    print('2: Generate embedding based on loaded dataset')
    print('3: Generate abbreviation based on embedding')
    
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description = 'Getting that sweet PENIS')



parser.add_argument('-l', '--list', help='Lists all options of LSA',
                    action='store_true', default=False)
parser.add_argument('-s', '--simple', type=str2bool, nargs='?',
                        const=True, default=True,
                        help="Activate simple mode.")
parser.add_argument('-v', '--verbosity', type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Increase output verbosity.")

parser.add_argument('-ld', '--load_dataset', type=str, 
                    help='Loads a new dataset')
parser.add_argument('-ge','--generate_embedding', type=int, 
                    help = 'Generate an LSA embedding based on loaded dataset')
parser.add_argument('-cr', '--create_relation', nargs =2 + 5,
                    help = 'Generate abbreviations based on desired abbreviation and relation') # TODO the amount of arguments expected dynamic with the relation string

parser.add_argument('--test', action='store_true', help='simple testing function')

args = parser.parse_args()


def main():
    no_docs = no_embedding = False
    P_word = P_doc = vocab = BoW = docs = None    
    print('Welcome to abbrev_gen V0.6')
    print("""
          -----------------------
          -----------------------
          -----------------------
          --Ascii Art goes here--
          -----------------------
          -----------------------
          -----------------------""")

    
    while True:
        astr = input('$: ')
        
        try:
            args = parser.parse_args(astr.split()) # Parse args in while true because it is better
        except:
            print('Error when parsing argument,', astr.split()[0])
            continue
        
        
        if args.list:
            list_options()
            args.list = False
        
        if args.load_dataset is not None:
            docs = load_docs(args.load_dataset)
            args.load_dataset = False
        
        if args.generate_embedding is not None:
            if docs == None:
                print('No dataset loaded, loading default')
                docs = load_docs('articles.json', 500)
            
            P_word, P_doc, vocab, BoW = generate_embedding(docs)
            args.generate_embedding = None
            
        if args.create_relation is not None:
            
            if args.simple and docs == None:
                print('Loading default document set...')
                docs = load_docs('articles.json', 500, verbose=args.verbosity)
            
            if args.simple and None in (P_word, P_doc, vocab, BoW):
                print('Generating default embedding...')
                P_word, P_doc, vocab, BoW = generate_embedding(docs, verbose=args.verbosity)

            sing_vals = int(args.create_relation[0])
            abbrev = args.create_relation[1]
            relation = ' '.join(args.create_relation[2:]) # Probably stupid to join them here, but abbrev_gen accepts relations as strings, not list
            print(relation)
            
            if len(list(abbrev)) != len(relation): # TODO, make it break out of if statment here to preserve program
                print("Your relation must contain as many words as your abbreviation!")
            
            if sing_vals == 0:
                print(P_word.shape)
                sing_vals = P_word.shape[1]
            
                
            sims = get_sims(abbrev, relation, vocab, BoW@P_word[:, 0:sing_vals])
            generate_abbrev(relation, sims)
            
            args.create_relation = None

        if args.test:
            args.test = False
            
            sing_vals = 0
            abbrev = 'penis'
            relation = 'der så en som er'

            if args.simple and docs == None:
                print('Loading default document set...')
                docs = load_docs('articles.json', 500, verbose=args.verbosity)
            
            if args.simple and None in (P_word, P_doc, vocab, BoW):
                print('Generating default embedding...')
                P_word, P_doc, vocab, BoW = generate_embedding(docs, verbose=args.verbosity)

            if sing_vals == 0:
                print(P_word.shape)
                sing_vals = P_word.shape[1]
            
            sims = get_sims(abbrev, relation, vocab, BoW@P_word[:, 0:sing_vals])
            
            k = 10
            s = 0
            print(sims[s:k], '\n')

            while True:

                inp = input('For more abbreviations, press y, to end, press n')
                
                if 'n' in inp.lower():
                    break
                elif 'y' in inp.lower():
                    k += 10
                    s += 10
                    print(sims[s:k], '\n')
                else:
                    print('Please choose a valid option')
            
                
            #sims, axe = get_sims(abbrev, relation, vocab, BoW@P_word[:, 0:sing_vals])
            #generate_abbrev(relation, sims)

            
# =============================================================================
#             if docs == None: # TODO, make it break out of if statment here to preserve program
#                 print('Sorry, there are no documents loaded, load a document please')
#                 print('Otherwise, turn simple mode on')
#                 no_docs = True
#                 #args.create_relation = None
#             
#             if None in (P_word, P_doc, vocab, BoW): # TODO, make it break out of if statment here to preserve program
#                 print('Sorry, you have an invalid embedding, please generate a valid embedding to continue')
#                 print('Otherwise, turn simple mode on')
#                 no_embedding = True
#                 #args.create_relation = None
# =============================================================================
      
        

# =============================================================================
# def main():
#     docs = None    
#     print('Welcome to abbrev_gen V0.6')
#     print("""
#           -----------------------
#           -----------------------
#           -----------------------
#           --Ascii Art goes here--
#           -----------------------
#           -----------------------
#           -----------------------""")
# 
#     P_word = None
#     while True:
#         list_options()
#         
#         inp = input('...') 
#         
#         if inp == '1':
#             print('enter path of dataset to load \n')
#             path = input()
#             
#             
#             print('Enter number of documents of the dataset you want to use, leave blank for all')
#             no_docs = input()
#             
#             # Add options for stripping and trimming...
#             
#             docs = load_docs(path, no_docs)
#         
#         elif inp == '2':
#             # TODO, make dataset load automatically
#             if docs == None:
#                 print('Error: No dataset loaded, loading default')
#                 docs = load_docs('articles.json', 500)
#             
#             P_word, P_doc, vocab, BoW = generate_embedding(docs, 0)
#             
#         elif inp == '3':
#             
#             if P_word == None:
#                 print('error, please generate a valid embedding first')
#                 return
#             relation = input(' Please enter relation string of words seperated by whitespace \n')
#             abbrev = input(f"Enter desired abbreviation, it should be {len(relation.split(' '))} letters long \n")
#             
#             sims = get_sims(abbrev, relation, vocab, BoW@P_word)
#             
#             for i, word in enumerate(list(abbrev)):
#                 print(sims[relation.split(' ')[i]][:10])
#                 
#             if sims == None:
#                 print('It appears there was a mistake, please try again')
#                 continue
#                 
#             generate_abbrev(relation, sims)
#             
# =============================================================================
#parser.add_argument('-s', '--simple', help='Turns simple mode on', 
#                    action='store_bool', const=False)
           
            
# =============================================================================
#     print("""
#           -----------------------
#           -----------------------
#           -------------( )-------
#           -----------(    )------
#           ----------(      )-----
#           ---------(__    __)-----
#           -----------(    )------
#           -----------(    )------
#           -----------(    )------
#           --------#--(    )--#----
#           ------#--#______#-#-----
#           --------#---------#----""")
# =============================================================================
            
main()
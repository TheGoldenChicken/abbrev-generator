# abbrev-generator
Uses LSA to create abbreviations based on similar words and desired abbreviation


This program uses articles collected from bt.dk to generate word embeddings using latent semantic analysis. This is then used to generate words in a desired abbreviation, based on a collection of words that roughly decide what the abbreviation should mean.

For example, the abbreviation 'PENIS' is desired to roughly describe "Party planners for first years'". The program then finds words similar in meaning to each word of the description, while matching in first letter of the abbreviation. It ranks these based on how much they relate to each word in the description. Finally, it reccomends a series of words to describe the abbreviation.

The data is made for Danish, but can be freely changed to another dataset based on another language


USE abbrev-gen.py and main.py with articles.json, THE OTHER FILES ARE LEGACY SINCE OWNER IS AN IDIOT AT GITHUB

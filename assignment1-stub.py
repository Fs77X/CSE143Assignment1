#!/usr/bin/env python

import nltk, zipfile, argparse
import numpy
from nltk.tokenize import sent_tokenize, word_tokenize
###############################################################################
## Utility Functions ##########################################################
###############################################################################
# This method takes the path to a zip archive.
# It first creates a ZipFile object.
# Using a list comprehension it creates a list where each element contains
# the raw text of the fable file.
# We iterate over each named file in the archive:
#     for fn in zip_archive.namelist()
# For each file that ends with '.txt' we open the file in read only
# mode:
#     zip_archive.open(fn, 'rU')
# Finally, we read the raw contents of the file:
#     zip_archive.open(fn, 'rU').read()
def unzip_corpus(input_file):
    zip_archive = zipfile.ZipFile(input_file)
    contents = [zip_archive.open(fn, 'r').read().decode('utf-8') for fn in zip_archive.namelist() if fn.endswith(".txt")
                and not fn.startswith('__MACOSX')]
    return contents

###############################################################################
## Stub Functions #############################################################
###############################################################################
def process_corpus(corpus_name):
    input_file = corpus_name + ".zip"
    corpus_contents = unzip_corpus(input_file)

    # Your code goes here
    print("1. Corpus Name: " + corpus_name)
    sentenceStory = []
    wordStory = []
    for i in range(len(corpus_contents)):
        sentenceStory.append(sent_tokenize(corpus_contents[i]))

    # print(sentenceStory)

    for i in range(len(sentenceStory)):
        for j in range(len(sentenceStory[i])):
            wordStory.append(word_tokenize(sentenceStory[i][j]))

    counter = 0
    for i in range(len(wordStory)):
        for j in range(len(wordStory[i])):
            counter = counter + 1

    print("2: Total words: " + str(counter))
    corpusTags = []
    # print(wordStory)
    for i in range(len(wordStory)):
        corpusTags.append(nltk.pos_tag(wordStory[i]))

    # print(corpusTags)
    wordStory1 = []
    
    for i in range(len(wordStory)):
        for j in range(len(wordStory[i])):
            wordStory1.append(wordStory[i][j])

    uniqueWord = set(wordStory1)
    print("3: length:" + str(len(uniqueWord)))

    corpus1 = []
    uniqueWord = list(uniqueWord)
    # print(uniqueWord)
    # for i in uniqueWord:
    corpus1 = nltk.pos_tag(uniqueWord)

    # print(len(corpus1))
    corpus2 = []
    
    for i in range(len(corpus1)):
        corpus2.append(corpus1[i][1])

    # print(len(corpus2))
    corpus3 = set(corpus2)
    dict0 = {}
    for i in corpus3:
        dict0[i] = corpus2.count(i)

    print(dict0)



    pass

###############################################################################
## Program Entry Point ########################################################
###############################################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Assignment 1')
    parser.add_argument('--corpus', required=True, dest="corpus", metavar='NAME',  help='Which corpus to process {fables, blogs}')

    args = parser.parse_args()
    
    corpus_name = args.corpus
    
    if corpus_name == "fables" or "blogs":
        process_corpus(corpus_name)
    else:
        print("Unknown corpus name: {0}".format(corpus_name))
        
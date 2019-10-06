#!/usr/bin/env python
import contextlib
import nltk, zipfile, argparse
import numpy
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import ConditionalFreqDist, FreqDist
import operator
from contextlib import redirect_stdout
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

    sentenceTag = []
  

    # for i in range(len(sentenceStory)):
    #     sentenceTag.append(nltk.pos_tag(word_tokenize(sentenceStory[i])))

    # print(sentenceTag)

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
    
    #for sentence, if sentence is 0, then yeet else print newline, then print shit
    fileOut = open(corpus_name +'-pos.txt', 'w') 
    for i in range(len(corpusTags)):
        if i != 0:
            fileOut.write('\n')
        for word in corpusTags[i]:
            fileOut.write(word[0] + '/' + word[1] + ' ')

    fileOut.close()


    # print(corpusTags)
    wordStory1 = []
    
    for i in range(len(wordStory)):
        for j in range(len(wordStory[i])):
            wordStory1.append(wordStory[i][j])

    uniqueWord = set(wordStory1)
    corpus1 = nltk.pos_tag(wordStory1)
    corpus1 = list(set(corpus1))

    # print(corpus1)
   
   
    print("3: length:" + str(len(uniqueWord)))

    # uniqueWord = list(uniqueWord)
    # print(uniqueWord)
    # for i in uniqueWord:
    

    # print(len(corpus1))
    corpus2 = []
    for i in range(len(corpus1)):
        corpus2.append(corpus1[i][1])

   
    corpus3 = set(corpus2)
  
    dict0 = {}
    for i in corpus3:
        dict0[i] = corpus2.count(i)

    sorted_d = list(sorted(dict0.items(), key=operator.itemgetter(1)))
    sorted_d.reverse()
  
    for i in range(0, 10):
        print(sorted_d[i])

    
  

    fDist = FreqDist()
    # print(wordStory1)
    
    for word in wordStory1:
        fDist[word.lower()] += 1

    # print(fDist)
    dict4fDist = {}
    for word in fDist:
        dict4fDist[word] = fDist.freq(word)

        # print ("Frequency of", word, fDist.freq(word))

    # print(dict4fDist)
    sorted_d2 = list(sorted(dict4fDist.items(), key=operator.itemgetter(1)))
    sorted_d2.reverse()

    fileOut = open(corpus_name +'-word-freq.txt', 'w') 
    for word in sorted_d2:
        fileOut.write('The word ' + word[0] + ' has frequency of ' + str(word[1]) + '\n')


    fileOut.close()
    # for i in range(0, 10):
    #     print(sorted_d2[i])
  
    
   
    corpustag2 = []
    for i in range(len(corpusTags)):
        for j in range(len(corpusTags[i])):
            corpustag2.append((corpusTags[i][j][0], corpusTags[i][j][1]))
            # condition = corpusTags[i][j][1]
    
            # word = corpusTags[i][j][0]
            
            # cfdist[condition][word.lower()] += 1
    
    cfdist = ConditionalFreqDist(corpustag2)

        
 
    fileOut = open(corpus_name +'-pos-word-freq.txt', 'w') 
    with redirect_stdout(fileOut):
        cfdist.tabulate()
    fileOut.close()

    dict4NN = {}
    dict4VBD = {}
    dict4JJ = {}
    dict4RB = {}

    text = nltk.Text(wordStory1)
    for word in cfdist:
        dict4NN[word] = cfdist[word]['NN']
        dict4VBD[word] = cfdist[word]['VBD']
        dict4JJ[word] = cfdist[word]['JJ']
        dict4RB[word] = cfdist[word]['RB']

    sorted_dNN = list(sorted(dict4NN.items(), key=operator.itemgetter(1)))
    sorted_dNN.reverse()
    sorted_dVBD = list(sorted(dict4VBD.items(), key=operator.itemgetter(1)))
    sorted_dVBD.reverse()
    sorted_dJJ = list(sorted(dict4JJ.items(), key=operator.itemgetter(1)))
    sorted_dJJ.reverse()
    sorted_dRB = list(sorted(dict4RB.items(), key=operator.itemgetter(1)))
    sorted_dRB.reverse()
    print(sorted_dNN[0])
    print(text.similar(sorted_dNN[0][0]))
    print(sorted_dVBD[0])
    print(text.similar(sorted_dVBD[0][0]))
    print(sorted_dJJ[0])
    print(text.similar(sorted_dJJ[0][0]))
    print(sorted_dRB[0])
    print(text.similar(sorted_dRB[0][0]))

    print(type(wordStory1))
    print(len(wordStory1))
    
    print(type(text))
    print('; '.join(text.collocation_list()))

        
  
#give list of numbers, list.max

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
        
#!/usr/bin/env python
import contextlib
import nltk, zipfile, argparse
from decimal import Decimal
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

    stories = []
    for i in corpus_contents:
        stories.append([i])

    # print(stories)
    senstor = []
    for i in range(len(stories)):
        senstor.append([])
        # print(sent_tokenize(stories[i][0]))
        for sentence in sent_tokenize(stories[i][0]):

            senstor[i].append(sentence) 

    # print(senstor)

    wordstor = []
    for i in range(len(senstor)):
        wordstor.append([])
        for j in range(len(senstor[i])):
            wordstor[i].append([])
            for word in word_tokenize(senstor[i][j]):
                wordstor[i][j].append(word)
            

    # print(wordstor)

    corpstor = []
    for i in range(len(wordstor)):
        corpstor.append([])
        for j in range(len(wordstor[i])):
            corpstor[i].append(nltk.pos_tag(wordstor[i][j]))
            # for word in wordstor[i][j]:
            #     corpstor[i][j].append(nltk.pos_tag(word))


    # print(corpstor)


        

    for i in range(len(sentenceStory)):
        for j in range(len(sentenceStory[i])):
            wordStory.append(word_tokenize(sentenceStory[i][j]))

    # print(wordStory)

    counter = 0
    for i in range(len(wordStory)):
        for j in range(len(wordStory[i])):
            counter = counter + 1

    print("2. Total words in the corpus: " + str(counter))
    corpusTags = []
    # print(wordStory)
    for i in range(len(wordStory)):
        corpusTags.append(nltk.pos_tag(wordStory[i]))


    fileOut = open(corpus_name +'-pos.txt', 'w') 
    for i in range(len(corpstor)):
        for sentence in corpstor[i]:
            for word in sentence:
                fileOut.write(word[0] + '/' + word[1] + ' ')
            fileOut.write('\n')
            
        fileOut.write('\n\n')

    fileOut.close()


    wordStory1 = []
    
    for i in range(len(wordStory)):
        for j in range(len(wordStory[i])):
            wordStory1.append(wordStory[i][j])

    uniqueWord = set(wordStory1)
    corpus1 = nltk.pos_tag(wordStory1)
    corpus1 = list(set(corpus1))


   
    print("3. Vocabulary size of the corpus:" + str(len(uniqueWord)))

 
    corpus2 = []
    for i in range(len(corpus1)):
        corpus2.append(corpus1[i][1])

    corpus3 = set(corpus2)
  
    dict0 = {}
    for i in corpus3:
        dict0[i] = corpus2.count(i)

    sorted_d = list(sorted(dict0.items(), key=operator.itemgetter(1)))
    sorted_d.reverse()
    
    print('4. The most frequent part-of-speech tag is ' + sorted_d[0][0] + ' with frequeency of ' + str(sorted_d[0][1]))
    print('5.  Frequencies  and  relative  frequencies  of  all  part-of-speech  tags  in  the  corpus  in  decreasing  order  of frequency are: ')
    for i in range(0, 10):
        print(sorted_d[i][0] +  ' has frequency ' + str(sorted_d[i][1]) + ' and relative frequency of ' + str( "{:.2E}".format(Decimal(sorted_d[i][1]/counter))))

    
    fDist = FreqDist()
 
    
    for word in wordStory1:
        fDist[word.lower()] += 1

    dict4fDist = {}
    for word in fDist:
        dict4fDist[word] = fDist[word]


    sorted_d2 = list(sorted(dict4fDist.items(), key=operator.itemgetter(1)))
    sorted_d2.reverse()

    fileOut = open(corpus_name +'-word-freq.txt', 'w') 
    for word in sorted_d2:
        fileOut.write('The token ' + word[0] + ' has frequency of ' + str(word[1]) + '\n')

    fileOut.close()

    corpustag2 = []
    for i in range(len(corpusTags)):
        for j in range(len(corpusTags[i])):
            corpustag2.append((corpusTags[i][j][0], corpusTags[i][j][1]))
    
    
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

    print('6.  The most frequent word in the POS:')

    sorted_dNN = list(sorted(dict4NN.items(), key=operator.itemgetter(1)))
    sorted_dNN.reverse()
    sorted_dVBD = list(sorted(dict4VBD.items(), key=operator.itemgetter(1)))
    sorted_dVBD.reverse()
    sorted_dJJ = list(sorted(dict4JJ.items(), key=operator.itemgetter(1)))
    sorted_dJJ.reverse()
    sorted_dRB = list(sorted(dict4RB.items(), key=operator.itemgetter(1)))
    sorted_dRB.reverse()
    print('The most frequent word in the POS NN is : ' + str(sorted_dNN[0][0]) + ' and its similar word are:', end=" ") 
    print(str(text.similar(sorted_dNN[0][0]))) 
    print('The most frequent word in the POS VBD is : ' + str(sorted_dVBD[0][0]) + ' and its similar word are:', end=" ")
    print(str(text.similar(sorted_dVBD[0][0])))
    print('The most frequent word in the POS JJ is : ' +  str(sorted_dJJ[0][0]) + ' and its similar word are:' , end=" ") 
    print(str(text.similar(sorted_dJJ[0][0])))
    print('The most frequent word in the POS RB is : ' +  str(sorted_dRB[0][0]) + ' and its similar word are:' , end=" ")
    print(str(text.similar(sorted_dRB[0][0])))

    print('7.  Collocations: ' + '; '.join(text.collocation_list()))


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
        
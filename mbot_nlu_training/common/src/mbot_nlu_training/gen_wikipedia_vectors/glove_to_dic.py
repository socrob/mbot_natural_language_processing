#!/usr/bin/env python3

import msgpack
import msgpack_numpy
import sys
import numpy as np

# the pretrained model, recommended one (glove) can be found here: https://github.com/stanfordnlp/GloVe
# more specifically we got the wikipedia 2014 pre-trained word vectors:
#   wget http://nlp.stanford.edu/data/wordvecs/glove.6B.zip
# unzip and use the 300 vector size one (it has also other size vectors inside)

# fetch glove.6B.300d.txt path from args
if len(sys.argv) == 1:
    print('Usage: {} GLOVE_FILE'.format(sys.argv[0]))
    sys.exit(1)

glove_vectors = sys.argv[1] + '/glove.6B.300d.txt'

# iterate over the list and create big_dictionary with word and index
i = 0
# intialize empty big_dictionary
big_dictionary = {}

# read file one time to get number of lines
number_of_loops = sum(1 for line in open(glove_vectors))

big_wordvectors = np.zeros( (number_of_loops, 300), dtype=float )

# open text file, read each line and store in list
f = open(glove_vectors)
for token in f:
    # [1:] trashes away the first element and keeps the rest
    token_vector_as_string_list = token.split()
    # convert token_vector_as_string_list into a list of floats
    big_wordvectors[i,:] = list(map(float, token_vector_as_string_list[1:]))
    #big_wordvectors.append(token_vector)
    # the following line creates the big_dictionary, similar to -> big_dictionary.append(token_vector_as_string_list[0] : i)
    big_dictionary[token_vector_as_string_list[0]] = i
    # increment count for the next word
    i = i + 1
    print('\r%d/%d completed (%s %% done)' % (i, number_of_loops, str(int(float(i) / float(number_of_loops) * 100.0))), end='\r')
    # print str(i) + "/" + str(number_of_loops) + " completed, (" +  str(int(float(i) / float(number_of_loops) * 100.0)) + "% done)"
f.close()

print()
print('Dumping big_dictionary and big_wordvectors files, will take a while...')

# dump big_dictionary to a serialized file
with open(sys.argv[1] + '/big_dictionary', 'wb') as big_dictionary_handle:
    msgpack.dump(big_dictionary, big_dictionary_handle) # not numpy

# dump big_wordvectors to a serialized file
with open(sys.argv[1] + '/big_wordvectors', 'wb') as vector_handle:
    msgpack_numpy.dump(big_wordvectors, vector_handle)

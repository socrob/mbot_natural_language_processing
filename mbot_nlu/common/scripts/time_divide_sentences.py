#!/usr/bin/env python

from timeit import default_timer as timer
from mbot_nlu.phrases import divide_sentence_in_phrases as divide
from sys import argv

sentences = [
    'find Oscar at the office and tell the time to him',
    'find mithun and help him',
    'robot, go home and charge your batteries',
    'hello robot, go home and charge your batteries', # failing right now
    'go to the kitchen',
    'go to the kitchen and find a person',
    'go to the kitchen, find a person and follow them',
    'go to the kitchen, find a person, introduce yourself and follow them',
    'find carlos in the living room and bring him a knife'
]

if __name__ == "__main__":

    start = timer()

    if len(argv) > 1:
	print('With DEBUG')
	opt_debug = True
    else: opt_debug=False

    for sentence in sentences:
        per_start = timer()
        divided = divide(sentence, debug=opt_debug)
        per_end = timer()
        print('({:.2f}s) {} ----> {}'.format(per_end - per_start, sentence, divided))

    end = timer()
    ellapsed = end-start
    ellapsed_per_sentence = ellapsed/len(sentences)

    print('\nTook a total of {:.2f} seconds, {:.2f} seconds per sentence'.format(ellapsed, ellapsed_per_sentence))

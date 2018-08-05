#!/usr/bin/env python

import subprocess
import os
import sys

from mbot_world_model_ros.gpsr_dict import slots_dict
# from https://stackoverflow.com/a/2659877
inv_slots_map = dict(
    (v, [k for (k, xx) in filter(lambda (key, value): value == v, slots_dict.items())]) 
    for v in set(slots_dict.values())
)
person_names = inv_slots_map['p']
person_names_upper = [p[0].upper() + p[1:] for p in person_names]

def divide_sentence_in_phrases(sentence, debug=False):

    spl = sentence.split()
    # upper case first letter if person name
    for idx, word in enumerate(spl):
	if word in person_names:
	    spl[idx] = word[0].upper() + word[1:]

    # remove multiple and trailing whitespaces
    sentences = ' '.join(spl)


    # call syntaxnet parsing process
    process = subprocess.Popen(
        'MODEL_DIRECTORY=$HOME/Software/models/English; '
        'cd $HOME/Software/models/syntaxnet; '
        'echo \'%s\' | syntaxnet/models/parsey_universal/parse.sh '
        '$MODEL_DIRECTORY 2' % sentences,
        shell=True,
        universal_newlines=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    # wait for process to finish and read output
    output = process.communicate() # returns tuple (stdout, stderr)
    if output[0] == '':
        print('Error on calling syntaxnet process: {}'.format(output[1]))
        return None

    processed_sentences = []
    sentence = []

    for line in output[0].split("\n"):
        if len(line) == 0:
            processed_sentences.append(sentence)
            sentence = []
        else:
            word = line.split("\t")
            sentence.append(word)

    if debug: print('Before post-processing: {}'.format(processed_sentences))

    words = []
    deps = []
    for sentence in processed_sentences:
        s = ''
        for line in sentence:
            words.append(line)
            s += "\t".join(line) + '\n'
        deps.append(s)


    phrases = [[] for _ in range(len(words))]
    numbers = [[] for _ in range(len(words))]
    missing = [[] for _ in range(2 * len(words))]
    missingaux = [[] for _ in range(2 * len(words))]

    # below older stuff that we think is not needed, syntaxnet will catch it
    '''
    extra_verbs = ['guide', 'find', 'look', 'follow', 'accompany', 'take', 'deliver', 'grasp', 'tell', 'answer', 'search', 'meet', 'bring', 'carry',
    'come', 'drive', 'find', 'get', 'go', 'grab', 'hang', 'let', 'look', 'move', 'pick', 'place', 'put', 'reach', 'search', 'take', 'walk']
    '''

    # if syntaxnet fails for specific noun or verb, add here and it might help
    extra_verbs = ['charge', 'ask']
    extra_names = ['robot', 'mbot'] + person_names_upper

    i = 0
    m = 0
    c = 0
    v = 0
    verb = []
    w = 0
    conj = []
    dictionary = dict()
    for word in words:
        dictionary [word[0]] = word[1]

        if word[1] in extra_verbs:
            word[4] = 'VB'
            if word[3] == 'AUX':
                word[3] = 'VERB'
            if word[7] == 'xcomp':
                word[7] = 'verb'

        if word[1] in extra_names:
            word[3] = 'Noun'
            word[4] = 'NN'
            word[5] = 'Noun'


        if ('VB' in word[4] or 'Verb' in word[5]) and word[3] != 'AUX' and word[7] != 'xcomp' and v == 0:
            phrases[i].append(int(word[0]))
            for x in range(0, int(word[0])-1):
                phrases[i].append(int(words[x][0]))
            i += 1
            v += 1
            verb.append(word[0])

        elif ('VB' in word[4] or 'Verb' in word[5]) and word[3] != 'AUX' and word[7] != 'xcomp' and word[7] != 'amod' and words[int(word[0])-2][3] != 'PART' and words[int(word[0])-2][4] != 'WDT':
            for x in range(int(verb[-1])+1, int(word[0])):
                phrases[i-1].append(int(words[x-1][0]))
            phrases[i].append(int(word[0]))
            i += 1
            verb.append(word[0])

        elif (word[3] == 'CONJ' or word[3] == 'SCONJ' or 'CONJ' in word[5]) and (words[int(word[6])-1][3] == 'VERB' or words[w+1][3] == 'VERB'
                                                            or words[w+2][3] == 'VERB' or 'Verb' in words[w+1][5] or 'Verb' in words[w+2][5]):
            conj.append(word[0])

    # check if at least one verb was found - needed for sentence currently
    if len(verb) == 0:
        print('No verbs were found in this sentence - might need to add as an extra verb')
        return None

    try:
        for x in range(int(verb[-1]), len(words)):
            phrases[i-1].append(int(words[x][0]))


        for v in range(len(phrases)):
            for i in phrases[v]:
                if str(i) in conj:
                    phrases[v].remove(i)

        phrases_final = []
        for k in range(len(phrases)):
            if phrases[k]:
                phrases[k].sort()
                phrases_final.append(phrases[k])

        instruction = []

        # to store the phrases, which is what the sentence is divided into
        phrases = []

        for p in range(len(phrases_final)):
            sentence = ''
            v = 0
            for number in phrases_final[p]:
                if v != 0:
                    sentence += ' '
                v += 1
                sentence += dictionary[str(number)]

            instruction.append(sentence)
            phrases.append(instruction[p])
            #print(str(p+1) + ': ' + instruction[p] + ' .')
        return phrases
    except Exception, e:
        print('Exception when using syntaxnet: {}'.format(e))
	return None

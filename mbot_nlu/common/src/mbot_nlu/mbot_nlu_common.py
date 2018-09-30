#!/usr/bin/env python

'''
GPSR General Purpose Service Robot Natural Language Understanding api
'''

from __future__ import print_function

import tensorflow as tf
import numpy as np
import msgpack
import threading
import time
import os
import sys
import yaml
import inspect

# load list of available intents from configuration file, add to list if your training data has more intents.
available_intents = yaml.load(open(str(os.path.dirname(os.path.realpath(__file__))) + '/../../../../mbot_nlu_training/ros/config/config_mbot_nlu_training.yaml'))['test_params']['available_intents']


class NaturalLanguageUnderstanding(object):

    '''
    functions for natural language uderstanding
    input text, output intention (action) and slot (arguments)
    to be able to communicate with a robot in a natural way
    '''
    def __init__(self, classifier_path, wikipedia_vectors_path, debug=False):
        # classifier path
        self.base_path = classifier_path

        # whether to print verbose info
        self.debug = debug

        # to store the found intention and slots
        self.intention_found = None
        self.slot_found = None

        # if classifier is pedro_gpsr, according dictionary should be used
        dic_name = 'pedro_dictionary' if 'pedro_gpsr' in classifier_path else 'dictionary'
        # test file existance, wikipedia vectors is required
        if os.path.isfile(wikipedia_vectors_path + '/' + dic_name):
            print('Wikipedia dictionary file was found.. proceed')
        else:
            print('\033[91m' + '[ERROR] [mbot_nlu_common] Wikipedia dictionary file not found,' + '\033[0m')
            sys.exit()
        # load serialized object wikipedia dictionary
        with open(wikipedia_vectors_path + '/' + dic_name, 'rb') as dict_file:
            self.dictionary = msgpack.load(dict_file, raw=False)

        # check if user has requested verbose debug info
        if not self.debug:
            # Disable Tensorflow debugging information
            tf.logging.set_verbosity(tf.logging.ERROR)

        # print available intents if debug
        if debug: print('available intents = {}'.format(self.available_intents))


    def initialize_session(self):
        '''
        method to initialize session, graph and meta data from pretrained intent and slot classifiers
        '''

        # sanity check intent
        intent_initialization_var = ['self.intent_sess', 'self.x_intent', 'self.y_intent', 'self.sequence_length_intent']
        # if classifier exists or not
        classifier_check = True
        # check if the essential intent variables has been declared
        proceed_status = [True if var not in locals() else False for var in intent_initialization_var]

        # configuring gpu use and limiting memory
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True

        if proceed_status.count(True)==len(proceed_status):
            print('Initiating intent classifier session... ', end='')
            # defining intent graph (graph is wrt terminology in TF)
            intent_graph = tf.Graph()
            # initiating tf session with intent graph
            self.intent_sess = tf.Session(graph=intent_graph, config=config)
            # setting intent_graph as default
            with intent_graph.as_default():
                try:
                    # restoring pretrained graph
                    saver_intent = tf.train.import_meta_graph(self.base_path + '/intent/actions_mydata_3.ckpt.meta', clear_devices=True)
                    # restoring meta data (contains variable data such as weights and biases)
                    saver_intent.restore(self.intent_sess, self.base_path + '/intent/actions_mydata_3.ckpt')
                    # assigning input tensor variable (1/2)
                    self.x_intent = intent_graph.get_tensor_by_name("input_placeholder:0")
                    # assigning input tensor variable (2/2)
                    self.sequence_length_intent = intent_graph.get_tensor_by_name("inputs_length:0")
                    # assigning output tensor variable
                    self.y_intent = intent_graph.get_tensor_by_name("Gather:0")
                except IOError:
                    print('\n\nIntention classifier missing!, are you sure you have downloaded them using the classifier setup? (mbot_nlu_classifier/common/setup/download_classifiers.sh)\n\n')
            print('Done')
        else:
            print('All the tf variables for intent session has been already initiated, moving on to slots session...')
            pass

        # sanity check slots
        slot_initialization_var = ['self.slot_sess', 'self.x_slot', 'self.y_slot', 'self.sequence_length_slot']
        # check if the essential intent variables has been declared
        proceed_status = [True if var not in locals() else False for var in slot_initialization_var]

        if proceed_status.count(True)==len(proceed_status):
            print('Initiating slot classifier session... ', end='')
            # defining slot graph
            slot_graph = tf.Graph()
            # initiating tf session with slot graph
            self.slot_sess = tf.Session(graph=slot_graph, config=config)
            # setting slot_graph as default
            with slot_graph.as_default():
                try:
                    # restoring pretrained graph
                    saver_slot = tf.train.import_meta_graph(self.base_path + '/slots/slots_2.ckpt.meta', clear_devices=True)
                    # restoring meta data (contains variable data such as weights and biases)
                    saver_slot.restore(self.slot_sess, self.base_path + '/slots/slots_2.ckpt')
                    # assigning input tensor variable (1/2)
                    self.x_slot = slot_graph.get_tensor_by_name("input_placeholder:0")
                    # assigning input tensor variable (2/2)
                    self.sequence_length_slot = slot_graph.get_tensor_by_name("inputs_length:0")
                    # assigning output tensor variable
                    self.y_slot = slot_graph.get_tensor_by_name("Reshape:0")
                    print('Done')
                except IOError:
                    print('\n\nArguments/slots classifier missing!, are you sure you have downloaded them using the classifier setup?(mbot_nlu_classifier/common/setup/download_classifiers.sh)\n\n')
        else:
            print('All the tf variables for slot session has been already initiated, moving on to processing input...')

        return


    def close_session(self):
        '''
        method to close both tf sessions (which will release the tf variables from memory) once NLU is no longer needed.
        (use it wisely ;))
        '''
        # sanity check
        # closing intent and slot sessions
        if not self.intent_sess._closed: self.intent_sess.close()
        if not self.slot_sess._closed: self.slot_sess.close()
        print('\033[1;31mBoth tensorflow sessions (intent and slots) are now closed\033[0;37m')


    def find_intention(self, phrase_as_index_vector, vector_size=15):
        '''
        method that recognizes the intention of the given phrase (phrase_as_index_vector)
        using a trained Neural Network with tensor flow
        for now only commands are allowed, no "pure" knowledge is supported
        input:
            phrase_as_index_vector - a single command, e.g. "go to the kitchen"
                but in index vector form,
                e.g. phrase_as_index_vector = [[243, 5, 1, 4907, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
            vector_size - the size of the input vector to the NN (15)
            NOTE: muliple phrases are not allowed e.g. "go to the kitchen and grasp the coke"
            first step in the NLU pipeline is to divide a sentence into phrases (using syntaxnet)
            and this method receives the individual phrases
        output:
            intention - string with the recognized intention
        '''

        # calculating the output of intent classifier [a list of 'probabilities' corresponding to each intent]
        with self.intent_sess.as_default():
            y_pred = self.y_intent.eval(feed_dict={self.x_intent: phrase_as_index_vector, self.sequence_length_intent: vector_size})

        # print debug information if debug is set to true
        if self.debug:
            print('prediction from the intent classifier = {}'.format(y_pred)) # probabilites (kind of, not exactly probabilites) for each of the actions

        # finding probability of intent class with maximum probability
        b = np.max(y_pred, 1)

        # init intention to 'other'
        intention = 'other'

        if b > 6.5: # threshold for the classification to be consider succesful

            y_pred = np.argmax(y_pred, 1).tolist()

            if self.debug:
                print('probability corresponding to predicted intent = {}'.format(y_pred)) # probabilites (kind of, not exactly probabilites) for each of the actions

            try:
                intention = available_intents[y_pred[0]]
            except:
                print('Error: NN classified your vector, but to a unknown class.. check your code + your training!')
                print('predicted class : ' + str(y_pred[0]))

        if self.debug:
            print('predicted intention = {}'.format(intention))

        # return value (store in member variable)
        self.intention_found = intention


    def find_slots(self, word_index_vector, vector_size, phrase):
        '''
        to identify the slots of an intention
        '''

        # calculating the output of slot classifier
        with self.slot_sess.as_default():
            y_slot = self.y_slot.eval(feed_dict={self.x_slot: word_index_vector, self.sequence_length_slot: vector_size})

        # finding probability of slot class with maximum probability
        y_pred = np.argmax(y_slot, 1).tolist()

        slots = []
        for i in range(len(phrase)):
            pred = y_pred[i]

            # TODO define this somewhere else
            if pred == 0:
                s_type = 'object'
            elif pred == 2:
                s_type = 'source'
            elif pred == 4:
                s_type = 'destination'
            elif pred == 6:
                s_type = 'person'
            elif pred == 7:
                s_type = 'sentence'
            else:
                continue

            s_data = phrase[i]
            # look for same type but Inside, for instance, many Iobject after Bobject
            if s_type != 'person':
                corresponding_inside = pred+1 # hard assumption, the Inside correspondence must be right after the Begin in the slot y_slot definition

                for j in range(i+1, len(phrase)):
                    if y_pred[j] != corresponding_inside:
                        break
                    s_data += ' ' + phrase[j]

            slots.append( (s_type, s_data) ) # tuple

        if self.debug:
            for slot in slots:
                print('predicted slots = {}'.format(slot)) # slot or agument !!

        # return value (store in member variable)
        self.slot_found = slots


    def filter_phrase(self, phrase):
        '''
        1. convert phrase to lowercase
        2. remove odd characters from words, e.g. , ? .
        input : phrase - a string, e.g. 'go to the kitchen'
        '''
        # convert phrase into lowercase
        filtered_phrase = phrase.lower()
        # remove unwanted characters from phrase
        filtered_phrase = filtered_phrase.strip('\n')
        # removing unwanted characters
        for symbol in ",.!?;":
           filtered_phrase = filtered_phrase.replace(symbol,'')

        return filtered_phrase

    def process_single_phrase(self, phrase, vector_size=15):
        # phrase filtering, remove odd chars from phrase
        filtered_phrase = self.filter_phrase(phrase)

        # convert string into list separating using ' ' (spaces)
        filtered_phrase = filtered_phrase.rsplit()

        # init empty list to be filled inside for loop
        word_index_vector = []

        # warn the user if more than 15 words are used (per filtered_phrase)
        max_phrase_length = 15
        if len(filtered_phrase) >= vector_size:
            print('\033[1;33mWARNING: phrase cant be longer than '+ str(max_phrase_length) +' words\033[0;37m')
            print('\033[1;33mWill only consider first ' + str(vector_size) + ' words\033[0;37m\n')

        # generate word_index_vector of length vector_size (15), contains the indexes obtained from wikipedia dictionary
        # for each of the words in the phrase + a bunch of zeros, as many required to reach vector_size (15) elements
        # e.g. word_index_vector = [[243, 5, 1, 4907, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        # the above example is for : "go to the kitchen"
        for i in range(0, vector_size):
            if i < len(filtered_phrase):
                # fill with wikipedia index
                try:
                    word_index_vector.append(self.dictionary[filtered_phrase[i]]) # filtered_phrase[i] is a word
                except:
                    print('\033[1;33mWARNING: word '+ filtered_phrase[i] + \
                      ' was not found on wikipedia most common words dataset, will be replaced with null word vector\033[0;37m')
                    try: word_index_vector.append(self.dictionary['zerowordvec'])
                    except: word_index_vector.append(0)
                    pass
            else:
                # fill with null wordvec index
                try: word_index_vector.append(self.dictionary['zerowordvec'])
                except: word_index_vector.append(0)

        # ensure that word_index_vector is of length vector_size (15)
        assert len(word_index_vector) == vector_size

        # start intention class method in separate threads
        intention_detector_thread = threading.Thread(target = self.find_intention, args= [[word_index_vector], [vector_size]])
        slot_detector_thread = threading.Thread(target = self.find_slots, args= [[word_index_vector], [vector_size], filtered_phrase])
        intention_detector_thread.start()
        slot_detector_thread.start()

        # wait until threads are finished
        while intention_detector_thread.isAlive() or slot_detector_thread.isAlive():
            time.sleep(0.001)

        # return results obtained from the threads
        return self.intention_found, self.slot_found


    def process_sentence(self, sentence, vector_size=15):
        '''
        1. process text to recogn
        Divide sentence into phrases
        2. convert to lowercase
        3. match word with wikipedia dictionary to get id (dictionary)
        4. ? TODO
        '''
        # to store return values, intention and slots e.g. recognized_intention = [['go','kitchen'],['grasp','bottle']]
        recognized_intention = []

        # iterate over the sentence to extract 1 intention per phrase
        for j, phrase in enumerate(sentence):
            if self.debug:
                # print the phrase which is currently being analyzed
                print("---")
                print(str(j) + ': ' + phrase)

            # process this phrase
            intention, slot = self.process_single_phrase(phrase, vector_size=15)

            # if intention is known then store to return values
            if intention != 'other':
                # for each filtered_phrase append the intention (action) and slot (args)
                recognized_intention.append([intention, slot])
            else:
                # inform the user that the detected intention is not known
                print('\033[1;33mWARNING : Detected intention not known!\033[0;37m')

            # NOTE: will continue looping over sentence and will process next phrase!

        return recognized_intention


if __name__ == '__main__':
    # example of how to use this class
    import rospkg
    import rospy
    rospack = rospkg.RosPack()
    classifier_path = rospack.get_path('mbot_nlu_classifiers') + \
        '/common/classifiers/' + rospy.get_param('~nlu_classifier', 'mithun_gpsr_robocup')
    wikipedia_vectors_path = rospack.get_path('mbot_nlu_training') + \
        '/common/resources/wikipedia_vectors'

    # instantiation
    nlu = NaturalLanguageUnderstanding(classifier_path=classifier_path, wikipedia_vectors_path=wikipedia_vectors_path)

    # initiating nlu session
    nlu.initialize_session()

    # examples
    print(nlu.process_sentence(['go to the kitchen']))
    print("----")
    print(nlu.process_sentence(['pick the bottle']))
    print("----")
    print(nlu.process_sentence(['go to the kitchen', 'pick the bottle']))
    print("----")
    print(nlu.process_sentence(['go to the kitchen', 'pick the bottle from the table']))

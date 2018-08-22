#!/usr/bin/env python3

import os
import sys
import time
import yaml
import unittest
import progressbar
from nlu_source.mbot_nlu_common import NaturalLanguageUnderstanding

class MbotNluTest(unittest.TestCase):

    def setUp(self):
        '''
        Sets up the test fixture before exercising it
        '''
        # load test parameters from yaml file
        yaml_dict = yaml.load(open('../../gpsr/nlu_training.yaml'))['test_params']
        classifier_path = yaml_dict['classifier_path']
        wikipedia_vectors_path = yaml_dict['base_path']
        available_intents = yaml_dict['available_intents']
        self.pwd = yaml_dict['pwd']
        self.test_choice = yaml_dict['test_choice']
        debug = yaml_dict['debug']
        # NLU class and instance
        self.nlu = NaturalLanguageUnderstanding(available_intents, classifier_path, wikipedia_vectors_path, self.test_choice, debug=debug)
        self.nlu.intitialize_session()
        print('nlu session is running')

    def tearDown(self):
        self.nlu.close_session()
        print('nlu session is closed')

    def read_sentences_from_textfile(self, filename):
        '''
        open sentences.txt file and read sentences inside
        '''
        sentences = []
        with open(self.pwd + filename) as fp:
            for line in fp:
                sentences.append(line)
        # rm sentences with #
        sentences = [item for item in sentences if '#' not in item]
        return sentences

    def read_expected_values_from_textfile(self, filename):
        '''
        get the expected intent and slots from text file
        '''
        available_slots = ['Person', 'Object', 'Source', 'Destination', 'Tell'] # 'what to tell' doesn't work, need updating
        expected_output = [] # [['go', 'to the kitchen'],['pick','coke is an object'], ... ]
        with open(self.pwd + filename) as fp:
            for line in fp:
                # if '#' in line, continue to next line
                if '#' in line: continue

                # strip end chars and split
                line = line.rstrip().split()

                #intent extraction and appending
                intent = line.pop(0) # intent is removed from line
                expected_output.append([intent])

                # extracting the slot index from the current line
                slot_idx_list = []
                for slot in available_slots:
                    try: slot_idx_list.append(line.index(slot))
                    except: continue

                # Sorting the slot indexes
                slot_idx_list = sorted(slot_idx_list, key=int)

                #slots extraction and appending to the current intent
                prev_slot_idx = 0
                for slot_idx in slot_idx_list:
                    # print('line = {}'.format(line))
                    # print('slot index = {}'.format(slot_idx))
                    # slots are extracted according to their indexes from previous search
                    slot = str(' '.join(line[prev_slot_idx:slot_idx+1]))
                    # appending to the last item in the list (which is the current intent)
                    expected_output[-1].append(slot.lower())
                    # print('slot = {}'.format(slot))
                    prev_slot_idx = slot_idx+1

        return expected_output

    def test_mbot_nlu(self):
        '''
        the test function
        Publish a sentence and compare to an expected return value from the node
        '''

        # read nlu input and expected output from textfiles
        sentences = self.read_sentences_from_textfile('nlu_test_inputs.txt')
        expected_output = self.read_expected_values_from_textfile('nlu_expected_output.txt')
        # print(expected_output)

        bar = progressbar.ProgressBar(max_value=len(sentences), redirect_stdout=True)

        test_total_number = 0

        for i, sentence in enumerate(sentences):

            # print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

            # Check if NLU has an output in not continue to the next sentence
            self.result = None
            try:
                self.result = self.nlu.process_sentence(sentence)
            except:
                print('result not found for sentece = {}'.format(sentence))
                continue

            # wait until result is received.
            while type(self.result)!=list:
                time.sleep(0.01)

            # Check if the output list has atleast one item
            if len(self.result)>=1:
                pass
            else:
                print('result has no intent or slots for the sentence = {}'.format(sentence))
                continue

            # Assigning expected intent and slots
            exp_intent = expected_output[i][0]
            exp_slots = expected_output[i][1:]

            # Testing intent
            if self.test_choice=='intent' or self.test_choice=='both':
                with self.subTest(Sentence_and_Intent = sentence.rstrip() + '--' + exp_intent):
                    # counting test number
                    test_total_number += 1

                    # conditions for the test to be considered as passed
                    # If there is no intent, there is IndexError
                    self.assertEqual(self.result[0][0], exp_intent)

            # Testing slots
            if self.test_choice=='slot'or self.test_choice=='both':
                for j in range(len(exp_slots)):
                    # counting test number
                    test_total_number += 1

                    # conditions for the test to be considered as passed for each slot
                    # If there is absense specific slot, there is an IndexError
                    with self.subTest(Sentence_and_Slot = sentence.rstrip() + '--' + exp_slots[j]):
                        self.assertEqual(self.result[0][1:][0][j], exp_slots[j])

            bar.update(i)

        bar.finish()
        print('Total numer of tests run is = {} \n see the log_file.txt for more information'.format(test_total_number))

if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.environ['CUDA_VISIBLE_DEVICES'] = '2'
    log_file = 'log_file.txt'
    # move previous log to log_file_last
    f = open(log_file, "w")
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner)
    # unittest.main()
    # f.close()
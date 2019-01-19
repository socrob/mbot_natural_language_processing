#!/usr/bin/env python3

import os
import sys
import time
import yaml
import unittest
import progressbar
sys.path.append(os.path.abspath('../'))
from src.mbot_nlu.mbot_nlu_common import NaturalLanguageUnderstanding

class MbotNluTest(unittest.TestCase):

    def setUp(self):
        '''
        Sets up the test fixture before exercising it
        '''
        print('\033[1;32mNLU TEST\033[0;37m')
        print('\033[1;32m==========================\033[0;37m')
        # print('\033[1;32m--------------------------\033[0;37m')
        # load test parameters from yaml file
        yaml_dict = yaml.load(open('../../../mbot_nlu_training/ros/config/config_mbot_nlu_training.yaml'))['test_params']
        classifier_path = yaml_dict['classifier_path']
        wikipedia_vectors_path = yaml_dict['base_path']
        self.pwd = yaml_dict['pwd']
        self.test_choice = yaml_dict['test_choice']
        debug = yaml_dict['debug']

        # NLU class and instance
        self.nlu = NaturalLanguageUnderstanding(classifier_path, wikipedia_vectors_path, debug=debug)

        # initialize session
        self.nlu.initialize_session()
        print('\033[1;32mnlu session is running\033[0;37m')

    def tearDown(self):
        self.nlu.close_session()
        print('\033[1;31mnlu session is closed\033[0;37m')

    def read_sentences_from_textfile(self, filename):
        '''
        open sentences.txt file and read sentences inside
        '''
        sentences = []
        with open(self.pwd + filename) as fp:
            for line in fp:
                sentences.append(line.strip('\n'))
        # rm commented sentences
        sentences = [[item] for item in sentences if '#' not in item]
        return sentences

    def read_expected_values_from_textfile(self, filename):
        '''
        get the expected intent and slots from text file
        '''
        available_slots = ['Person', 'Object', 'Source', 'Destination', 'Sentence']
        expected_output = [] # [['go', [('destination', 'kitchen')],['grasp',[('object', 'coke')], ... ]
        with open(self.pwd + filename) as fp:
            for line in fp:
                # skip commented lines
                if '#' in line: continue
                # strip end chars and split
                line = line.rstrip().split()
                #intent extraction
                intent = line.pop(0)
                # extracting the slot index from the current line
                slot_idx_list = []
                for slot in available_slots:
                    try: slot_idx_list.append(line.index(slot))
                    except: continue
                # Sorting the slot indexes
                slot_idx_list = sorted(slot_idx_list, key=int)
                # last element index
                slot_idx_list.append(len(line))
                # print(slot_idx_list)

                #slots extraction and appending to the current intent
                slots = []
                for v, w in zip(slot_idx_list, slot_idx_list[1:]):
                  # slots are extracted according to their indexes from previous search
                  slot = (line[v].lower(), ' '.join(line[v+1:w]))
                  # appending to the last item in the list (which is the current intent)
                  slots.append(slot)

                # append intent and slots
                expected_output.append([[intent], slots])
                # print(expected_output)

        return expected_output

    def test_mbot_nlu(self):
        '''
        the test function
        Publish a sentence and compare to an expected return value from the node
        '''
        # read nlu input and expected output from textfiles
        sentences = self.read_sentences_from_textfile('nlu_test_inputs.txt')
        expected_output = self.read_expected_values_from_textfile('nlu_expected_output.txt')

        # progress bar
        sentences_length = len(sentences)
        bar = progressbar.ProgressBar(max_value=sentences_length)

        # open raw result dump file
        raw_result_dump = open('raw_nlu_output.txt', 'w')

        # iterate over test sentences (list)
        # count wrong tests if either the intent or one of the slots are wrong
        wrong_tests = 0
        correct_untill_now = True
        def count_wrong_test(sentence_test_status, wrong_tests):
            if not sentence_test_status:
                wrong_tests += 1
                return False, wrong_tests
            else:
                return True, wrong_tests

        for i, sentence in enumerate(sentences):

            # Check if NLU has an output if not continue to the next sentence
            self.result = None
            self.result = self.nlu.process_sentence(sentence)

            # export raw result to text file (for manual inspection)
            raw_result_dump.write(str(sentence) + '===' + str(self.result) + '\n')

            # continue to next sentences if result is None or empty list
            result_length = len(self.result)
            if self.result is None or result_length==0:
                print('nlu is not able to classify the sentence = {}'.format(sentence))
                print('skipping to next sentence')
                correct_untill_now, wrong_tests = count_wrong_test(False, wrong_tests)
                continue

            # wait until result is received.
            while type(self.result)!=list:
                time.sleep(0.01)

            # Check if the output list has atleast one item
            if result_length<1:
                print('nlu is able to classify only intent or only one slot for the sentence = {}'.format(sentence))
                print('result = {}'.format(self.result))
                print('skipping to next sentence')
                correct_untill_now, wrong_tests = count_wrong_test(False, wrong_tests)
                continue

            # Assigning expected intent and slots
            exp_intent = expected_output[i][0][0]
            exp_slots = expected_output[i][1]

            # Testing intent
            if self.test_choice=='intent' or self.test_choice=='both':
                with self.subTest(Sentence_and_Intent = sentence[0].rstrip() + '--' + str(exp_intent)):
                    # conditions for the test to be considered as passed
                    # If there is no intent, there is IndexError
                    self.assertEqual(self.result[0][0], exp_intent)

                    # count failures
                    try:
                        if self.result[0][0]!=exp_intent:
                            correct_untill_now, wrong_tests = count_wrong_test(False, wrong_tests)
                    except IndexError:
                        correct_untill_now, wrong_tests = count_wrong_test(False, wrong_tests)

            # Testing slots
            if self.test_choice=='slot'or self.test_choice=='both':
                for slot_num, slot in enumerate(exp_slots):
                    # conditions for the test to be considered as passed for each slot
                    # If there is absence of specific slot, there is an IndexError
                    with self.subTest(Sentence_and_Slot = sentence[0].rstrip() + '--' + str(slot)):
                        self.assertEqual(self.result[0][1][slot_num], slot)

                    # count failures
                    try:
                        if self.result[0][1][slot_num]!=slot and correct_untill_now:
                            correct_untill_now, wrong_tests = count_wrong_test(False, wrong_tests)
                    except IndexError:
                        correct_untill_now, wrong_tests = count_wrong_test(False, wrong_tests)

            bar.update(i)

        bar.finish()

        # Accuracy
        Accuracy = (1-(wrong_tests/sentences_length))*100

        # print additional information
        print('\033[1;32m==========================\033[0;37m')
        print('\033[1;32mTEST COMPLETE\033[0;37m')
        print('\033[1;32m--------------------------\033[0;37m')
        print('\033[1;32mTotal number of tests and failures = {}, {} \nsee the log_file.txt for detailed report\033[0;37m'.format(sentences_length, wrong_tests))
        print('\033[1;32m--------------------------\033[0;37m')
        print('\033[1;32mAccuracy = {} \n\033[0;37m'.format(Accuracy))
        print('\033[1;32m--------------------------\033[0;37m')


if __name__ == '__main__':
    # env variables for tf and cuda
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.environ['CUDA_VISIBLE_DEVICES'] = '2'

    # test and log results
    log_file = 'log_file.txt'
    f = open(log_file, "w")
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner)

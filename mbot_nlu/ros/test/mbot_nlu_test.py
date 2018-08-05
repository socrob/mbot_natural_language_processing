#!/usr/bin/env python

import rospy
import sys
import unittest
import rostest
import rospkg

from std_msgs.msg import String
from mbot_nlu.mbot_nlu_common import NaturalLanguageUnderstanding
from mbot_nlu.msg import ActionSlotArray

PKG = 'mbot_nlu'

class MbotNluTest(unittest.TestCase):
    def setUp(self):
        '''
        Sets up the test fixture before exercising it
        '''
        # params
        self.result = None
        self.wait_for_result = None

        # get the absolute path of this test folder
        rospack = rospkg.RosPack()
        self.base_path = rospack.get_path('mbot_nlu') + '/ros/test/'

        # publishers
        self.component_input = rospy.Publisher(
            '/mbot_hri/mbot_nlu/input_sentence', String, queue_size=1)

        # subscribers
        self.component_output = rospy.Subscriber(
            '/mbot_hri/mbot_nlu/output_recognition', ActionSlotArray, self.result_callback)

        # give some time for publishers and subscribers to register in the network
        rospy.sleep(0.5)


    def tearDown(self):
        '''
        Deconstructs the test fixture after testing it
        '''
        self.component_input.unregister()
        self.component_output.unregister()


    def read_sentences_from_textfile(self, filename):
        '''
        open sentences.txt file and read sentences inside
        '''
        sentences = []
        with open(self.base_path + filename) as fp:
            for line in fp:
                sentences.append(line)
        return sentences


    def read_expected_values_from_textfile(self, filename):
        '''
        get the expected intent and slots from text file
        '''
        expected_output = [] # [['go', 'to the kitchen'],['pick','coke is an object'], ... ]
        with open(self.base_path + filename) as fp:
            for line in fp:
                line = line.rstrip()
                expected_output.append([line.split()[0], line.split(' ', 1)[1]])
        return expected_output


    def test_mbot_nlu(self):
        '''
        the test function
        Publish a sentence and compare to an expected return value from the node
        '''

        # read nlu input and expected output from textfiles
        sentences = self.read_sentences_from_textfile('nlu_test_inputs.txt')
        expected_output = self.read_expected_values_from_textfile('nlu_expected_output.txt')

        print expected_output

        for i, sentence in enumerate(sentences):

            rospy.loginfo("sentenceeee")
            rospy.loginfo(sentence)

            # publish test string
            test_sentence_msg = String()
            test_sentence_msg.data = sentence   # e.g. 'go to the kitchen'
            self.component_input.publish(test_sentence_msg)

            # wait until topic is received
            while not self.wait_for_result and not rospy.is_shutdown():
                rospy.sleep(0.1)

            # lower flag
            self.wait_for_result = False

            # conditions for the test to be considered as passed
            self.assertEqual(self.result.sentence_recognition[0].recognized_action, expected_output[i][0])
            self.assertEqual(self.result.sentence_recognition[0].slot[0], expected_output[i][1])


    def result_callback(self, msg):
        self.result = msg
        self.wait_for_result = True


if __name__ == '__main__':
    rospy.init_node('mbot_nlu_test')
    rostest.rosrun(PKG, 'test_mbot_nlu', MbotNluTest)

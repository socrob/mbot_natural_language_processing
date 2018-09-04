#!/usr/bin/env python

import rospy
import copy
import rospkg
from mbot_nlu.mbot_nlu_common import NaturalLanguageUnderstanding
from mbot_nlu.simple_phrase_divider import divide_sentence_in_phrases
from std_msgs.msg import String
from mbot_nlu.msg import Slot, ActionSlot, ActionSlotArray

class NLUNode(object):
    '''
    ROS wrapper for the nlu class
    input text, outputs intention (action) and slots (arguments)
    '''
    def __init__(self):
        # wheter to use syntaxnet to divide sentences
        self.opt_use_syntaxnet = rospy.get_param('~use_syntaxnet', True)
        if not self.opt_use_syntaxnet:
            rospy.loginfo('Parameter set to NOT USE syntaxnet - maybe you are still using it in the filter')
        # get paths relative to the location of this pkg
        rospack = rospkg.RosPack()
        classifier_path = rospack.get_path('mbot_nlu_classifiers') + \
            '/common/classifiers/' + rospy.get_param('~nlu_classifier', 'mithun_gpsr_robocup')
        wikipedia_vectors_path = rospack.get_path('mbot_nlu_training') + \
            '/common/resources/wikipedia_vectors'
        self.nlu_object = NaturalLanguageUnderstanding(classifier_path, wikipedia_vectors_path)
        # initiating nlu session
        self.nlu_object.initialize_session()
        # get from param server the rate at which this node will run
        self.loop_rate = rospy.Rate(rospy.get_param('~loop_rate', 10.0))
        # subscribe to a sentence (text) topic
        rospy.Subscriber("~input_sentence", String, self.nluCallback, queue_size=1)
        # to publish the recognition
        self.pub_sentence_recog = rospy.Publisher('~output_recognition', ActionSlotArray, queue_size=1)
        # flag to indicate that a text was received and needs to be processed
        self.nlu_request_received = False
        # to store the sentece that will be received in the callback
        self.received_sentence = None
        # inform the user that the node has initialized
        rospy.loginfo("natural_language_understanding node initialized, ready to accept requests")


    def nluCallback(self, msg):
        '''
        this callback will get executed every time you get a msg on nlu_input_sentence topic
        '''
        self.received_sentence = msg.data
        self.nlu_request_received = True


    def process_sentence(self, sentence):
        '''
        divide sentence into phrases and recognize the intention + args
        on each of them
        return: recognized_sentence, examples:
        [['go', ['kitchen is a destination']]]
        [['go', ['kitchen is a destination']], ['grasp', ['bottle is an object']]]
        '''
        # divide sentence into phrases, i.e. go to the kitchen and grasp the bottle
        # ['go to the kitchen', 'grasp the bottle']
        if self.opt_use_syntaxnet:
            phrases = divide_sentence_in_phrases(sentence)
        else:
            phrases = [sentence]

        if phrases is None:
            # some problem in using syntaxnet - no good verbs? using the raw sentence
            print('Using raw sentence -> {}'.format(sentence))
            phrases = [sentence]

        return self.nlu_object.process_sentence(phrases)


    def start_nlu(self):
        while not rospy.is_shutdown():
            if self.nlu_request_received == True:
                # lower flag
                self.nlu_request_received = False
                # recognize intention
                recognized_sentence = self.process_sentence(self.received_sentence)
                rospy.loginfo("Recognized : " + str(recognized_sentence))
                # [['go', ['kitchen is a destination']]]
                # create empty msg
                action_slot_array_msg = ActionSlotArray()
                for phrase in recognized_sentence:
                    # create empty msg
                    action_slot_msg = ActionSlot()
                    # fill msg
                    action_slot_msg.intention = phrase[0]
                    for slot in phrase[1]:
                        action_slot_msg.slots.append( Slot(type=slot[0], data=slot[1]) )
                    # append each single action_slot to from the array
                    action_slot_array_msg.sentence_recognition.append(copy.deepcopy(action_slot_msg))
                # publish recognition
                self.pub_sentence_recog.publish(action_slot_array_msg)
            # sleep to control the frequency of this node
            self.loop_rate.sleep()

        # closing NLU session
        self.nlu_object.close_session();


def main():
    rospy.init_node('natural_language_understanding', anonymous=False)
    natural_lang_under = NLUNode()
    natural_lang_under.start_nlu()

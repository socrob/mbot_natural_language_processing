#!/usr/bin/env python

from re import sub
import rospy
from threading import Thread
from mbot_world_model_ros.gpsr_dict import answers_dict
from mbot_robot_class_ros import mbot as mbot_class
from mbot_nlu.simple_phrase_divider import divide_sentence_in_phrases as syntaxnet
#from mbot_nlu.phrases import divide_sentence_in_phrases as syntaxnet
from std_msgs.msg import String
from mbot_nlu.msg import Slot, ActionSlotArray, ActionSlot

# Ease of access, does not create an object
mbot = mbot_class.mbotRobot


class NLULoop(object):
    """
    Handles the logic necessary for interacting with NLU when a complex sentence is given
    Example:
        1) Sentence "Find a knife, then take it to the kitchen"
        2) Split sentence into phrases using syntaxnet:
            a) Find a knife
            b) Take it to the kitchen
        3) Send a) to NLU, wait for response
        4) Analyze b) locating keywords, in this case "it", and replace with information from previous sentence(s)
        5) Send modified b) to NLU, wait for response
        6) Concatenate and publish the full response
    """

    keyword_to_slot_type = {
        # keyword: (what_to_add_before, [type1, type2,...])
        "it": ("the ", ["object", "sentence"]),
        "that": ("the ", ["object", "sentence"]),

        "him": ("", ["person"]),
        "her": ("", ["person"]),
        "them": ("", ["person"]),

        "there": ("the ", ["source", "destination"])
    }

    def __init__(self, use_syntaxnet=True):
        # auxiliary and setup variables
        self._phrases_left = None
        self._full_feedback = None
        self._completed = False
        self._waiting_feedback = False
        self._use_syntaxnet = use_syntaxnet
        self._syntaxnet_t = Thread()

        # publishers and subscribers
        self._nlu_pub = rospy.Publisher('~nlu_input_topic', String, queue_size=1)
        rospy.Subscriber('~nlu_output_topic', ActionSlotArray, queue_size=1, callback=self._nlu_callback)

    def _syntaxnet_thread(self, sentence):
        phrases = syntaxnet(sentence)
        if phrases is None or len(phrases) == 0:
            rospy.loginfo("Nothing returned from syntaxnet - sentence has no verb? Using whole sentence")
            self._phrases_left = [sentence]
        else:
            rospy.loginfo("Got {} from syntaxnet".format(phrases))
            self._phrases_left = phrases

        # fix tell specific by joining all phrases after 'tell' is seen
        fixed_phrases = NLUFilter.fix_tell(self._phrases_left)
        if self._phrases_left != fixed_phrases:
            self._phrases_left = fixed_phrases
            rospy.loginfo("After filtering: {}".format(fixed_phrases))

    @staticmethod
    def get_replacement(kw, feedback):
        # type: (str, ActionSlotArray) -> str
        corresponding_slots = NLULoop.keyword_to_slot_type[kw]

        # couldn't find a better way to do this, for some types we want to add "the" before, for others no...
        add_before = corresponding_slots[0]
        types_to_find = corresponding_slots[1]

        feedback_slots = [f.slots for f in feedback.sentence_recognition]

        # go through feedback in inverse order
        # gives priority to what was said last in order to give meaning to the keyword
        for phrase_slots in reversed(feedback_slots):
            # get data from matching slot types, if any
            matching_data = [slot.data for slot in phrase_slots if slot.type in types_to_find]
            if len(matching_data) > 0:
                if len(matching_data) > 1:
                    rospy.logwarn("Got more than one match for keyword {}: {}".format(kw, matching_data))
                return add_before + matching_data[0]  # if more than one, oh well

        # nothing was found to replace the keyword
        return ''

    @staticmethod
    def get_keywords(phrase):
        # type: (list[str]) -> set[str]
        return set(NLULoop.keyword_to_slot_type.keys()).intersection(phrase.split())

    def get_feedback(self):
        # type: () -> ActionSlotArray
        return self._full_feedback

    def is_done(self):
        return self._completed

    def set_new_sentence(self, sentence):
        assert type(sentence) is str

        # clean previous leftovers
        self._completed = False
        del self._full_feedback
        self._full_feedback = ActionSlotArray()

        if self._use_syntaxnet:
            self._phrases_left = None

            # check if there is already a syntaxnet call in progress (for simplicity do one at a time)
            if self._syntaxnet_t.is_alive():
                rospy.logwarn("Waiting for previous syntaxnet call to finish")
                self._syntaxnet_t.join()

            # call syntaxnet to get divided sentence
            rospy.loginfo("Calling syntaxnet in the background...")
            self._syntaxnet_t = Thread(target=self._syntaxnet_thread, name="syntaxnet", args=[sentence])
            self._syntaxnet_t.start()
        else:
            self._phrases_left = [sentence]

    def step(self):
        if self._waiting_feedback:
            return False

        if self._completed:
            rospy.logerr("No more steps to perform, NLU feedback loop is complete")
            return False

        elif self._full_feedback is None:
            raise Exception("First need to set a new sentence")

        if self._use_syntaxnet and self._syntaxnet_t.is_alive():
            self._syntaxnet_t.join()

        next_phrase = self._phrases_left[0]

        # if there is any feedback
        if len(self._full_feedback.sentence_recognition) > 0:
            # look for keywords in the next phrase
            keywords_found = self.get_keywords(next_phrase)
            if len(keywords_found) > 0:
                for kw in keywords_found:
                    # find replacement for keyword in feedback up to now
                    replacement = self.get_replacement(kw, self._full_feedback)
                    if replacement != '':
                        # if replacement found, replace kw in the phrase
                        # -- using sub to replace full keyword only i.e. not replacing 'it' in 'kitchen'
                        # -- all occurrences will be replaced if keyword is repeated (nonsensical)
                        rospy.loginfo("In sentence '{}' replaced keyword '{}' for '{}'"
                                      .format(next_phrase, kw, replacement))
                        next_phrase = sub(r"\b{}\b".format(kw), replacement, next_phrase)
                    else:
                        rospy.loginfo(
                            "In sentence '{}' found keyword '{}' but no replacement in current feedback"
                            .format(next_phrase, kw))
        # send to NLU
        self._waiting_feedback = True
        self._nlu_pub.publish(String(next_phrase))
        self._phrases_left.pop(0)

        return True

    def _nlu_callback(self, feedback):
        if self._completed:
            return

        self._waiting_feedback = False

        # extend current feedback
        self._full_feedback.sentence_recognition.extend(feedback.sentence_recognition)

        if len(self._phrases_left) == 0:
            self._completed = True


class NLUFilter(object):
    """
    Filter speech recognition output before sending to nlu
    i.e. handle ! char (confidence threshold not achieved), detect if its a hardcoded question,
    ask confirmation, etc.
    """

    confirmations = ['yes', 'yes please', 'positive', 'it is correct', 'correct', 'true', 'it is true', 'yep', 'ok', 'excellent', 'confirmed']
    denials = ['no', 'please no', 'negative', 'it is wrong', 'wrong', 'false', 'it is false', 'nope', 'never', "don't", 'do not', 'cancel', 'abort', 'stop', 'stop now']
    person_names_pre = ["i'm", "my name is"]
    tells = ['tell', 'say', 'ask']

    @staticmethod
    def is_bad_recognition(raw):
        return raw == '!'

    @staticmethod
    def is_introduce_request(raw):
        return 'introduce yourself' in raw

    @staticmethod
    def is_confirmation(raw):
        return raw in NLUFilter.confirmations

    @staticmethod
    def is_person_saying_name(raw):
        for pre in NLUFilter.person_names_pre:
            if pre in raw: return True
        return False

    @staticmethod
    def is_denial(raw):
        return raw in NLUFilter.denials

    @staticmethod
    def fix_tell(sentences):
        for idx, phrase in enumerate(sentences):
            # look for one of the words such as 'tell', 'ask'
            if len([word for word in NLUFilter.tells if word in phrase]) > 0:
                # build new list, joining the phrases that belong to the 'tell' phrase
                return list(sentences[:idx]) + list([' '.join(sentences[idx:])])
        return sentences

    @staticmethod
    def fix_take_grasp(feedback):
        action_slot_array_msg = ActionSlotArray()
        for item in feedback.sentence_recognition:
            action_slot_msg = ActionSlot()
            # if take check condition for grasp
            if item.intention=='take':
                num_slots = len(item.slots)
                num_obj = len([slot for slot in item.slots if slot.type=='object'])
                num_src = len([slot for slot in item.slots if slot.type=='source'])
                # if 1 total slots = object -> grasp
                if num_slots == 1 and num_obj == 1:
                    action_slot_msg.intention = 'grasp'
                # if 2 total slots = object + source -> grasp
                elif num_slots == 2 and num_obj == 1 and num_src == 1:
                    action_slot_msg.intention = 'grasp'
                # all other cases are take
                else:
                    action_slot_msg.intention = item.intention
            # if no take copy the feedback contents directly
            else:
                action_slot_msg.intention=item.intention
            
            for slot in item.slots: action_slot_msg.slots.append(Slot(type=slot.type, data=slot.data))
            action_slot_array_msg.sentence_recognition.append((action_slot_msg))
        return action_slot_array_msg


    def __init__(self):

        # create mbot robot class object
        mbot(enabled_components=['hri', 'navigation', 'manipulation', 'misc'])

        # use syntaxnet?
        opt_use_syntaxnet = rospy.get_param('~use_syntaxnet', True)
        if not opt_use_syntaxnet:
            rospy.logwarn('Parameter set to NOT USE syntaxnet')

        # ask for confirmation when length of sentence is below X words
        self.confirmation_max_words = rospy.get_param('~confirmation_max_words', 999)

        # skip beginning of sentence? for instance if using 'ok robot' or similar
        self.filter_sentence = rospy.get_param('~filter_sentence', True)
        self.filter_sentence_pattern = rospy.get_param('~filter_sentence_pattern', ".*(robot|please|mbot|gasparzinho) ")

        # setup talking function from mbot robot class, either waiting or not to finish talking
        if rospy.has_param('~wait_when_talking') and not rospy.get_param('~wait_when_talking'):
            self.say = mbot().hri.say
        else:
            self.say = mbot().hri.say_and_wait

        # setup publishers
        self.event_pub = rospy.Publisher('~event_out', String, queue_size=5)
        self.response_pub = rospy.Publisher('~full_response_topic', ActionSlotArray, queue_size=1)
        self.person_names_pub = rospy.Publisher('~person_names_topic', String,queue_size=1)

        # NLU feedback loop handler
        self.nlu_feedback_loop = NLULoop(use_syntaxnet=opt_use_syntaxnet)

        # auxiliary and setup variables
        self.in_nlu_loop = False
        self.previous_sentence = None
        self.speech = None
        self.in_silent_mode = False

        # setup subscribers
        rospy.Subscriber('~speech_topic', String, callback=self.speech_callback, queue_size=5)
        rospy.Subscriber('~event_in', String, callback=self.event_in_callback, queue_size=5)

        # to give some time for publishers to register into the network
        rospy.sleep(0.3)

    def speech_callback(self, sentence):
        self.speech = sentence

    def event_in_callback(self, event):
        if event.data == 'e_start_silent':
            self.event_pub.publish(String('e_silent_started'))
            self.in_silent_mode = True
        elif event.data == 'e_stop_silent':
            self.event_pub.publish(String('e_silent_stopped'))
            self.in_silent_mode = False
        else:
            self.event_pub.publish(String('e_failure'))

        rospy.loginfo('Silent mode: {}'.format(self.in_silent_mode))

    def process_speech(self, sentence):
        """
        Perform the following checks and behaviours:
        1. Is it a bad recognition? Do nothing
        1.5. Is it 'introduce yourself'?
        2. Is it a question? Speak the answer
        3. Is it a person saying his/her name? Output to a specific topic
        4. Follow up confirmation/denial? Start NLU feedback loop if it is a confirmation
        5. Is it a confirmation or denial without a previous sentence?
        6. Ask for confirmation
        """
        # convert raw speech recognition input to lower case
        raw = sentence.data.lower()

        rospy.loginfo('Recognized sentence after lower case : {}'.format(raw))

        # 1. Is it a bad recognition? Do nothing
        if NLUFilter.is_bad_recognition(raw):
            # this is the usual output from speech recognition when nothing interested is detected
            rospy.loginfo('Filtered - detected a bad recognition (!)')
            self.event_pub.publish(String('e_bad'))
            return

        # 1.5. Is it 'introduce yourself'?
        if NLUFilter.is_introduce_request(raw):
            mbot().misc.introduce_yourself()
            return

        # 2. Is it a question? Speak the answer
        try:
            answer = answers_dict[raw.strip('?')]
            self.previous_sentence = None
            self.say(answer)
            rospy.loginfo('Filtered - hardcoded question')
            self.event_pub.publish(String('e_hardcoded'))
            return
        except KeyError:
            pass  # not a question, move on

        # 3. Is it a person saying his/her name? Output to a specific topic
        if NLUFilter.is_person_saying_name(raw):
            # assume person name is the last word
            person_name = raw.split()[-1]
            self.person_names_pub.publish(String('{}'.format(person_name)))

            if not self.in_silent_mode:
                self.say('Nice to meet you {}'.format(person_name))
            rospy.loginfo('Filtered - person say his/her name: {}'.format(person_name))
            return

        # 4. Follow up confirmation/denial? Send previous spoken sentence to NLU if it is a confirmation
        is_conf = NLUFilter.is_confirmation(raw)
        is_denial = NLUFilter.is_denial(raw)

        if self.previous_sentence is not None:
            if is_denial:
                self.say("I understand")
                rospy.loginfo('Filtered - denial')
                self.event_pub.publish(String('e_denied'))
                self.previous_sentence = None
                return

            elif is_conf:
                self.say("Okay, please wait")
                rospy.loginfo('Will begin NLU loop')
                self.in_nlu_loop = True
                self.event_pub.publish(String('e_loop_start'))
                self.previous_sentence = None
                return

        # 5. Is it a confirmation or denial without a previous sentence?
        if self.previous_sentence is None and (is_conf or is_denial):
            if not self.in_silent_mode:
                self.say("Sorry, did you ask me anything? I don't recall")
            rospy.loginfo('Filtered - confirmation/denial with no previous sentence')

            if is_conf:
                self.event_pub.publish(String('e_conf_noprev'))
            elif is_denial:
                self.event_pub.publish(String('e_denial_noprev'))
            return

        # 6. Ask for confirmation
        # A new sentence can override confirmation
        if self.previous_sentence is not None:
            self.event_pub.publish('e_override')

        # Filter according to pattern, to remove for instance 'ok robot'
        if self.filter_sentence:
            try:
                self.previous_sentence = sub(self.filter_sentence_pattern, "", raw, count=1)
            except Exception: # invalid pattern given
                rospy.logwarn('Invalid pattern for substitution, using non-filtered sentence')
                self.previous_sentence = raw
        else:
            self.previous_sentence = raw

        # set in NLU loop as new sentence, setting in advance to call syntaxnet in background
        self.nlu_feedback_loop.set_new_sentence(self.previous_sentence)

        # if sentence has more than X words we skip confirmation
        if len(raw.split()) > self.confirmation_max_words:
            self.say("I will do as you said, please wait")
            self.event_pub.publish(String('e_skip_confirmation'))
            self.in_nlu_loop = True
            self.previous_sentence = None
            self.event_pub.publish(String('e_loop_start'))
        else:
            self.say("You said: {} . . is this correct?".format(self.previous_sentence))
            rospy.loginfo('Filtered - asked for confirmation')
            self.event_pub.publish(String('e_ask_confirmation'))

    def loop(self):
        rate = rospy.Rate(20)
        while not rospy.is_shutdown():
            if self.speech is not None:
                # process speech
                self.process_speech(self.speech)
                # reset speech
                self.speech = None

            if self.in_nlu_loop:
                if self.nlu_feedback_loop.is_done():
                    # fix take grasp problem
                    fixed_feedback = NLUFilter.fix_take_grasp(self.nlu_feedback_loop.get_feedback())
                    # set flags and publish the full response
                    self.in_nlu_loop = False
                    self.event_pub.publish(String('e_loop_done'))
                    self.response_pub.publish(fixed_feedback)
                    rospy.loginfo('NLU loop complete, result: {}'
                                  .format(fixed_feedback))
                else:
                    # do one step of the loop, if still waiting for feedback will not do anything
                    if self.nlu_feedback_loop.step():
                        self.event_pub.publish(String('e_loop_step'))

            rate.sleep()


def main():
    rospy.init_node('mbot_nlu_filter', log_level=rospy.INFO)
    NLUFilter().loop()


if __name__ == '__main__':
    main()

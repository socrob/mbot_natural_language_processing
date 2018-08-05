#!/usr/bin/env python
# run this file in ipython or another interactive env

import rospkg # only for obtaining the path
from mbot_nlu.mbot_nlu_common import NaturalLanguageUnderstanding as NLU

_rospack = rospkg.RosPack()
_classifier_path = _rospack.get_path('mbot_nlu_classifiers') + '/common/classifiers/pedro_gpsr'
_wikipedia_vectors_path = _rospack.get_path('mbot_nlu') + '/common/resources'

nlu = NLU(_classifier_path, _wikipedia_vectors_path, use_syntaxnet=True)

print('Try nlu.process_sentence() or nlu.process_single_phrase()')

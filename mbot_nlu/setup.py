#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# for your packages to be recognized by python
d = generate_distutils_setup(
 packages=['mbot_nlu', 'mbot_nlu_ros'],
 package_dir={'mbot_nlu': 'common/src/mbot_nlu', 'mbot_nlu_ros': 'ros/src/mbot_nlu_ros'}
)

setup(**d)

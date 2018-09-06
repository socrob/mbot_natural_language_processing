#!/usr/bin/env python

from __future__ import print_function
from termcolor import colored

class BulkdData2SimplePhrases(object):
  """This class contains methods to transform the bulk generated data from RoboCup command generator
  to simple sorted (Alphabetical) phrases. Lines with #, questions and answers, and duplicates are also removed.
  The final list of phrases (1 phrase per line) is saved in a text file named 'processed'. This script
  helps in collecting and cleaning data required for training the neural network.
  """
  def __init__(self):
    self.file_name_flag = False

  def open_and_readlines(self, file_name):
    # open file and load lines
    with open(file_name,'r') as file:
      contents = file.readlines()
    return contents

  def get_file_name(self):
    '''
    Get file name to process. If not entered correctly print more info and request again
    '''
    while not self.file_name_flag:
      file_name = raw_input(colored("\nPlease enter the relative path of file (w.r.t pwd) you want to process[sample.txt]\n",'green')) or "sample.txt"
      if '.txt' not in file_name:
        print(colored('Please re-enter the file path including the extension','yellow'))
        self.file_name_flag = False
      else:
        self.file_name_flag = True
    return str(file_name)

  def write_to_file(self, split):
    with open('processed.txt','w') as file:
        for item in split: file.write("%s\n" % item)

  def process_file(self):
    # get file name
    file_name = self.get_file_name()

    # open and read lines and return content
    contents = self.open_and_readlines(file_name)

    # rm lines with # and blank lines
    contents = [line.rstrip().replace('.','') for line in contents if '#' not in line and not line.startswith('\n')]

    # split sentences at [','] and remove 'and', questions, answers and duplicates if there is
    split = [line.split(',') for line in contents]
    split = [line.replace(' and','').strip().lower() for i in range(len(split)) for line in split[i]]
    split = [line for line in split if not line.startswith('a:') and not line.startswith('q:') and not line.startswith('question')]
    split = list(set(split))

    # rm intro (eg: could you, please)
    q_rm_intro = raw_input(colored("Want to remove the intro? (ex: 'could you please') [Y/n]\n",'yellow')) or "Y"
    if q_rm_intro=='Y':
      split = [line.replace('could you ','') for line in split]
      split = [line.replace('robot ','') for line in split]
      split = [line.replace('please ','') for line in split]
    elif q_rm_intro=='n':
      print(colored('Not removing the intro, moving on...','yellow'))

    # sorting alphabetically
    split.sort()

    # write to file
    print(colored('PROCESSING DONE','green'))
    print('======================================')
    print(colored('Saving processed texts to "processed.txt"','green'))
    self.write_to_file(split)
    print(colored('Total number of unique phrases = {}','green').format(len(split)))
    print('======================================')

if __name__ == '__main__':
  # example of how to use this class
  class_inst = BulkdData2SimplePhrases()
  class_inst.process_file()

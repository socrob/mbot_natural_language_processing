#!/bin/bash

# dir path of this file
DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

wikipedia_folder="${DIR}"/../resources/wikipedia_vectors
wikipedia_src_folder="${DIR}"/../src/mbot_nlu_training/gen_wikipedia_vectors

# make sure glove.6B.300d.txt file exists, otherwise wikipedia vectors cannot be generated!
if [ ! -f "${wikipedia_folder}"/glove.6B.300d.txt ]; then
    # warn the user about the fact that he tried to pull from x but he is currently in branch y, therefore doing nothing
    RED='\033[0;31m'
    NC='\033[0m' # No Color
    printf "${RED}ERROR: File glove.6B.300d.txt not found, make sure to run nlu_training_setup.bash !${NC}\n"
    exit 0
fi

# echo 'WARNING: you have pending git jobs!' in yellow color:
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
printf "${YELLOW}WARNING: This will take a while !${NC}\n"

# sleep 2
echo 'file glove.6B.300d.txt found!, process started...'

function remove_old_files()
{
    # args : 1. file to be removed

    # rm dictionary wordvectors
    if [ -f "${wikipedia_folder}"/$1 ]; then
        echo "Removing $1 file, will be replaced by a new one"
        rm "${wikipedia_folder}"/$1
    fi
}

remove_old_files dictionary
remove_old_files wordvectors

# check if the big_dictionary and big_wordvectors file have already been generated
if [ -e "${wikipedia_folder}"/big_wordvectors ] && [ -e "${wikipedia_folder}"/big_dictionary ]

then
    # echo 'INFO: 'The files (big_dictionary & big_wordvectors) have already been processed, moving on...':
    YELLOW='\033[1;33m'
    NC='\033[0m' # No Color
    printf "${YELLOW}INFO: 'The files (big_dictionary & big_wordvectors) have already been processed, moving on...'${NC}\n"

    echo "iterating over old dictionary and finding its corresponding wordvectors using big dictionary and big wordvectors (400,000) to create new simplified dictionary and wordvectors (50,000)"
    python3 "${wikipedia_src_folder}"/list_to_vec.py "${wikipedia_folder}"
else
    echo "converting glove to dic pretrained data into big dictionary and big wordvectors"
    python3 "${wikipedia_src_folder}"/glove_to_dic.py "${wikipedia_folder}"

    echo "iterating over old dictionary and finding its corresponding wordvectors using big dictionary and big wordvectors (400,000) to create new simplified dictionary and wordvectors (50,000)"
    python3 "${wikipedia_src_folder}"/list_to_vec.py "${wikipedia_folder}"
fi

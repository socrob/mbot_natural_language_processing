#!/bin/bash

# apt installs
debian_packagelist=(
    unzip
    python-msgpack
)

# pip package list
pip3_packagelist=(
    asciitree
    msgpack
    msgpack_numpy
    PyYAML
    numpy
    scipy
    scikit-learn
    progressbar2
)

# Install debian packages listed in array above
sudo apt-get install -y ${debian_packagelist[@]}

# Install python packages listed in array above in python 3
pip3 install ${pip3_packagelist[@]} --user

# dir path of this file
DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Setup custom
nlu_training_dir="${DIR}"/../..

# file to download
word_vectors_zip="glove.6B.zip"

# check if the glove.6B.300d.txt file has already been downloaded
if [ -e ${nlu_training_dir}/common/resources/wikipedia_vectors/glove.6B.300d.txt ]

then
    # echo 'INFO: 'The glove pretrained file has already been downloaded, moving on...':
    YELLOW='\033[1;33m'
    NC='\033[0m' # No Color
    printf "${YELLOW}INFO: 'The glove pretrained file has already been downloaded, moving on...'${NC}\n"
    bash "${nlu_training_dir}"/common/setup/gen_wikipedia_vectors.sh

else
    # download wikipedia pre-trained vectors
    wikipedia_file="http://nlp.stanford.edu/data/${word_vectors_zip}"

    mkdir -p /tmp/wikipedia && cd "$_"
    wget -t 5 -c ${wikipedia_file}

    # extract and move to desired dir
    mkdir -p ${nlu_training_dir}/common/resources/wikipedia_vectors/
    unzip ${word_vectors_zip} -d "$_"

    # remove zip tmp file to save hard disk space
    rm -rf /tmp/wikipedia
    # to prevent shell-init: error retrieving current directory...
    cd ${nlu_training_dir}

    # keep only the 300 dimension vectors
    rm ${nlu_training_dir}/common/resources/wikipedia_vectors/glove.6B.50d.txt
    rm ${nlu_training_dir}/common/resources/wikipedia_vectors/glove.6B.200d.txt
    rm ${nlu_training_dir}/common/resources/wikipedia_vectors/glove.6B.100d.txt

    # generate wikipedia vectors
    bash "${nlu_training_dir}"/common/setup/gen_wikipedia_vectors.sh
fi
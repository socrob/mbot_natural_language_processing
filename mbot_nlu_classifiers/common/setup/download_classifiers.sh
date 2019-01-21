#!/bin/bash

# Change here when new classifiers are added
# Only .tar.gz file extensions are supported
# -> compress a directory using  tar -zcvf OUTPUT_FILE DIRECTORY
# If using nextcloud, need to add /download to the end of the url

CLASSIFIERS=(
    1 pedro_gpsr http://dantecloud.isr.tecnico.ulisboa.pt/index.php/s/3Y4pdcT9cm2AbY6/download
    2 mithun_gpsr http://dantecloud.isr.tecnico.ulisboa.pt/index.php/s/Zo9c2DzaFArTLKE/download
    3 mithun_gpsr_robocup http://dantecloud.isr.tecnico.ulisboa.pt/index.php/s/RR8zzjm6ddPXFFE/download
    4 mithun_eegpsr_robocup http://dantecloud.isr.tecnico.ulisboa.pt/index.php/s/4ioQP2S5knbzNy5/download
    5 mithun_erl_madrid http://dantecloud.isr.tecnico.ulisboa.pt/index.php/s/p2tiL7kBSZbE3Yk/download
    6 mithun_erl_lisbon http://dantecloud.isr.tecnico.ulisboa.pt/index.php/s/4GnWTPLnoeqJTTa/download
    #7 example exampleurl
)

# dir path of this file
DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

REL_PATH=/../classifiers/

# Find proj root
ABS_PATH=${DIR}${REL_PATH}

# Asks user which files to download, then downloads them and sets them up
NCLASS=$((${#CLASSIFIERS[@]}/3))
echo "Which classifier do you wish to download?"
for (( i=0; i<=${NCLASS}; i++ )) ; do
    echo "${CLASSIFIERS[3*${i}]} ${CLASSIFIERS[3*${i}+1]}"
done
echo "Choose (1)-(${NCLASS})"
echo "q/Q to exit without downloading"

# Allow default option given as argument (mostly for installation scripts)
if [ $# -ge 1 ] ; then
    choose=$1
    echo "Chosen ${choose} automatically from given argument"
else
    read choose
fi

# Allow exiting
if [ "${choose}" == "q" ] || [ "${choose}" == "Q" ] ; then
    exit
fi

choose=$((choose-1))
if [ "${choose}" -ge "${NCLASS}" ] || [ "${choose}" -lt 0 ] ; then
    echo "Invalid option, choose a number from the classifiers"
    exit
fi

NAME=${CLASSIFIERS[3*$choose+1]}
URL=${CLASSIFIERS[3*$choose+2]}
echo "Downloading from ${URL}"
mkdir -p $ABS_PATH && cd $ABS_PATH
curl -o $NAME.tar.gz $URL
tar -zxvf $NAME.tar.gz
rm $NAME.tar.gz

echo "Successfuly installed to ${ABS_PATH}${NAME} and removed temporary files"

NOTE: This package is purely based on python 3 and does not depend up on ros.

This Readme has additional information regarding the DNN training procedure compared to the [main README file](https://github.com/socrob/mbot_natural_language_processing/blob/master/README.md). We prefer to train the neural networks in virutal environment. The setup is as follows.

## Virtual environment Setup*

- Make sure you have virtual env installed, if not, please install it using this command
~~~
sudo apt-get install python3-pip python3-dev python-virtualenv
~~~
- Install pip using one of the below commands
~~~
sudo pip install -U pip 
easy_install -U pip
~~~
- Create a directory for the virtual environment, choose a Python interpreter and activate the virtual env
~~~
mkdir ~/tensorflow
cd ~/tensorflow
virtualenv --system-site-packages -p python3 venv
source ~/tensorflow/venv/bin/activate
~~~
When the Virtualenv is activated, the shell prompt displays as (venv) $  

- Upgrade pip
~~~
pip install -U pip
~~~

## Installing DNN training dependencies and initiating the DNN training

For installing debs and initiating the DNN training please follow the DNN training set up in the [main README](https://github.com/socrob/mbot_natural_language_processing/blob/master/README.md)

## Additional tips for training procedure

- If you want to see the graphics processor and memory usage and the index of gpu (to be updated in the [configuration file](https://github.com/socrob/mbot_natural_language_processing/blob/master/mbot_nlu_training/ros/config/config_mbot_nlu_training.yaml)), use [glances](https://nicolargo.github.io/glances/). Glances can be installed using,
~~~
pip install glances --user
~~~

- If you have multiple GPUs you can run the intention and slots training at the same time, given that you have updated the GPU index in the [configuration file](https://github.com/socrob/mbot_natural_language_processing/blob/master/mbot_nlu_training/ros/config/config_mbot_nlu_training.yaml)

## Brief introduction to the DNN training script

The input sentences are converted to wordvectors using [GloVe](https://nlp.stanford.edu/projects/glove/) pre-trained vectors and the labels are converted to one-hot vectors before the training. The loss function (softmax cross entropy) is minimized using Adam optimizer with a constant learning rate. The DNN (LSTM) properties (Layers and number of cells) 
can be altered in the [configuration file](https://github.com/socrob/mbot_natural_language_processing/blob/master/mbot_nlu_training/ros/config/config_mbot_nlu_training.yaml).

*Follow https://www.tensorflow.org/install/install_linux#installing_with_virtualenv in case of any doubts about the virtual environment setup and tensorflow installation.

end of file

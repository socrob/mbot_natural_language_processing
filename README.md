# Natural Language Understanding (NLU) using Deep Neural Networks (DNN)
Maps robot commands (text) into intentions and arguments used during [RoboCup@Home 2018](http://www.robocup2018.com/)

Brought to you by:
- [Instituto Superior Tecnico, Lisboa](http://welcome.isr.tecnico.ulisboa.pt/)
- [Institute for Systems and Robotics (ISR)](http://welcome.isr.tecnico.ulisboa.pt/)
- [Laboratório de Robótica e Sistemas em Engenharia e Ciência (LARSyS)](http://larsys.pt/)
- [SocRob RoboCup team](http://socrob.isr.tecnico.ulisboa.pt)

This code was tested on Ubuntu 16.04 and ROS kinetic. The DNN was trained using [TensorFlow](https://www.tensorflow.org/) platform.

There are two parts to this repository. First, the DNN inference or the usage of the classifiers and second, the DNN training procedure.

## Minimum Requirements (Inference / Training)
- Processor -  Intel(R) Core(TM) i7-3630QM CPU @ 2.40GHz / Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz
- Memory -  2GB RAM / 5GB RAM
- Graphics -  Not required / NVIDEA GEFORCE GTX 1060
- OS -  Ubuntu 16.04 with ROS Kinetic

## DNN Inference setup

- Clone this repository to your workspace source folder using the below command  
~~~~
git clone https://github.com/socrob/mbot_natural_language_processing.git  
cd mbot_natural_language_processing
~~~~
- Install dependencies and finish the setup by invoking the automated script (require admin privilages)  
~~~~
sudo ./repository.debs
(Give No for all the unnecessary prompts)
~~~~
- Build the packages and source the workspace
~~~~
catkin build mbot_nlu mbot_nlu_classifiers mbot_nlu_filter mbot_nlu_training
source ../../devel/setup.bash
~~~~

## DNN Inference

# Single sentence classification

- Run the launch file
~~~~
roslaunch mbot_nlu mbot_nlu.launch nlu_classifier:=mithun_gpsr_robocup
~~~~
- Visualize the intention and arguments
~~~~
rostopic echo /hri/nlu/mbot_nlu/output_recognition
~~~~
- Trigger the node with some text
~~~~
rostopic pub --once /hri/nlu/mbot_nlu/input_sentence std_msgs/String "data: 'go to the kitchen'"
~~~~

# Multi sentence classification

- Edit ros parameter to use sentence divider
~~~~
roscd mbot_nlu
gedit ros/launch/mbot_nlu.launch
set "use_syntaxnet" param to "True"
~~~~
- Run the launch file
~~~~
roslaunch mbot_nlu mbot_nlu.launch nlu_classifier:=mithun_gpsr_robocup
~~~~
- Visualize the intention and arguments
~~~~
rostopic echo /hri/nlu/mbot_nlu/output_recognition
~~~~
- Trigger the node with some text
~~~~
rostopic pub --once /hri/nlu/mbot_nlu/input_sentence std_msgs/String "data: 'go to the kitchen and pick the spoon'"

## DNN training setup
- Clone this repository to your PC dedicated for training the DNN using the below command  
~~~~
git clone https://github.com/socrob/mbot_natural_language_processing.git  
cd mbot_natural_language_processing
~~~~
- Install dependencies and finish the training setup by invoking the automated script  
~~~~
source mbot_nlu_training/common/setup/nlu_training_setup.sh
~~~~
- Edit and Verify the parameters used in the training using the configuration file
~~~~
gedit mbot_nlu_training/ros/config/config_mbot_nlu_training.yaml
~~~~
- Generate the data and initiate the training 
  - Intention classifier training
~~~~
cd mbot_nlu_training/common/src/mbot_nlu_training/gpsr/intention_NN/
./gpsr_data_generator.py (wait for completion)
./train_nn_model.py
~~~~
  - Arguemnts/ Slots classifier training
~~~~
cd mbot_nlu_training/common/src/mbot_nlu_training/gpsr/slots_NN/
./gpsr_data_generator.py (wait for completion)
./train_nn_model.py
~~~~

Upon training completion the classifiers will saved in latest_intents_classifier and latest_slots_classifier in the respective folders (intention_NN/slots_NN). Copy the files in the above mentioned folders to `mbot_nlu_classifiers/common/classifiers/` with sample structure given below and follow the DNN Inference procedure with `nlu_classifier` paramer as your `CLASSIFIER_NAME`
  
Your classifier should be in a tree such as:    
~~~~
root
     | - CLASSIFIER_NAME
           | - intent
           | - slots
~~~~

## NLU automated test

To execute the test, simply execute the python script in the test folder. The test input sentences are sourced from `nlu_test_inputs.txt` and corresponding ideal outputs are sourced from `nlu_expected_output.txt` files. Both files can be modified to the user needs, but make sure that the input sentence and the corresponding output are properly paired. Once the test is complete a detailed log of errors will be published in `log_file.txt` in the same folder. 

~~~
cd /mbot_natural_language_processing/mbot_nlu/common/test
./mbot_nlu_test.py
~~~

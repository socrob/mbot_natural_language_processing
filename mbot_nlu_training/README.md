NOTE: This package is purely based on python and tensorflow
Does not depend on ROS

Edited by Mithun K

Step by step on how to setup your computer for training.

1. Install TF using virtual env (ref: https://www.tensorflow.org/install/install_linux#installing_with_virtualenv)
2. Download the training files (http://dante.isr.tecnico.ulisboa.pt/mkinarullathil/mbot_natural_language_processing/tree/intent_and_slots_training_and_results/mbot_nlu_training) to Batatinha
3. Go to common/src/mbot_nlu_training/gpsr/
4. The intention_NN and slots_NN folders has all the required files for training,
   all you have to do is run the ```train_nn_model.py``` in respective folders.
5. Open glances to see the usage of memory and GPU. If you see anyone using gpu 0, change the gpu number in the train_nn_model script.
6. Don't run both trainings at the same time.
7. It's a usual convention to run the file with the gpu number, for the intention of feedback for the others using the same system.
   i.e: python train_nn_model.py gpu 0
8. The output of the training is saved in the same folder.

Brief introduction to train_nn_model.py

1. I have added comments in intention training file (not available in slots).
2. There are two parts. One is importing data and processing the sentences to word vectors. (This happens in the first 15-20 mins of training)
3. inputs file has the sentences and output has the intentions.
   Each word in each sentence of the input is searched in ```dictionary``` and
   corresponding ```wordvector``` is saved as a list.
   The outputs are converted to oneHot vectors
   (eg: [1,0,0,0,0,0,0,0,0], [0,0,0,0,1,0,0,0,0]).
   The position of 1 is corresponding to the position of the intent in the list of 9 intents.

end of file


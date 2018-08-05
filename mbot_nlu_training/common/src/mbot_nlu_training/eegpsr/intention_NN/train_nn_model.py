#!/usr/bin/env python3

import os
import yaml
import time
import msgpack
import msgpack_numpy
import numpy as np
import progressbar
import tensorflow as tf
from termcolor import colored
from tensorflow.contrib import rnn
from sklearn.utils import resample
start_time = time.time()

class intent_training_class():
    '''
    This class contains a set of methods used to train the intents classifier for mbot_nlu package.
    '''
    def __init__(self, yaml_dict):
        '''
        constructor
        '''
        self.available_intents = yaml_dict['available_intents']                        # list of available intents, add to list if your training data has more intents.
        self.n_steps = yaml_dict['n_steps']                                            # max n of words in the sentences
        self.n_epochs = yaml_dict['n_epochs']                                          # n epochs
        self.base_path = yaml_dict['base_path']                                        # path to dictionary and wordvector files
        self.rnn_size = yaml_dict['rnn_size']                                          # n of lstm cells in each layer
        self.n_lstm_layers = yaml_dict['n_lstm_layers']                                # n lstm layers
        self.batch_size = yaml_dict['batch_size']                                      # batch size
        self.n_examples = yaml_dict['n_examples']                                      # n of samples for training and validation
        self.number_of_batches = yaml_dict['number_of_batches']                        # n batches
        self.number_of_validation_batches = yaml_dict['number_of_validation_batches']  # n validation batches
        self.embedding_size = yaml_dict['embedding_size']                              # embedding size of each wordvector
        self.forget_bias = yaml_dict['forget_bias']                                    # forget bias for lstm cell
        self.learning_rate = yaml_dict['learning_rate']                                # initial learning rate for adam optimizer
        self.loss_lower_limit = yaml_dict['loss_lower_limit']                          # used to stop the training when the loss is below this value
        self.debug = yaml_dict['debug']                                                # debug, will give lot of info about the execution if True
        self.n_classes = len(self.available_intents)                                   # n of actions
        self.use_tensorboard = yaml_dict['use_tensorboard']                            # to use tensorboard or not
        self.resample_replace = yaml_dict['resample_replace']                          # to use duplicate data(randomly) while shuffling and batching

    def import_data(self, debug=False):
        '''
        method for importing and processing input data
        '''
        # Importing pickled wordvectors, dictionary, inputs and labels
        with open(self.base_path + '/wordvectors', 'rb') as vectors_file:
            print("Importing wordvectors...", end=' ', flush=True)
            word_vectors = msgpack_numpy.load(vectors_file)
            print("Done")
        with open(self.base_path + '/dictionary', 'rb') as dict_file:
            print("Importing dictionary...", end=' ', flush=True)
            dictionary = msgpack.load(dict_file, raw=False)
            print("Done")
        with open('inputs', 'rb') as data_inputs_file:
            print("Importing inputs...", end=' ', flush=True)
            sentences = msgpack.load(data_inputs_file, raw=False)
            print("Done")
        with open('outputs', 'rb') as data_outputs_file:
            print("Importing labels...", end=' ', flush=True)
            outputs = msgpack.load(data_outputs_file, raw=False)
            print("Done")


        ########################################################################################################################
        # Processing inputs
        ########################################################################################################################
        print('Modifying input sentences...')

        # importing progressbar
        bar = progressbar.ProgressBar(max_value=len(sentences), redirect_stdout=True, end=' ')
        # preassigning the inputs variable for faster processing
        data_inputs = np.zeros((len(sentences), self.n_steps), dtype=np.int32)
        # initiating all the inputs to index of zero vector (zerowordvec_idx = dictionary['zerowordvec'])
        zerowordvec_idx = dictionary['zerowordvec']
        data_inputs[:,:] = zerowordvec_idx
        # Modifying the input senteces for training.
        lengths = []
        i = 0
        words_not_found_in_dic = []
        for line in sentences:
            line = line.lower()             # All the sentences to lowe caps
            line = line.strip('\n')         # Strip all the \n at the end
            line = line.replace(',', '')    # Removing ","
            line = line.rsplit(' ', -1)     # Split the sentence to a list of strings(words)
            # Initializing an empty list
            h = []
            # Iterating each word in the line over the dictionary and appending the indexes to a list
            for k in range(len(line)):
                # searching the index of each word in the dictionary and saving the number to the variable "idx"
                try:
                    idx = dictionary[line[k]]
                except:
                    # Exporting the words not found in the dictionary to (for reference)
                    idx = zerowordvec_idx
                    words_not_found_in_dic.append(line[k])
                # Appending the index(idx) of each word to the list h.
                h.append(idx)
            # appending the length of each line to the list lengths
            lengths.append(len(line))
            # modifying the array
            data_inputs[i, :len(h)] = h
            # bar update
            bar.update(i)
            i = i + 1
        # bar finish
        bar.finish()
        # if words are not found in dictionary
        if len(words_not_found_in_dic)!=0:
            # rm duplicates
            words_not_found_in_dic = list(set(words_not_found_in_dic))
            # use this file to update most_common_words and to generate a new dictionary and wordvector
            with open('words_not_found_in_dic.txt','w') as f:
                for item in words_not_found_in_dic: f.write(item + '\n')
            print(colored('\nNo. of words not found in the dict = {}, pls. check words_not_found_in_dic file\n'.format(len(words_not_found_in_dic)),'red'), end='', flush=True)

        # if debug print input sample to check if the input pipeline is correct
        if debug:
            print('Sample input data')
            print('=========================================================')
            print('input sentence are {}'.format(sentences[0:2]))
            print('input lengths are {}'.format(lengths[0:2]))
            print('[Vector]input sentence are {}'.format(data_inputs[0:2]))
            print('=========================================================')
        ########################################################################################################################
        # Processing labels
        ########################################################################################################################
        print("Modifying labels...")

        # initiating progress bar
        bar = progressbar.ProgressBar(max_value=len(outputs), redirect_stdout=True, end=' ')
        # preassinging outputs variable for faster processing
        data_outputs = np.zeros((len(outputs), len(self.available_intents)), dtype=np.int32)
        # Iterating over outputs list and corresponding one hot vectors is stacked( using vstack) to a list (o)
        v=0
        for output in outputs:
            # find intent if it exists in available intents list
            try:
                idx_found = self.available_intents.index(output)
            except ValueError:
                raise Exception('Could not find this output = {} in the available list of intents'.format(output))
            # modifying the output array
            data_outputs[v, idx_found] = 1
            # bar update
            bar.update(v)
            v = v + 1
        # bar finish
        bar.finish()

        # debug prining
        if debug:
            print('Sample output data')
            print('=========================================================')
            print('output labels are {}'.format(outputs[0:2]))
            print('[Vector]output labels are {}'.format(data_outputs[0:2]))
            print('=========================================================')

        return word_vectors, data_inputs, data_outputs, lengths


    def suffle_n_batch(self, data_inputs, data_outputs, lengths):
        '''
        shuffles and splits the data inputs for each epoch in to batches. self.number_of_batches batches are used for training and self.number_of_validation_batches batch is used for validation
        '''
        split_list_inputs = []
        split_list_outputs = []
        split_list_lengths = []
        # resamplining data
        data_inputs, data_outputs, lengths = resample(data_inputs, data_outputs, lengths, replace=self.resample_replace)
        # splitting to batches
        len_each_chunks = int(len(data_inputs)/self.number_of_batches)
        for i in range(self.number_of_batches):
            split_list_inputs.append(np.array(data_inputs[len_each_chunks*(i):len_each_chunks*(i+1)]))
            split_list_outputs.append(np.array(data_outputs[len_each_chunks*(i):len_each_chunks*(i+1)]))
            split_list_lengths.append(np.array(lengths[len_each_chunks*(i):len_each_chunks*(i+1)]))

        if self.debug:
            print('Sample input data after shuffle and batch')
            print('=========================================================')
            print('[Vector]input sentence are {}'.format(split_list_inputs[0][0:2]))
            print('input lengths are {}'.format(split_list_lengths[0][0:2]))
            print('=========================================================')
            print('Sample output data after shuffle and batch')
            print('=========================================================')
            print('[Vector]output labels are {}'.format(split_list_outputs[0][0:2]))
            print('=========================================================')

        return split_list_inputs, split_list_outputs, split_list_lengths


    def recurrent_neural_network(self, rnn_inputs, sequence_length_placeholder):
        '''
        defining nn layers (graph in TF terms)
        '''
        # def of 1 layer of lstm
        def cell(): return  tf.nn.rnn_cell.BasicLSTMCell(self.rnn_size, forget_bias=self.forget_bias)
        # initializing weights and biases for the output layer
        layer = {'weights': tf.Variable(tf.random_normal([self.batch_size, self.rnn_size, self.n_classes]), name='weights'),
                 'biases': tf.Variable(tf.random_normal([self.n_classes]), name='biases')}

        # n layer of lstm with rnn_size number of cells
        with tf.device('/GPU:0'):
            layers = self.n_lstm_layers
            cell = tf.nn.rnn_cell.MultiRNNCell([cell() for _ in range(layers)], state_is_tuple=True)

        # building the graph while running the session (tf methods which reduces the load on the pc)
        outputs, _ = tf.nn.dynamic_rnn(cell, rnn_inputs, sequence_length_placeholder, dtype=tf.float32)

        # output layer modifications
        with tf.device('/GPU:0'):
            output = tf.matmul(outputs, layer['weights']) + layer['biases']
            index = tf.range(0, self.batch_size) * self.n_steps + (sequence_length_placeholder - 1)
            flat = tf.reshape(output, [-1, self.n_classes])
            relevant = tf.gather(flat, index)
            prediction = tf.nn.softmax(relevant)

        return relevant


    def train_neural_network(self):
        '''
        Main method used contatining the training processes.
        '''
        # import data
        word_vectors, data_inputs, data_outputs, lengths = self.import_data(debug=self.debug)

        ########################################################
        # TF placeholder implementation
        ########################################################
        input_placeholder = tf.placeholder(tf.int32, [self.batch_size, self.n_steps], name='input_placeholder')
        labels_placeholder = tf.placeholder(tf.int32, [self.batch_size, self.n_classes], name='labels_placeholder')
        sequence_length_placeholder = tf.placeholder(tf.int32, [None], name='inputs_length')

        # wordvector embeddings
        print('Embedding wordvectors...', end=' ', flush=True)
        embeds = tf.convert_to_tensor(word_vectors, name="embeds")
        print('Done')
        # look up for embeds/wordvectors (words_index to 300 len vector)
        rnn_inputs = tf.nn.embedding_lookup(embeds, input_placeholder)
        # output of the nn layer. this prediction is compared with the actual labels to find the cost and minimize it
        prediction = self.recurrent_neural_network(rnn_inputs, sequence_length_placeholder)
        # cost function
        cost = tf.reduce_mean(tf.losses.sigmoid_cross_entropy(logits = prediction, multi_class_labels = labels_placeholder))
        # adam optimizer
        optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(cost)

        # TB file writer def
        if self.use_tensorboard:
            merged_summary = tf.summary.merge_all()
            writer = tf.summary.FileWriter('./tf_log_intent/')

        # configuring session to use only required amount of memory
        saver = tf.train.Saver()                # for saving the classifiers
        config = tf.ConfigProto()               # for session configurations (eg: gpu memory growth)
        config.gpu_options.allow_growth = True  # allow only required gpu memory
        print("\nStarting training...")
        with tf.Session(config=config) as sess:
            # adding graph to the writer
            if self.use_tensorboard: writer.add_graph(sess.graph)
            print('Initiating global variables...', end=' ', flush=True)
            sess.run(tf.global_variables_initializer())
            print('Done')

            ########################################################################################################################
            # NN Training
            ########################################################################################################################
            cost_value = 0
            for epoch in range(self.n_epochs):
                epoch_loss = 0
                steps = self.number_of_batches-self.number_of_validation_batches

                # shuffling and generating training and validation batches every epoch
                print('Splitting data inputs to batches of {} ({} for training {} for validation)...'.format(self.number_of_batches, self.number_of_batches-self.number_of_validation_batches, self.number_of_validation_batches ), end=' ', flush=True)
                [split_list_inputs, split_list_outputs, split_list_lengths] = self.suffle_n_batch(data_inputs, data_outputs, lengths)
                print('Done')
                # iterating through the batches
                for i in range(steps):
                    print('Processed batches = {}/{}'.format(i+1, steps))
                    range_each_chunks = len(split_list_inputs[i])
                    # progressbar
                    bar = progressbar.ProgressBar(max_value=range_each_chunks, redirect_stdout=True, end=' ', flush=True)
                    # iterating over batches
                    for k in range(0, range_each_chunks):
                        # assining each input variable
                        epoch_x = np.array(split_list_inputs[i][k: k+self.batch_size])
                        epoch_y = np.array(split_list_outputs[i][k: k+self.batch_size])
                        inputs_length = np.array(split_list_lengths[i][k: k+self.batch_size])
                        # finding the cost for each input
                        _, cost_value = sess.run([optimizer, cost], feed_dict={input_placeholder: epoch_x, labels_placeholder: epoch_y, sequence_length_placeholder: inputs_length})
                        epoch_loss += cost_value
                        # bar update
                        bar.update(k)
                    # bar finish
                    bar.finish()

                ########################################################################################################################
                # NN Validation
                ########################################################################################################################
                print('Epoch', epoch, 'completed out of',self.n_epochs,'loss:',epoch_loss)
                # Calcuting accuracy
                print('Calculating accuracy of the classifier based on validation data...', end=' ', flush=True)
                correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(labels_placeholder, 1))
                accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
                p_accuracy = 0
                i = i+1
                for chunk in range(self.number_of_validation_batches):
                    for v in range(len(split_list_inputs[i+chunk])-self.batch_size):
                        p_accuracy += accuracy.eval({input_placeholder:split_list_inputs[i+chunk][v: v+self.batch_size],
                                                    labels_placeholder:split_list_outputs[i+chunk][v: v+self.batch_size],
                                                    sequence_length_placeholder:split_list_lengths[i+chunk][v: v+self.batch_size]})
                accuracy_val = p_accuracy/(int(len(split_list_inputs[0])-self.batch_size)*self.number_of_validation_batches)
                print('Done')
                print('Accuracy of validation data = {}%'.format(accuracy_val*100))

                # Generating the directory for saving the classifier after training if it doesn't exist
                if not os.path.exists('latest_intents_classifier'): os.makedirs('latest_intents_classifier')

                # Saving the current session in seperate folders to be tested manually and select the best suited one
                saver.save(sess, './latest_intents_classifier/actions_mydata_3.ckpt')

                # If the epoch_loss is less than self.loss_lower_limit the training stops
                if epoch_loss<=self.loss_lower_limit:
                    print('The loss value is close to zero, exiting the training')
                    print("--- %s seconds ---" % (time.time() - start_time))
                    break
        return

if __name__ == "__main__":

    # Some OS environment variables to set for tensorflow
    os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

    # load training and validation parameters from yaml file
    config_file = '../../../../../ros/config/config_mbot_nlu_training.yaml'
    yaml_dict = yaml.load(open(config_file))['intent_train']

    # Set CUDA parameters
    if os.environ.get('CUDA_VISIBLE_DEVICES') is None:
        gpu_to_use = yaml_dict['available_gpu_index']
        print("CUDA_VISIBLE_DEVICES environment variable is not set, will try to set to use only GPU {} but may not work".format(gpu_to_use))
        os.environ['CUDA_VISIBLE_DEVICES'] = gpu_to_use

    # initiate training
    class_object = intent_training_class(yaml_dict)
    class_object.train_neural_network()

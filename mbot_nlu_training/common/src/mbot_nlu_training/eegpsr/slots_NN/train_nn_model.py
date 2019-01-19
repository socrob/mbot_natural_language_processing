#!/usr/bin/env python3

import os
import time
import yaml
import shutil
import msgpack
import msgpack_numpy
import numpy as np
import progressbar
import tensorflow as tf
from termcolor import colored
from sklearn.utils import resample
from tensorflow.contrib import rnn
start_time = time.time()


class slot_training_class():
    '''
    This class contains a set of methods used to train the slots classifier for mbot_nlu package.
    '''
    def __init__(self, yaml_dict):
        '''
        constructor
        '''
        self.available_slots = yaml_dict['available_slots']                            # list of available intents, add to list if your training data has more intents.
        self.n_steps = yaml_dict['n_steps']                                            # max n of words in the sentences
        self.n_epochs = yaml_dict['n_epochs']                                          # n epochs
        self.base_path = yaml_dict['base_path']                                        # path to dictionary and wordvector files
        self.rnn_size = yaml_dict['rnn_size']                                          # n of lstm cells in each layer
        self.n_lstm_layers = yaml_dict['n_lstm_layers']                                # n lstm layers
        self.n_examples = yaml_dict['n_examples']                                      # n of samples for training and validation
        self.embedding_size = yaml_dict['embedding_size']                              # embedding size of each wordvector
        self.forget_bias = yaml_dict['forget_bias']                                    # forget bias for lstm cell
        self.learning_rate = yaml_dict['learning_rate']                                # initial learning rate for adam optimizer
        self.loss_lower_limit = yaml_dict['loss_lower_limit']                          # used to stop the training when the loss is below this value
        self.debug = yaml_dict['debug']                                                # debug, will give lot of info about the execution if True
        self.n_parallel_iterations_bi_rnn = yaml_dict['n_parallel_iterations_bi_rnn']  # The number of iterations to run in parallel...
                                                                                       # Those operations which do not have any temporal dependency and can be run in parallel...
                                                                                       # will be. This parameter trades off time for space. default=32
        self.train_method = yaml_dict['train_method']                                  # key to activate old and the new method,
                                                                                       # old = using tf placeholder with feed_dict, new = tf data iteration
        self.use_tensorboard = yaml_dict['use_tensorboard']                            # to use TB or not
        self.n_classes = len(self.available_slots)                                     # n of slots
        self.resample_replace = yaml_dict['resample_replace']                          # to use data duplication (randomly) while shuffling and batching

        # parameters for old method
        if self.train_method=='old':
            self.batch_size = yaml_dict['old_method']['batch_size']
            self.number_of_batches = yaml_dict['old_method']['number_of_batches']     # n batches
            self.number_of_validation_batches = yaml_dict['old_method']['number_of_validation_batches'] # n validation batches
            self.n_inputs_per_step = int(self.n_examples/self.number_of_batches)

        # parameters for new method
        if self.train_method=='new':
            self.batch_size = yaml_dict['new_method']['batch_size'] # batch size
            self.q = yaml_dict['new_method']['q']                   # Percentage of sample used for testing after each training session
            self.prefetch_buffer = self.batch_size                  # prefetching inputs to memory
            self.shuffle_buffer = self.n_examples                   # input data shuffle. Value > n_samples gives uniform shuffle
            self.repeat_dataset = self.n_epochs                     # repeat the dataset n number of times
            self.steps = int(int((1-self.q)*self.n_examples)/self.batch_size) # n steps per epoch (experimental)

        # printing parameters before training
        print('Training method = {}'.format(self.train_method))

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
        with open('inputs_slot_filling', 'rb') as data_inputs_file:
            print("Importing inputs...", end=' ', flush=True)
            sentences = msgpack.load(data_inputs_file, raw=False)
            print("Done")
        with open('outputs_slot_filling', 'rb') as data_outputs_file:
            print("Importing labels...", end=' ', flush=True)
            outputs = msgpack.load(data_outputs_file, raw=False)
            print("Done")


        ########################################################################################################################
        # Processing inputs
        ########################################################################################################################
        print("Modifying input sentences...")

        # importing progressbar
        bar = progressbar.ProgressBar(max_value=len(sentences), redirect_stdout=True, end=' ')
        # preassigning the inputs variable for faster processing
        data_inputs = np.zeros((len(sentences), self.n_steps), dtype=np.int32)
        # initiating all the inputs to index of zero vector (zerowordvec_idx = dictionary['zerowordvec'])
        zerowordvec_idx = dictionary['zerowordvec']
        data_inputs[:, :] = zerowordvec_idx
        # Processing inputs
        lengths = np.zeros(len(sentences), dtype=np.int32)
        i = 0
        words_not_found_in_dic = []
        for line in sentences:
            # Initializing an empty list of Indexes
            h = []
            # Iterating each word in the line over the dictionary and appending the indexes to a list
            for k in range(len(line)):
                try:
                    idx = dictionary[line[k]]
                except:
                    idx = zerowordvec_idx
                    words_not_found_in_dic.append(line[k])
                # Appending the index(idx) of each word to the list h.
                h.append(idx)
            # appending the length of each line to the list lengths
            lengths[i] = len(line)
            # modify contents of the array
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
            print('input sentences are {}'.format(sentences[0:2]))
            print('[Vector]input sentence are {}'.format(data_inputs[0:2]))
            print('=========================================================')

        ########################################################################################################################
        # Processing labels
        ########################################################################################################################
        print("Modifying outputs...")

        # Pre assigning the data_outputs array
        data_outputs = np.zeros((self.n_examples, self.n_steps, len(self.available_slots)), dtype=np.int32)
        # Initiating all the one hot vectors to the default vector corresponding to the 'Outside' slot
        # Outside string 'O' is part of the naming convention (Begin, Inside and Outside)for classification of words (Object, Source etc) in a sentence.
        # Ref: $ROS_WORKSPACE/mbot_natural_language_processing/mbot_nlu/ros/doc/pedro_thesis.pdf
        idx_outside = self.available_slots.index('O')
        data_outputs[:, :, idx_outside] = 1
        # Initiating progress bar
        bar = progressbar.ProgressBar(max_value=len(outputs), redirect_stdout=True, end=' ')
        # Index for line wise iteration
        v = 0
        # Process outputs
        for line in outputs:
            # Index for word wise iteration
            w = 0
            for output in line:
                # find slot if it exists in available slots list
                try:
                    idx_found = self.available_slots.index(output)
                    # print('index found is ' + str(idx_found))
                except ValueError:
                    raise Exception('Could not find this output = {}  in this sentence = {} in the available list of slots'.format(output, sentences[outputs.index(line)]))
                # modify array
                data_outputs[v][w][idx_outside] = 0
                data_outputs[v][w][idx_found] = 1
                w = w + 1
            # Incrementing line index
            v = v + 1
            # Progress bar update
            bar.update(v)
        # Progress bar finished
        bar.finish()

        # debug prining
        if debug==True:
            print('Sample output data')
            print('=========================================================')
            print('output labels are {}'.format(outputs[0:2]))
            print('[Vector]output labels are {}'.format(outputs_train[0:2]))
            print('=========================================================')

        return word_vectors, data_inputs, data_outputs, lengths


    def shuffle_n_batch(self, data_inputs, data_outputs, lengths):
        '''
        shuffles and splits the data inputs for each epoch. 8 batches are used for training and 1 batch is used for validation
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

        return split_list_inputs, split_list_outputs, split_list_lengths


    def recurrent_neural_network(self, rnn_inputs, sequence_lengths):
        '''
        defining nn layers (graph in TF terms)
        '''
        # def of 1 layer of lstm
        def cell(): return tf.nn.rnn_cell.BasicLSTMCell(self.rnn_size, forget_bias=self.forget_bias)
        # initializing weights and biases for the output layer
        num_layers = self.n_lstm_layers
        layer = {'weights': tf.Variable(tf.random_normal(shape=[self.batch_size, 2*self.rnn_size, self.n_classes]), name='WEIGHTS'),
                 'biases': tf.Variable(tf.random_normal(shape=[self.n_classes]), name='BIASES')}

        # histograms for TB
        if self.use_tensorboard:
            tf.summary.histogram('weights', layer['weights'])
            tf.summary.histogram('biases', layer['biases'])

        # n layer of lstm with rnn_size number of cells for both forward and backward hidden layers.
        with tf.device('/GPU:0'):
            fw_cell = tf.nn.rnn_cell.MultiRNNCell([cell() for num in range(num_layers)], state_is_tuple=True)
            bw_cell = tf.nn.rnn_cell.MultiRNNCell([cell() for num in range(num_layers)], state_is_tuple=True)

        # building the graph while running the session (tf methods which reduces the load on the pc)
        (outputs_fw, outputs_bw), _ = tf.nn.bidirectional_dynamic_rnn(
            cell_fw=fw_cell,
            cell_bw=bw_cell,
            inputs=rnn_inputs,
            sequence_length=sequence_lengths,
            parallel_iterations=self.n_parallel_iterations_bi_rnn,
            dtype=tf.float32,
            scope='BI_DIRECTIONAL_DYNAMIC_RNN')

        # output layer modifications
        with tf.device('/GPU:0'):
            outputs = tf.concat((outputs_fw, outputs_bw), 2)
            output = tf.matmul(outputs, layer['weights']) + layer['biases']
            if self.train_method=='new': prediction = tf.reshape(output, [self.batch_size, self.n_steps, self.n_classes])
            if self.train_method=='old': prediction = tf.reshape(output, [self.n_steps, self.n_classes])
            if self.debug:
                print('RNN properties')
                print('=========================================================')
                print('fw shape = ', outputs_fw.get_shape().as_list())
                print('bw shape = ', outputs_bw.get_shape().as_list())
                print('concat shape = ', outputs.get_shape().as_list())
                print('weights shape = ', layer['weights'].get_shape().as_list())
                print('biases shape = ', layer['biases'].get_shape().as_list())
                print('=========================================================')

        return prediction


    def train_neural_network(self):

        # importing data
        word_vectors, data_inputs, data_outputs, lengths = self.import_data(debug=False)

        ########################################################################################################################
        # TF Data implementation (experimental)
        ########################################################################################################################
        # creating dataset (train and test) from input and label arrays
        if self.train_method=='new':
            print('Creating tf datasets...', end=' ', flush=True)
            # train data
            dataset_train = tf.data.Dataset.from_tensor_slices({'inputs': inputs_train, 'labels': outputs_train, 'inputs_length': lengths_train})
            shuffled_dataset_train = dataset_train.apply(tf.contrib.data.shuffle_and_repeat(buffer_size=self.shuffle_buffer, count=self.repeat_dataset, seed=self.shuffle_buffer))
            batched_dataset_train = shuffled_dataset_train.batch(self.batch_size).prefetch(buffer_size=self.prefetch_buffer)
            # test data
            dataset_test = tf.data.Dataset.from_tensor_slices({'inputs': inputs_test, 'labels': outputs_test, 'inputs_length': lengths_test})
            batched_dataset_test = dataset_test.batch(self.batch_size).prefetch(buffer_size=self.prefetch_buffer)
            # pointers to initiate train and validation set
            iterator = tf.data.Iterator.from_structure(batched_dataset_train.output_types, batched_dataset_train.output_shapes)
            # batched_dataset_train = batched_dataset_train.apply(tf.contrib.data.prefetch_to_device('/GPU:0'))
            # op to select train and test data
            training_init_op = iterator.make_initializer(batched_dataset_train)
            validation_init_op = iterator.make_initializer(batched_dataset_test)
            combined_input = iterator.get_next(name='combined_input')
            print('Done')

        ########################################################
        # TF placeholder implementation (old method)
        ########################################################
        if self.train_method=='old':
            input_placeholder = tf.placeholder(dtype=tf.int32, shape=[self.batch_size, self.n_steps], name='input_placeholder')
            labels_placeholder = tf.placeholder(dtype=tf.int32, shape=[self.batch_size*self.n_steps, self.n_classes], name='labels_placeholder')
            sequence_length_placeholder = tf.placeholder(dtype=tf.int32, shape=(None), name='inputs_length')

        # selecting inputs if method is old else new
        if self.train_method=='old':
            input_indexes = input_placeholder
            labels = labels_placeholder
            sequence_lengths = sequence_length_placeholder
        else:
            input_indexes = combined_input['inputs']
            labels = combined_input['labels']
            sequence_lengths = combined_input['inputs_length']

        ##########################################################
        # Trying to get the batch size from input so that we can use it in the input as a symbolic tensor
        ##########################################################
        # self.dim_batch = tf.shape(rnn_inputs)[0]

        # look up for embeds/wordvectors (words_index to 300 len vector)
        print('Embedding wordvectors...', end=' ', flush=True)
        embeds = tf.convert_to_tensor(word_vectors, name="embeds")
        print('Done')

        # output of the TF graph
        rnn_inputs = tf.nn.embedding_lookup(embeds, input_indexes)
        prediction = self.recurrent_neural_network(rnn_inputs, sequence_lengths)

        # defining cost
        with tf.name_scope('COST'):
            cost = tf.reduce_mean(tf.losses.sigmoid_cross_entropy(logits = prediction, multi_class_labels = labels_placeholder))
            tf.summary.scalar('cross_entropy/loss', cost)
        # defining optimizer
        with tf.name_scope('TRAIN'):
            optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(cost)

        # Defining the accuracy of the model
        with tf.name_scope('ACCURACY'):
            correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(labels, 1))
            accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
            tf.summary.scalar('train dataset accuracy', accuracy)

        # classifier saver def
        saver = tf.train.Saver()

        ########################################################################################################################
        # TB Implementation (experimental)
        ########################################################################################################################
        # tf summary for TB
        # tf.summary.text('input_text_and_labels', combined_input['inputs'])
        if self.use_tensorboard:
            merged_summary = tf.summary.merge_all()
            writer = tf.summary.FileWriter('./tf_log/validation_accuracy')

        # configuring session parameters to use only required amount of memory
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True

        print("\nStarting training...\n")
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
                # choosing steps based on old and new method
                if self.train_method=='old':
                    n_training_batches = self.number_of_batches-self.number_of_validation_batches#self.n_inputs_per_epoch
                else:
                    n_training_batches = self.steps

                # initializing training dataset
                if self.train_method=='new':
                    sess.run(training_init_op)
                else:
                    if epoch==0:
                        # first epoch shuffle and split into training and validation sets, training data shuffle only then onwards
                        # shuffling and generating training and validation batches every epoch
                        print('Splitting data inputs to batches of {} ({} for training {} for validation)...'.format(self.number_of_batches, n_training_batches, self.number_of_validation_batches ), end=' ', flush=True)
                        [split_list_inputs, split_list_outputs, split_list_lengths] = self.shuffle_n_batch(data_inputs, data_outputs, lengths)
                        print('Done')
                    else:
                        # shuffling only training batch
                        split_list_inputs[:n_training_batches], split_list_outputs[:n_training_batches], split_list_lengths[:n_training_batches] = resample(split_list_inputs[:n_training_batches], split_list_outputs[:n_training_batches], split_list_lengths[:n_training_batches], replace=False)

                # Starting training
                for training_batch_idx in range(0, n_training_batches):
                    if self.train_method=='old':
                        print('Processed batches = {}/{}'.format(training_batch_idx + 1, n_training_batches))
                        range_each_chuntraining_batch_idxs = len(split_list_inputs[training_batch_idx]) - self.batch_size
                        # progressbar
                        bar = progressbar.ProgressBar(max_value=range_each_chuntraining_batch_idxs, redirect_stdout=True, end=' ', flush=True)
                        # iterating over batches
                        for training_data_point_idx in range(range_each_chuntraining_batch_idxs):
                            epoch_x = np.array(split_list_inputs[training_batch_idx][training_data_point_idx: training_data_point_idx + self.batch_size])
                            epoch_y = np.array(split_list_outputs[training_batch_idx][training_data_point_idx])
                            inputs_length = np.array(split_list_lengths[training_batch_idx][training_data_point_idx: training_data_point_idx + self.batch_size])
                            # running optimizer and cost nodes
                            _, cost_value = sess.run([optimizer, cost], feed_dict={input_placeholder: epoch_x, labels_placeholder: epoch_y, sequence_length_placeholder: inputs_length})
                            # cumulative epoch_loss
                            epoch_loss+=cost_value
                            # printing input shapes for debug
                            if self.debug==True: print('shape of input, labels and lengths = {}, {}, {}'.format(epoch_x.shape, epoch_y.shape, inputs_length.shape))
                            bar.update(training_data_point_idx)

                            ########################################################################################################################
                            # TB Implementation (method=old)
                            ########################################################################################################################
                            if training_data_point_idx%5==0 and self.use_tensorboard:
                                summary_iter = sess.run(merged_summary, feed_dict={input_placeholder: epoch_x, labels_placeholder: epoch_y, sequence_length_placeholder: inputs_length})
                                writer.add_summary(summary_iter, training_data_point_idx)
                        bar.finish()
                    else:
                        ########################################################################################################################
                        # TB Implementation (method=new)
                        ########################################################################################################################
                        if k%5==0 and self.use_tensorboard:
                            summary_iter = sess.run(merged_summary)
                            writer.add_summary(summary_iter, k)
                        # running optimizer and cost nodes
                        _, cost_value = sess.run([optimizer, cost])
                        # printing input shapes for debug
                        if self.debug==True: print('shape of input, labels and lengths = {}, {}, {}'.format(input_indexes.get_shape().as_list(), labels.get_shape().as_list(), sequence_lengths.get_shape().as_list()))
                        # cumulative epoch_loss
                        epoch_loss+=cost_value

                print('Epoch', epoch, 'completed out of',self.n_epochs,'loss:',epoch_loss)
                ########################################################################################################################
                # NN Validation
                ########################################################################################################################
                # printing loss for every 5th batch or final batch
                p_accuracy = 0
                print('Calculating accuracy of the classifier based on validation data...', end=' ', flush=True)
                if self.train_method=='old':
                    for chunk in range(self.number_of_validation_batches):
                        for v in range(len(split_list_inputs[n_training_batches + chunk])-self.batch_size):
                            p_accuracy += accuracy.eval({input_placeholder:split_list_inputs[n_training_batches + chunk][v: v + self.batch_size],
                                                        labels_placeholder:split_list_outputs[n_training_batches + chunk][v],
                                                        sequence_length_placeholder:split_list_lengths[n_training_batches + chunk][v: v + self.batch_size]})

                    accuracy_val = p_accuracy/(int(len(split_list_inputs[0])-self.batch_size)*self.number_of_validation_batches)
                    n_training_batches += 1
                else:
                    sess.run(validation_init_op)
                    for v in range(int(int(self.q*self.n_examples)/(self.batch_size))):
                        p_accuracy += accuracy.eval()
                    accuracy_val = p_accuracy/int(int(self.q*self.n_examples)/(self.batch_size))
                print('Done')
                # adding validation accuracy to TB
                with tf.name_scope('ACCURACY'):
                    tf.summary.scalar('validation dataset accuracy', p_accuracy)
                print('Accuracy of validation data = {}%'.format((accuracy_val)*100))

                # Generating the directory for saving the classifier after training if it doesn't exist
                if not os.path.exists('latest_slots_classifier'):
                    os.makedirs('latest_slots_classifier')

                # Saving the current session in seperate folders
                saver.save(sess, './latest_slots_classifier/slots_2.ckpt')

                # Exit the training once the loss reaches near zero
                if epoch_loss<=self.loss_lower_limit:
                    print('The loss has reached the minimum value, terminating the training to save the most recent classifier.')
                    print(" --- Total time consumed to train the network = %s seconds ---" % (time.time() - start_time))
                    break
        return

if __name__ == "__main__":

    # Some OS environment variables to set for tensorflow
    # set TF log level
    os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

    # load training and validation parameters from yaml file
    yaml_dict = yaml.load(open('../../../../../ros/config/config_mbot_nlu_training.yaml'))['slots_train']

    # set GPU
    if os.environ.get('CUDA_VISIBLE_DEVICES') is None:
        gpu_to_use = yaml_dict['available_gpu_index']
        print("CUDA_VISIBLE_DEVICES environment variable is not set, will try to set to use only GPU {} but may not work".format(gpu_to_use))
        os.environ['CUDA_VISIBLE_DEVICES'] = gpu_to_use

    # initiate training
    class_object = slot_training_class(yaml_dict)
    class_object.train_neural_network()

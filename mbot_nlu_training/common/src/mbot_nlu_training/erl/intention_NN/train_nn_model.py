import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn


q = 0.2
n_examples = 150000
n_epochs = 4
embedding_size = 250
n_steps = 15    # n de palavras na frase. vai ser preciso fazer padding e organizar os batches mais ou menos por tamanhos
n_classes = 5   # n de actions
batch_size = 1 #int ( q * n_examples)
rnn_size = 250   # n of lstm hidden units
learning_rate = 0.001
gpu = False # set True for batatinha

def import_data(n_examples, n_steps):

    with open('wordvectors', 'rb') as vectors_file: #TODO: load from mbot_nlu_training/common/src/mbot_nlu_training/erl/wikipedia_vectors
        word_vectors = pickle.load(vectors_file)
        word_vectors[0] = np.zeros(250)

    with open('dictionary', 'rb') as dict_file: #TODO: load from mbot_nlu_training/common/src/mbot_nlu_training/erl/wikipedia_vectors
        dictionary = pickle.load(dict_file)

    vocab_size = len(dictionary)

    with open('inputs', 'rb') as data_inputs_file:
        sentences = pickle.load(data_inputs_file)

        lengths = []
        i = 0
        for line in sentences:
            line = line.lower()
            line = line.strip('\n')
            line = line.replace(',', '')
            line = line.rsplit(' ', -1)
            
            h = []
            
            for k in range(len(line)):
                try:
                    idx = dictionary[line[k]]
                except:
                    pass
                h.append(idx)
            lengths.append(len(line))
            for _ in range(len(line), n_steps):
                h.append(0)
            i += 1

            if i == 1:
                data_inputs = np.array(h)
            else:
                data_inputs = np.vstack([data_inputs, h])

            inputs_train = np.array(data_inputs[int(q*n_examples):])
            inputs_test = np.array(data_inputs[:int(q*n_examples)])
            lengths_train = lengths[int(q*n_examples):]
            lengths_test = lengths[: int(q*n_examples)]

    with open('outputs', 'rb') as data_outputs_file:
        outputs = pickle.load(data_outputs_file)
        v=0
        for line in outputs:
            o = []
            if line == 'motion':
                o.append([1,0,0,0,0])
            elif line == 'searching':
                o.append([0,1,0,0,0])
            elif line == 'taking':
                o.append([0,0,1,0,0])
            elif line == 'placing':
                o.append([0,0,0,1,0])
            elif line == 'bringing':
                o.append([0,0,0,0,1])
            else:
                print(line)
            v+=1
            if v == 1:
                data_outputs = np.array(o)
            else:
                data_outputs = np.vstack([data_outputs, o])
            outputs_train = np.array(data_outputs[int(q*n_examples):])
            outputs_test = np.array(data_outputs[: int(q*n_examples)])

    return [vocab_size, n_examples, inputs_train, inputs_test, outputs_train, outputs_test, lengths_train, lengths_test, word_vectors]

def recurrent_neural_network(rnn_size, n_classes, rnn_inputs, n_steps, batch_size):
    
    layer = {'weights': tf.Variable(tf.random_normal([batch_size, 2 * rnn_size, n_classes])),
             'biases': tf.Variable(tf.random_normal([n_classes]))}

    def cell():
        return  tf.nn.rnn_cell.BasicLSTMCell(rnn_size, forget_bias=1.0)

    if (gpu):
        with tf.device('/gpu:0'):
            lstm_cell_bw = tf.nn.rnn_cell.BasicLSTMCell(rnn_size, forget_bias=1.0)
            lstm_cell_fw = tf.nn.rnn_cell.BasicLSTMCell(rnn_size, forget_bias=1.0)
            layers = 2
            fw_cell = tf.nn.rnn_cell.MultiRNNCell([cell() for _ in range(layers)], state_is_tuple=True)
            bw_cell = tf.nn.rnn_cell.MultiRNNCell([cell() for _ in range(layers)], state_is_tuple=True)
    else:
        lstm_cell_bw = tf.nn.rnn_cell.BasicLSTMCell(rnn_size, forget_bias=1.0)
        lstm_cell_fw = tf.nn.rnn_cell.BasicLSTMCell(rnn_size, forget_bias=1.0)
        layers = 2
        fw_cell = tf.nn.rnn_cell.MultiRNNCell([cell() for _ in range(layers)], state_is_tuple=True)
        bw_cell = tf.nn.rnn_cell.MultiRNNCell([cell() for _ in range(layers)], state_is_tuple=True)

    (outputs_fw, outputs_bw), _ = tf.nn.bidirectional_dynamic_rnn(fw_cell, bw_cell, rnn_inputs, sequence_length, dtype=tf.float32)

    if (gpu):
        with tf.device('/gpu:0'):
            outputs = tf.concat((outputs_fw, outputs_bw), 2)
            output = tf.matmul(outputs, layer['weights']) + layer['biases']
            index = tf.range(0, batch_size) * n_steps + (sequence_length - 1)
            flat = tf.reshape(output, [-1, n_classes])
            relevant = tf.gather(flat, index)
            prediction = tf.nn.softmax(relevant)
    else:
        outputs = tf.concat((outputs_fw, outputs_bw), 2)
        output = tf.matmul(outputs, layer['weights']) + layer['biases']
        index = tf.range(0, batch_size) * n_steps + (sequence_length - 1)
        flat = tf.reshape(output, [-1, n_classes])
        relevant = tf.gather(flat, index)
        prediction = tf.nn.softmax(relevant)

    return relevant, prediction



def train_neural_network(prediction, n_examples, batch_size, inputs_train, inputs_test, outputs_train, outputs_test,
                        lengths_train, lengths_test, word_vectors, n_epochs, learning_rate):
    

    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = prediction, labels = y))
    
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        sess.run(embeds.assign(word_vectors))

        for epoch in range(n_epochs):
            epoch_loss = 0
            
            for k in range(0, int((1-q)*n_examples)-1):
                epoch_x = np.array(inputs_train[k*batch_size: (k+1)*batch_size])

                epoch_y = np.array(outputs_train[k*batch_size: (k+1)*batch_size])

                inputs_length = np.array(lengths_train[k*batch_size: (k+1)*batch_size])
                
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y, sequence_length: inputs_length})
                
                epoch_loss += c

                if k%1000 == 0:
                    print(k)

            print('Epoch', epoch, 'completed out of',n_epochs,'loss:',epoch_loss)
            correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

            accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

            p_accuracy = 0

            for v in range(int(q*n_examples)):

                p_accuracy += accuracy.eval({x:inputs_test[v*batch_size: (v+1)*batch_size], y:outputs_test[v*batch_size: (v+1)*batch_size],
                                             sequence_length:lengths_test[v*batch_size: (v+1)*batch_size]})

            print('Accuracy, test data:', p_accuracy/(int(q*n_examples)))

            saver.save(sess, 'actions_mydata_rockin.ckpt')

    return


[vocab_size, n_examples, inputs_train, inputs_test, outputs_train,
                     outputs_test, lengths_train, lengths_test, word_vectors] = import_data(n_examples, n_steps)


x = tf.placeholder(tf.int32, [batch_size, n_steps], name='input_placeholder')
y = tf.placeholder(tf.int32, [batch_size, n_classes], name='labels_placeholder')

embeds = tf.Variable(tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0), trainable = False, name="embeds")

sequence_length = tf.placeholder(shape=(None), dtype=tf.int32, name='inputs_length')

rnn_inputs = tf.nn.embedding_lookup(embeds, x)  

pred, prediction = recurrent_neural_network(rnn_size, n_classes, rnn_inputs, n_steps, batch_size)

saver = tf.train.Saver()

train_neural_network(pred, n_examples, batch_size, inputs_train, inputs_test, outputs_train, outputs_test,
                     lengths_train, lengths_test, word_vectors, n_epochs, learning_rate)
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn


q = 0.2
n_examples = 120000
n_epochs = 16
embedding_size = 250
n_steps = 15    # n de palavras na frase. vai ser preciso fazer padding e organizar os batches mais ou menos por tamanhos
n_classes = 5    # n de ações
batch_size = 1 #int ( q * n_examples)
rnn_size = 500   # n of lstm hidden units
learning_rate = 0.0001


def import_data(n_examples, n_steps):

    with open('wordvectors', 'rb') as vectors_file:
        word_vectors = pickle.load(vectors_file)
        word_vectors[0] = np.zeros(250)

    with open('dictionary', 'rb') as dict_file:
        dictionary = pickle.load(dict_file)

    vocab_size = len(dictionary)

    with open('inputs_slot_filling', 'rb') as data_inputs_file:
        sentences = pickle.load(data_inputs_file)

        lengths = []
        i = 0
        for line in sentences:
            
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

    with open('outputs_slot_filling', 'rb') as data_outputs_file:
        outputs = pickle.load(data_outputs_file)

        v=0
        data_outputs = [[] for _ in range(n_examples)]
        
        for line in outputs:
            for output in line:
                if 'Btheme' in output:                                    
                    data_outputs[v].append([1,0,0,0,0])
                elif 'Itheme' in output:                                  
                    data_outputs[v].append([0,1,0,0,0])
                elif 'Bground' in output:                            
                    data_outputs[v].append([0,0,1,0,0])
                elif 'Iground' in output:                            
                    data_outputs[v].append([0,0,0,1,0])                             
                elif 'O' in output:                                         
                    data_outputs[v].append([0,0,0,0,1])
                else:
                    print(output)
                    print('error')
            for _ in range(len(data_outputs[v]), n_steps):
                data_outputs[v].append([0,0,0,0,1])
            v+=1

        outputs_train = np.array(data_outputs[int(q*n_examples):])
        outputs_test = np.array(data_outputs[: int(q*n_examples)])

    return [vocab_size, n_examples, inputs_train, inputs_test, outputs_train, outputs_test, lengths_train, lengths_test, word_vectors]

def recurrent_neural_network(rnn_size, n_classes, rnn_inputs, n_steps):
    
    layer = {'weights': tf.Variable(tf.random_normal([batch_size , 2 * rnn_size, n_classes])),
             'biases': tf.Variable(tf.random_normal([n_classes]))}

    with tf.device('/gpu:3'):

        lstm_cell_bw = rnn.LSTMCell(rnn_size)
        lstm_cell_fw = rnn.LSTMCell(rnn_size)

    (outputs_fw, outputs_bw), _ = tf.nn.bidirectional_dynamic_rnn(lstm_cell_fw, lstm_cell_bw, rnn_inputs, sequence_length, dtype=tf.float32)

        outputs = tf.concat((outputs_fw, outputs_bw), 2)

        output = tf.matmul(outputs, layer['weights']) + layer['biases']

        prediction = tf.reshape(output, [n_steps, n_classes])

    return prediction



def train_neural_network(prediction, n_examples, batch_size, inputs_train, inputs_test, outputs_train, outputs_test,
                        lengths_train, lengths_test, word_vectors, n_epochs, learning_rate, q):
    

    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = prediction, labels = y))
    
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        sess.run(embeds.assign(word_vectors))

        for epoch in range(n_epochs):
            epoch_loss = 0

            for k in range(0, int((1-q)*n_examples)-1):
                c = 0

                epoch_x = np.array(inputs_train[k*batch_size: (k+1)*batch_size])
                
                epoch_y = np.array(outputs_train[k])
                
                inputs_length = np.array(lengths_train[k*batch_size: (k+1)*batch_size])
                
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y, sequence_length: inputs_length})
                
                epoch_loss += c

                if k%1000 == 0:
                    print(k)

            print('Epoch', epoch, 'completed out of',n_epochs,'loss:',epoch_loss)

            correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

            accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

            #print('Accuracy:',accuracy.eval({x:inputs_train[: batch_size], y:outputs_train[: batch_size], 
            #                                    sequence_length:lengths_train[:batch_size]}))
            #print('Accuracy:',accuracy.eval({x:inputs_test, y:outputs_test, sequence_length:lengths_test}))

            p_accuracy = 0
      #      y_true = []
       #     y_pred = []

            for v in range(int(q*n_examples)):

                p_accuracy += accuracy.eval({x:inputs_test[v*batch_size: (v+1)*batch_size], y:outputs_test[v],
                                             sequence_length:lengths_test[v*batch_size: (v+1)*batch_size]})

           # for v in range(int(0.001*n_examples)):

#                y_true.append(np.argmax(y.eval({x:inputs_test[v*batch_size: (v+1)*batch_size], y:outputs_test[v],
 #                                            sequence_length:lengths_test[v*batch_size: (v+1)*batch_size]}), 1).tolist())
  #              y_pred.append(np.argmax(prediction.eval({x:inputs_test[v*batch_size: (v+1)*batch_size],
   #                                          sequence_length:lengths_test[v*batch_size: (v+1)*batch_size]}), 1).tolist())

            #wtf = np.argmax(prediction.eval({x:np.array([[370, 1, 8355, 7, 1, 46584, 0, 0, 0, 0, 0, 0, 0]]),
            #    y:np.array([[0,0,0,0,0,0,0,0,0,1], [0,0,0,0,0,0,0,0,0,1], [1,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,1],
            #     [0,0,0,0,0,0,0,0,0,1], [0,0,0,0,1,0,0,0,0,1], [0,0,0,0,0,0,0,0,0,1], [0,0,0,0,0,0,0,0,0,1],
            #     [0,0,0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,1]]),
            #                             sequence_length:np.array([6])}), 1).tolist()

            print('Accuracy, test data:', p_accuracy/(q*n_examples))

    #        print(y_true)

     #       print(y_pred)

            #print('wtf', wtf)
            saver.save(sess, 'slots_rockin_searching.ckpt')

    return


[vocab_size, n_examples, inputs_train, inputs_test, outputs_train,
                     outputs_test, lengths_train, lengths_test, word_vectors] = import_data(n_examples, n_steps)


x = tf.placeholder(tf.int32, [batch_size, n_steps], name='input_placeholder')
y = tf.placeholder(tf.int32, [batch_size*n_steps, n_classes], name='labels_placeholder')

embeds = tf.Variable(tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0), trainable = False, name="embeds")

sequence_length = tf.placeholder(shape=(None), dtype=tf.int32, name='inputs_length')

rnn_inputs = tf.nn.embedding_lookup(embeds, x)  

prediction = recurrent_neural_network(rnn_size, n_classes, rnn_inputs, n_steps)

saver = tf.train.Saver()

train_neural_network(prediction, n_examples, batch_size, inputs_train, inputs_test, outputs_train, outputs_test,
                     lengths_train, lengths_test, word_vectors, n_epochs, learning_rate, q)
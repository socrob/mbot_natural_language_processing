wordvectors is the feature vectors, words transformed into vectors

dictionary has all words and their correspondent id's

wordvectors was generated using word2vec in batatinha (took days)

Downloads a dump file wikipedia, 2014 (20 GB) (basically a lot of words) but this can
be obtained from the internet also.

Then transforms all this words into feature vectors.

training time takes some hours in batatinha (4-5)

it takes some time to see the first console output log (print)

you dont need to run the file till the end, stop at 10 e -5

Please go to [Pedro's thesis](http://dante.isr.tecnico.ulisboa.pt/socrob_at_home/isr_monarch_robot/blob/kinetic/mbot_hri/mbot_nlu/ros/doc/pedro_thesis.pdf)
page 20, section word embeddings to understand this part, is basically to reduce vector dimension and gain meaning.

In the example given in the thesis: guide me to the bedroom and guide me to the bathroom, the surrounding words are the same.
Therefore the (valid) assumption here is that they will have similar meaning.

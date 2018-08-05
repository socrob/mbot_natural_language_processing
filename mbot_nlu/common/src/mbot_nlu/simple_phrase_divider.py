def divide_sentence_in_phrases(s):
    return s.replace(' ,',',').replace(', and ',' and ').replace('and ', ', ').split(', ')

if __name__ == '__main__':
    # test one sentence
    print divide_sentence_in_phrases('go to the kitchen , bring me a coke, and look for mithun')

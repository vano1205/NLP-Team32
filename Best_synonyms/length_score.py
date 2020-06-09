import os
import sys
import syllables
sys.path.append(os.path.abspath("pairkoreng"))

import pairkoreng

def get_sentences():
    f = open("pairkoreng/pair_result.txt", "r")
    inputs = f.read().split('\n')
    kor_sentences = []
    eng_sentences = []

    for input_ in inputs:
        tuples = list(input_)
        
        kor_sentence = ''
        for tup in tuples:
            if kor_sentence == '':
                kor_sentence += str(tuple(tup)[0])
            else:
                kor_sentence += ' ' + str(tuple(tup)[0])
        kor_sentences.append(kor_sentence)
        
        eng_sentence = ''
        for tup in tuples:
            if eng_sentence == '':
                eng_sentence += str(tuple(tup)[1])
            else:
                eng_sentence += ' ' + str(tuple(tup)[1])
        eng_sentences.append(eng_sentence)
    f.close()
    return (kor_sentences, eng_sentences)

sent = '[(1, 1)]'
print(tuple(list(sent)[0]))
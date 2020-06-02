from nltk import *
import sys
import os
sys.path.append(os.path.abspath("../pairkoreng"))
sys.path.append(os.path.abspath("../phoneme2viseme"))
sys.path.append(os.path.abspath("../korean2phoneme"))
sys.path.append(os.path.abspath("../sent_similarity"))
import pairkoreng
from korean2phoneme import kor2phon
from phoneme2viseme import pho2vi

import similarity
from similarity import compare_viseme

#import Evaluate_updated
#from Evaluate_updated import viseme_set_similarity

from nltk.corpus import wordnet as wn
from nltk.corpus import cmudict
import itertools

result_pair = pairkoreng.result_pair
viseme_list = []
best_viseme_list = []
cmu_d = cmudict.dict()


#Get visemes of a word
def viseme(word, language):
    """returns a list of visemes for the word in function call"""
    if (language == "en"):
        try:
            #special case
            if (word.lower() == "o.k."):
                phons=cmu_d["o"][0]+cmu_d["k"][0]
                return pho2vi(phons)

            cpt1 = word.count("_")
            cpt2 = word.count("-")

            if cpt1 == 0 and cpt2 == 0:
                #normal case
                return pho2vi(cmu_d[(word.strip()).lower()][0])

            #If multiple words separated by '_' like "out_of_order"
            #decompose in multiple words and treat
            phons=[]
            if cpt1 == 1:
                w1, w2 = word.split('_', 2)
                phons= cmu_d[(w1.strip()).lower()][0] + cmu_d[(w2.strip()).lower()][0]
            if cpt1 == 2:
                w1, w2, w3 = word.split('_', 3)
                phon=cmu_d[(w1.strip()).lower()][0]+cmu_d[(w2.strip()).lower()][0]+cmu_d[(w3.strip()).lower()][0]
            if cpt1 == 3:
                w1, w2, w3, w4 = word.split('_', 4)
                phon=cmu_d[(w1.strip()).lower()][0]+cmu_d[(w2.strip()).lower()][0]+cmu_d[(w3.strip()).lower()][0]+cmu_d[(w4.strip()).lower()][0]

            #If multiple words separated by '-' like "good-for-nothing"
            #decompose in multiple words and treat
            if cpt2 == 1:
                w1, w2 = word.split('-', 2)
                phons= cmu_d[(w1.strip()).lower()][0] + cmu_d[(w2.strip()).lower()][0]
            if cpt2 == 2:
                w1, w2, w3 = word.split('-', 3)
                phon=cmu_d[(w1.strip()).lower()][0]+cmu_d[(w2.strip()).lower()][0]+cmu_d[(w3.strip()).lower()][0]
            if cpt2 == 3:
                w1, w2, w3, w4 = word.split('-', 4)
                phon=cmu_d[(w1.strip()).lower()][0]+cmu_d[(w2.strip()).lower()][0]+cmu_d[(w3.strip()).lower()][0]+cmu_d[(w4.strip()).lower()][0]

            return pho2vi(phons)

        except:
            #print(word, "is not in cmudict\n")
            return ""
    else:
        return pho2vi(kor2phon(word))
        return " "

#Create a list of visemes in the same format as the list of English-Korean word pairs
def set_viseme_list(pair_list):
    """returns a list of visemes for all words in the list of Korean-English pairs"""
    list = []

    for pair in pair_list:
        tmp=[]
        i=0
        while i < len(pair):
            ko_vis = viseme(pair[i][0][0], "ko")
            eng_vis = []
            for w in pair[i][1]:
                eng_vis.append(viseme(w, "en"))
            i=i+1
            tmp.append((ko_vis, eng_vis))
        list.append(tmp)
    return list

#Find best synonym in terms of visemes similarity
def best_word(eng_word, eng_vis, ko_vis):
    """returns a synonym of eng_word with better visemes similarity (if it exists)"""

    cur = compare_viseme(eng_vis, ko_vis)
    res_word = eng_word
    res_vis = eng_vis

    for syn in wn.synsets(eng_word):
        for l in syn.lemmas():
            if l.name() != eng_word and l.name() != "group_a" and l.name() != "information_technology":
                #compare english synonym and korean word
                vis = viseme(l.name(), "en")
                tmp = compare_viseme(vis, ko_vis)
                if tmp > cur:
                    cur = tmp
                    res_word = l.name()
                    res_vis = vis

    return (res_word, res_vis)


viseme_list = set_viseme_list(result_pair)
best_viseme_list = viseme_list
best_pairs = result_pair


b=0
for word_pair, vis_pair in zip(result_pair, viseme_list):
    i=0
    while i < len(word_pair):
        j=0
        while j < len(word_pair[i][1]):
            if (len(vis_pair[i][0]) != 0):
                best = best_word(word_pair[i][1][j], vis_pair[i][1][j], vis_pair[i][0])
            #if a better synonym is found:
            if best[0] != word_pair[i][1][j]:
                best_pairs[b][i][1][j] = best[0]
                best_viseme_list[b][i][1][j] = best[1]
            j=j+1
        i=i+1
    b=b+1


f1 = open('best_pairs.txt','w')
for pair in best_pairs:
   f1.write(str(pair)+'\n')
f1.close()

f2 = open('best_viseme_pairs.txt','w')
for pair in best_viseme_list:
   f2.write(str(pair)+'\n')
f2.close()

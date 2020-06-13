from nltk import *
import sys
import os
import syllables
from nltk.tokenize import word_tokenize
from os import path

sys.path.append(os.path.abspath("pairkoreng"))
sys.path.append(os.path.abspath("phoneme2viseme"))
sys.path.append(os.path.abspath("korean2phoneme"))
sys.path.append(os.path.abspath("sent_similarity"))

import pairkoreng
from korean2phoneme import kor2phon
from phoneme2viseme import pho2vi
from similarity import compare_viseme
from similarity import sents_scores
import file_visemes
import scores_Death_Bell
#import Evaluate_updated
#from Evaluate_updated import viseme_set_similarity

from nltk.corpus import wordnet as wn
from nltk.corpus import cmudict
import itertools

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
        #print(tmp)
        list.append(tmp)
    f = open('Best_synonyms/file_visemes.py','w')
    f.write('list='+str(list))
    f.close()
    return list

#Find best synonym in terms of visemes similarity
def best_word(eng_word, eng_vis, ko_vis):
    """returns a synonym of eng_word with better visemes similarity (if it exists)"""

    cur = compare_viseme(eng_vis, ko_vis)
    res_word = eng_word
    res_vis = eng_vis

    for syn in wn.synsets(eng_word):
        for l in syn.lemmas():
            if l.name() != eng_word and (l.name()).find("type_") == -1 and  (l.name()).find("group_") == -1 and l.name() != "information_technology":
                #compare english synonym and korean word
                vis = viseme(l.name(), "en")
                tmp = compare_viseme(vis, ko_vis)
                if tmp > cur:
                    cur = tmp
                    res_word = (l.name()).replace('_', ' ')
                    res_vis = vis

    return (res_word, res_vis)


def getScores(word_pair, vis_pair):
    """returns a sorted list of the scores of each word in a sentence"""
    scores=[]
    #get the scores for all word pairs in a sentence
    i=0
    while i < len(word_pair):
        j=0
        while j < len(word_pair[i][1]):
            if (len(vis_pair[i][0]) != 0):
                scores.append((word_pair[i], word_pair[i][1][j], compare_viseme(vis_pair[i][1][j], vis_pair[i][0])))
            j=j+1
        i=i+1

    #sort by minimum score
    sorted_scores = sorted(scores, key=lambda tup: tup[2])
    return sorted_scores


def sents_viseme(visemes):
    """returns a tuple with the visemes of the korean sentence and the english sentence"""
    ko_vis=''
    eng_vis=''
    for vis in visemes:
        #korean visemes
        for v in vis[0]:
            ko_vis=ko_vis+v
        i = 0
        while i < len(vis[1]):
            l = vis[1][i]
            for elt in l:
                for v in elt:
                    eng_vis=eng_vis+v
            i=i+1
    return (ko_vis, eng_vis)



#def find_best_syn(file_en, file_ko, pairs):
result_pair = pairkoreng.result_pair
viseme_list = []
best_viseme_list = []

viseme_list = file_visemes.list
#viseme_list = set_viseme_list(result_pair)

best_viseme_list = viseme_list
best_pairs = result_pair


score_list=[]
sent_score=0
#sent_score_list=sents_scores("Import_script/Death Bell_ENG.txt", "Import_script/Death Bell_KOR.txt")
#takes too long so just read file
sent_score_list=scores_Death_Bell.list

s=0
b=0
for word_pair, vis_pair in zip(result_pair, viseme_list):
    sent_score = sent_score_list[s]
    s=s+1
    i=0
    p=0
    #scores for all word pairs in a sentence, sorted by min score
    pair_scores = getScores(word_pair, vis_pair)
    #if similarity score of the sentence < threshold
    while (sent_score < 0.6) and (p < len(pair_scores)):
        pair=pair_scores[p]
        exit=0
        i=0
        while i < len(word_pair):#sentence length
            j=0
            while j < len(word_pair[i][1]):#length of eng part of the pair
                #find the word to change that has the current lowest score
                if (word_pair[i][1][j] == pair[1]):
                    if (len(vis_pair[i][0]) != 0):
                        best = best_word(word_pair[i][1][j], vis_pair[i][1][j], vis_pair[i][0])
                        #if a better synonym is found:
                        if best[0] != word_pair[i][1][j]:
                            best_pairs[b][i][1][j] = best[0]
                            best_viseme_list[b][i][1][j] = best[1]
                        exit=1
                        break
                j=j+1
            if (exit == 1):
                break
            i=i+1
        #evaluate sentence score
        tuple=sents_viseme(best_viseme_list[b])
        sent_ko=tuple[0]
        sent_eng=tuple[1]
        sent_score = compare_viseme(sent_ko, sent_eng)
        p=p+1

    b=b+1

#b=0
#for word_pair, vis_pair in zip(result_pair, viseme_list):
#    i=0
#    while i < len(word_pair):
#        j=0
#        while j < len(word_pair[i][1]):
#            if (len(vis_pair[i][0]) != 0):
#                best = best_word(word_pair[i][1][j], vis_pair[i][1][j], vis_pair[i][0])
#            #if a better synonym is found:
#            if best[0] != word_pair[i][1][j]:
#                best_pairs[b][i][1][j] = best[0]
#                best_viseme_list[b][i][1][j] = best[1]
#            j=j+1
#        i=i+1
#    b=b+1

f1 = open('Best_synonyms/best_pairs.txt','w')
for pair in best_pairs:
   f1.write(str(pair)+'\n')
f1.close()

f2 = open('Best_synonyms/best_viseme_pairs.txt','w')
for pair in best_viseme_list:
   f2.write(str(pair)+'\n')
f2.close()


#f1 = open("Best_synonyms/best_pairs_%s_%s.txt" %
#        (file_en.split('/')[-1].split('.')[0], file_ko.split('/')[-1].split('.')[0])
#        , 'w',newline="")
#for pair in best_pairs:
#    f1.write(str(pair)+'\n')
#f1.close()

#f2 = open("Best_synonyms/best_viseme_pairs_%s_%s.txt" %
#        (file_en.split('/')[-1].split('.')[0], file_ko.split('/')[-1].split('.')[0])
#        , 'w',newline="")
#for pair in best_viseme_list:
#    f2.write(str(pair)+'\n')
#f2.close()

    #return best_pairs

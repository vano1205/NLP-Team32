from nltk import *
import sys
import os
import syllables
from nltk.tokenize import word_tokenize
from os import path
import re

sys.path.append(os.path.abspath("pairkoreng"))
sys.path.append(os.path.abspath("phoneme2viseme"))
sys.path.append(os.path.abspath("korean2phoneme"))
sys.path.append(os.path.abspath("sent_similarity"))
sys.path.append(os.path.abspath("Import_Script"))


from korean2phoneme import kor2phon
from phoneme2viseme import pho2vi
from similarity import compare_viseme
from similarity import sents_scores
import visemes_TheHost
import visemes_Death_Bell
import visemes_Bleak_Night
import visemes_WarOfFlower
import visemes_Find_Kim
import scores_Death_Bell
import scores_Bleak_Night
import scores_Find_Kim
import scores_TheHost
import scores_WarOfFlower

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
def set_viseme_list(pair_list, file):
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
    #f = open('Best_synonyms/file_visemes.py','w')
    file = file.replace(' ', '_')
    f = open('Best_synonyms/visemes_' + file.split('/')[-1].replace('_ENG.txt', '.py'), 'w')
    f.write('list='+str(list))
    f.close()
    return list

#Find best synonym in terms of visemes similarity
def best_word(eng_word, eng_vis, ko_vis,tag_info):
    """returns a synonym of eng_word with better visemes similarity (if it exists)"""

    cur = compare_viseme(eng_vis, ko_vis)
    res_word = eng_word
    res_vis = eng_vis

    for syn in wn.synsets(eng_word):
        for l in syn.lemmas():
            if l.name() != eng_word and (l.name()).find("type_") == -1 and  (l.name()).find("group_") == -1 and l.name() != "information_technology" and syn.pos()==tag_info:
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

def pos_convert(pos_info):
    if 'VB' in pos_info:
        return 'v'
    elif 'JJ' in pos_info:
        return 'a'
    elif 'NN' in pos_info:
        return 'n'
    elif 'RB' in pos_info:
        return 'r'
    else:
        return -1

def find_best_syn(file_en, file_ko, pairs):
    f_ENG = open(file_en, "r")

    #result_pair = pairkoreng.result_pair
    result_pair = pairs
    viseme_list = []
    best_viseme_list = []

#    viseme_list = set_viseme_list(result_pair, file_en)
#    sent_score_list=sents_scores(file_en, file_ko)

    #takes too long so just read file
    if ("Death" in file_en):
        viseme_list = visemes_Death_Bell.list
        sent_score_list=scores_Death_Bell.list
    elif ("Bleak" in file_en):
        viseme_list = visemes_Bleak_Night.list
        sent_score_list=scores_Bleak_Night.list
    elif ("Find_Kim" in file_en):
        viseme_list = visemes_Find_Kim.list
        sent_score_list=scores_Find_Kim.list
    elif("TheHost" in file_en):
        viseme_list = visemes_TheHost.list
        sent_score_list=scores_TheHost.list
    else:
        viseme_list = visemes_WarOfFlower.list
        sent_score_list=scores_WarOfFlower.list


    best_viseme_list = viseme_list
    best_pairs = result_pair


    score_list=[]
    sent_score=0


    sentences_ENG=[]
    for line in f_ENG:
        sentences_ENG.append(line)

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
        pattern='[^\w\s]'
        resub_ENG=re.sub(pattern=pattern,repl='',string=sentences_ENG[b])
        token_ENG = word_tokenize(resub_ENG)
        # eng_token = word_tokenize(eng_script[b])
        eng_tagged = pos_tag(token_ENG)

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
                            wordindex=0
                            for iter in range(i):
                                wordindex+=len(word_pair[iter][1])
                            wordindex+=j
                            converted=pos_convert(eng_tagged[wordindex][1])
                            if converted==-1:
                                break
                            best = best_word(word_pair[i][1][j], vis_pair[i][1][j], vis_pair[i][0],converted)
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

    f_ENG.close()

    f1 = open("Best_synonyms/best_pairs_%s_%s.txt" %
            (file_en.split('/')[-1].split('.')[0], file_ko.split('/')[-1].split('.')[0])
            , 'w',newline="")
    for pair in best_pairs:
        f1.write(str(pair)+'\n')
    f1.close()

    f2 = open("Best_synonyms/best_viseme_pairs_%s_%s.txt" %
            (file_en.split('/')[-1].split('.')[0], file_ko.split('/')[-1].split('.')[0])
            , 'w',newline="")
    for pair in best_viseme_list:
        f2.write(str(pair)+'\n')
    f2.close()

    return best_pairs


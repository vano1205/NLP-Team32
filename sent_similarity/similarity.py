import math
import nltk
import korean2phoneme
import phoneme2viseme
from kor_letterdivide import divideKoreanLetter
from g2pk import G2p
import re
import csv
from os import path

g2p = G2p()
# 21 visemes based on realistic interaction with social robots via facial expressions ...
visemes = {'1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'}

# the width and height of mouth shape, 5 stages each
mouthshape_width = {'1': 4, '2': 2, '3': 3, '4': 5, '5': 1, '6': 5, '7': 1, '8': 1, '9': 3, 'a': 2,
                    'b': 5, 'c': 2, 'd': 1, 'e': 4, 'f': 4, 'g': 3, 'h': 4, 'i': 4, 'j': 5, 'k': 4, 'l': 2}
mouthshape_height = {'1': 2, '2': 4, '3': 3, '4': 3, '5': 2, '6': 3, '7': 1, '8': 3, '9': 4, 'a': 4,
                     'b': 4, 'c': 1, 'd': 2, 'e': 3, 'f': 2, 'g': 3, 'h': 2, 'i': 1, 'j': 3, 'k': 3, 'l': 1}
# script2 viseme file
def eng2viseme(filename):
    cmu_d = nltk.corpus.cmudict.dict()
    f = open(filename, 'r')
    outfile = filename.split('/')[-1].replace('.txt', '_viseme.txt')
    if path.exists(outfile):
        out = open(outfile, 'r')
        return [s.split() for s in out.readlines()]
    out = open(outfile, 'w', encoding='utf8')
    result = []
    for l in f.readlines():
        sent_pho = []
        for w in l.split():
            phon = cmu_d.get(re.sub(r'[^a-z]+$', '', w.lower()), [None])[0]
            if phon == None:
                # sent_pho.append('None')
                pass
            else:
                sent_pho.extend(phoneme2viseme.pho2vi(phon))
        out.write("%s\n" % ' '.join(sent_pho))
        result.append(sent_pho)
    f.close()
    out.close()
    return result

def kor2viseme(filename):
    f = open(filename, 'r', encoding='utf8')
    outfile = filename.split('/')[-1].replace('.txt', '_viseme.txt')
    if path.exists(outfile):
        out = open(outfile, 'r')
        return [s.split() for s in out.readlines()]
    out = open(outfile, 'w', encoding='utf8')
    result = []
    for l in f.readlines():
        sent_pho = []
        for w in l.split(): # w is each word in a line
            entry = divideKoreanLetter(g2p(w))
            for letter in entry:
                if len(letter) == 1:
                    continue
                for i in range(3):
                    atom = letter[i]
                    if atom in korean2phoneme.kor2ipa_consonant:
                        if i == 2:
                            index = 1
                        elif i == 0:
                            index = 0
                        letter[i] = korean2phoneme.kor2ipa_consonant[atom][index]
                    elif atom in korean2phoneme.kor2ipa_vowels:
                        letter[i] = korean2phoneme.kor2ipa_vowels[atom]
                sent_pho.extend(phoneme2viseme.pho2vi(letter))
        out.write("%s\n" % ' '.join(sent_pho))
        result.append(sent_pho)
    f.close()
    out.close()
    return result

# giving length penalty
def compare_viseme(l_vis1, l_vis2):
    vis1_height = [mouthshape_height[i] for i in l_vis1]
    vis1_width = [mouthshape_width[i] for i in l_vis1]
    vis2_height = [mouthshape_height[i] for i in l_vis2]
    vis2_width = [mouthshape_width[i] for i in l_vis2]
    diff = 0
    shorter = min(len(l_vis1), len(l_vis2))
    if shorter == 0:
        return 0
    # diff = sum of Euclidean distance for each visemes
    for i in range(shorter):
        height_diff = (vis1_height[i] - vis2_height[i]) ** 2
        width_diff = (vis1_width[i] - vis2_width[i]) ** 2
        diff += math.sqrt(height_diff + width_diff)

    # longest = sum of longest Euclidean distance for n visemes
    longest = math.sqrt(((5 - 1) ** 2) * 2) * shorter
    # similarity = 1 - diff / longest, if the visemes are all same, it is 1. if it is totally different, it is 0.
    similarity = 1 - diff / longest
    # length penalty = ratio**0.5
    if len(l_vis1) == shorter:
        ratio = len(l_vis1) / len(l_vis2)
    else:
        ratio = len(l_vis2) / len(l_vis1)
    length_penalty = ratio ** 0.5
    # score = length_penalty * similarity.
    score = length_penalty * similarity
    return score

def compare_file(filename_en, filename_ko):
    enfile = open(filename_en, 'r', encoding='utf8')
    ev_sents = eng2viseme(filename_en) # english text file to list of list of viseme
    kofile = open(filename_ko, 'r', encoding='utf8')
    kv_sents = kor2viseme(filename_ko) # korean text file to list of list of viseme
    outfile = open('comp_%s_%s.csv' %
                   (filename_en.split('/')[-1].split('.')[0], filename_ko.split('/')[-1].split('.')[0]),
                   'w', newline='', encoding='utf-8-sig')
    csvwriter = csv.writer(outfile)
    sents_en = enfile.readlines() # english text file to list
    sents_ko = kofile.readlines() # korean text file to list
    for i in range(min(len(sents_en), len(sents_ko))):
        score = compare_viseme(kv_sents[i], ev_sents[i])
        csvwriter.writerow([sents_ko[i].strip('\n'), sents_en[i].strip('\n'), "%f" % score])


print("test for 'cake' and '케이크'",
      compare_viseme(['k', '4', 'k'], ['k', '1', '6', 'k', '6']))
print("test for 'english' and '영어'",
      compare_viseme(['6', 'k', 'k', 'e', '1', 'j', 'j'], ['6', '4', 'k', '4']))
print("test for 'korea' and '고려'",
      compare_viseme(['k', '3', 'd', '6', '1'], ['k', '8', 'j', '6', '4']))
print("test for 'dream' and '꿈'",
      compare_viseme(['j', 'd', '6', 'l'], ['k', '7', 'l']))
print("test for 'mango' and '망고'",
      compare_viseme(['l', '1', 'k', 'k', '8'], ['l', '2', 'k', 'k', '8']))
print("test for 'desk' and '책상'",
      compare_viseme(['j', '4', 'f', 'k'], ['g', '1', 'k', 'f', '2', 'k']))
# print(compare_viseme(['k', '4'], ['k', 'k']))
# print(compare_viseme(['k', '4','k','4'], ['k', 'k','k','k']))
compare_file("../Import_script/Death Bell_ENG.txt", "../Import_script/Death Bell_KOR.txt")

# matching length
def compare_viseme2(l_vis1, l_vis2):
    pass

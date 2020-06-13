import math
import nltk
import sys
import os
import chardet
from g2p_en import G2p as G2p_en

sys.path.append(os.path.abspath("korean2phoneme"))
sys.path.append(os.path.abspath("phoneme2viseme"))
from kor_letterdivide import divideKoreanLetter
from korean2phoneme import kor2ipa_consonant, kor2ipa_vowels
import phoneme2viseme

from g2pk import G2p
import re
import csv
from os import path
from pprint import pprint

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
    g2p_en = G2p_en()
    cmu_d = nltk.corpus.cmudict.dict()
    f = open(filename, 'r')

    outfile = 'sent_similarity/' + filename.split('/')[-1].replace('.txt', '_viseme.txt')

    if path.exists(outfile):
        out = open(outfile, 'r')
        return [s.split() for s in out.readlines()]
    out = open(outfile, 'w', encoding='utf8')
    result = []
    for l in f.readlines():
        sent_pho = []
        for w in l.split():
            phon = cmu_d.get(re.sub(r'[^a-z]+', '', w.lower()), [None])[0]
            if phon == None:
                phon = g2p_en(re.sub(r'[^a-z]+', '', w.lower()))
                sent_pho.extend(phoneme2viseme.pho2vi(phon))
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
    outfile = 'sent_similarity/' + filename.split('/')[-1].replace('.txt', '_viseme.txt')

    if path.exists(outfile):
        out = open(outfile, 'r')
        return [s.split() for s in out.readlines()]
    out = open(outfile, 'w', encoding='utf8')
    result = []
    for l in f.readlines():
        sent_pho = []
        for w in l.split():  # w is each word in a line
            entry = divideKoreanLetter(g2p(w))
            for letter in entry:
                if len(letter) == 1:
                    continue
                for i in range(3):
                    atom = letter[i]
                    if atom in kor2ipa_consonant:
                        if i == 2:
                            index = 1
                        elif i == 0:
                            index = 0
                        letter[i] = kor2ipa_consonant[atom][index]
                    elif atom in kor2ipa_vowels:
                        letter[i] = kor2ipa_vowels[atom]
                sent_pho.extend(phoneme2viseme.pho2vi(letter))
        out.write("%s\n" % ' '.join(sent_pho))
        result.append(sent_pho)
    f.close()
    out.close()
    return result


# giving length penalty
def compare_viseme(l_vis1, l_vis2):
    if len(l_vis1) == 0 and len(l_vis2) == 0:
        return 1
    if len(l_vis1) == 0 or len(l_vis2) == 0:
        return 0
    vis1_height = [mouthshape_height[i] for i in l_vis1]
    vis1_width = [mouthshape_width[i] for i in l_vis1]
    vis2_height = [mouthshape_height[i] for i in l_vis2]
    vis2_width = [mouthshape_width[i] for i in l_vis2]
    diff = 0
    shorter = min(len(l_vis1), len(l_vis2))
    # diff = sum of Euclidean distance for each visemes
    for i in range(shorter):
        height_diff = (vis1_height[i] - vis2_height[i]) ** 2
        width_diff = (vis1_width[i] - vis2_width[i]) ** 2
        diff += math.sqrt(height_diff + width_diff)

    # longest = sum of longest Euclidean distance for n visemes
    longest = math.sqrt(((5 - 1) ** 2) + (4 - 1) ** 2) * shorter
    # similarity = 1 - diff / longest, if the visemes are all same, it is 1. if it is totally different, it is 0.
    similarity = 1 - diff / longest
    # length penalty = ratio**0.5
    if len(l_vis1) == shorter:
        ratio = len(l_vis1) / len(l_vis2)
    else:
        ratio = len(l_vis2) / len(l_vis1)
    length_penalty = math.sqrt(ratio)
    score = length_penalty * similarity
    return score


# match length of two viseme list to lcm of two length
def compare_viseme2(l_vis1, l_vis2):
    # calculate least common multiple
    if len(l_vis1) == 0 and len(l_vis2) == 0:
        return 1
    if len(l_vis1) == 0 or len(l_vis2) == 0:
        return 0
    a = len(l_vis1)
    b = len(l_vis2)
    lcm = max(a, b)
    while True:
        if lcm % a == 0 and lcm % b == 0:
            break
        lcm += 1
    l_vis1_s = []
    l_vis2_s = []
    for vis in l_vis1:
        l_vis1_s += [vis] * (lcm // a)
    for vis in l_vis2:
        l_vis2_s += [vis] * (lcm // b)

    vis1_height = [mouthshape_height[i] for i in l_vis1_s]
    vis1_width = [mouthshape_width[i] for i in l_vis1_s]
    vis2_height = [mouthshape_height[i] for i in l_vis2_s]
    vis2_width = [mouthshape_width[i] for i in l_vis2_s]
    diff = 0

    # diff = sum of Euclidean distance for each visemes
    for i in range(lcm):
        height_diff = (vis1_height[i] - vis2_height[i]) ** 2
        width_diff = (vis1_width[i] - vis2_width[i]) ** 2
        diff += math.sqrt(height_diff + width_diff)

    # longest = sum of longest Euclidean distance for n visemes
    longest = math.sqrt(((5 - 1) ** 2 + (4 - 1) ** 2)) * lcm
    # similarity = 1 - diff / longest, if the visemes are all same, it is 1. if it is totally different, it is 0.
    similarity = 1 - diff / longest
    # length penalty = ratio**0.5
    if len(l_vis1) < len(l_vis2):
        ratio = len(l_vis1) / len(l_vis2)
    else:
        ratio = len(l_vis2) / len(l_vis1)
    length_penalty = ratio ** 0
    score = length_penalty * similarity
    return score


def compare_viseme3(l_vis1, l_vis2):
    if len(l_vis1) == 0 and len(l_vis2) == 0:
        return 1
    if len(l_vis1) == 0 or len(l_vis2) == 0:
        return 0

    la = len(l_vis1)
    lb = len(l_vis2)
    vis1_height = [mouthshape_height[i] for i in l_vis1]
    vis1_width = [mouthshape_width[i] for i in l_vis1]
    vis2_height = [mouthshape_height[i] for i in l_vis2]
    vis2_width = [mouthshape_width[i] for i in l_vis2]
    d = [[0 for i in range(lb + 1)] for j in range(la + 1)]
    dd = [[0 for i in range(lb + 1)] for j in range(la + 1)]
    for i in range(1, la + 1):
        d[i][0] = math.sqrt(vis1_height[i - 1] ** 2 + vis1_width[i - 1] ** 2)
    for i in range(1, lb + 1):
        d[0][i] = math.sqrt(vis2_height[i - 1] ** 2 + vis2_width[i - 1] ** 2)
        dd[0][i] = (vis2_height[i - 1], vis2_width[i - 1])
    for i in range(1, la + 1):
        for j in range(1, lb + 1):
            if l_vis1[i - 1] == l_vis2[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                edit_cost = math.sqrt(
                    (vis1_height[i - 1] - vis2_height[j - 1]) ** 2 + (vis1_width[i - 1] - vis2_height[j - 1]) ** 2)
                remove1_cost = math.sqrt(vis1_height[i - 1] ** 2 + vis1_width[i - 1] ** 2)
                remove2_cost = math.sqrt(vis2_height[j - 1] ** 2 + vis2_width[j - 1] ** 2)
                d[i][j] = min(d[i - 1][j - 1] + edit_cost, d[i][j - 1] + remove2_cost, d[i - 1][j - 1] + remove1_cost)
    longer = max(la, lb)
    longest = math.sqrt((5 ** 2 + 4 ** 2)) * longer
    # print(d[-1][-1], longest)
    return 1 - d[-1][-1] / longest


def compare_file(filename_en, filename_ko, out):
    enfile = open(filename_en, 'r', encoding='utf-8')
    ev_sents = eng2viseme(filename_en)  # english text file to list of list of viseme
    kofile = open(filename_ko, 'r', encoding='utf-8')
    kv_sents = kor2viseme(filename_ko)  # korean text file to list of list of viseme

    outfile = open(out, 'w', newline='', encoding='utf-8-sig')
    csvwriter = csv.writer(outfile)
    try:
        sents_en = enfile.readlines()  # english text file to list
    except:
        enfile.close()
        enfile = open(filename_en, 'r', encoding='cp949')
        sents_en = enfile.readlines()
    try:
        sents_ko = kofile.readlines()  # korean text file to list
    except:
        kofile.close()
        kofile = open(filename_en, 'r', encoding='cp949')
        sents_ko = kofile.readlines()

    csvwriter.writerow(
        ["Original(Korean)", "Basic Translation(google trans)", "comp1 score", "comp2 score", "comp3 score"])
    for i in range(min(len(sents_en), len(sents_ko))):
        print(i)
        score = compare_viseme(kv_sents[i], ev_sents[i])
        score2 = compare_viseme2(kv_sents[i], ev_sents[i])
        score3 = compare_viseme3(kv_sents[i], ev_sents[i])
        csvwriter.writerow(
            [sents_ko[i].strip('\n'), sents_en[i].strip('\n'), "%f" % score, "%f" % score2, "%f" % score3])


# print("test for 'cake' and '케이크'",
#       compare_viseme(['k', '4', 'k'], ['k', '1', '6', 'k', '6']))
# print("test2 for 'cake' and '케이크'",
#       compare_viseme2(['k', '4', 'k'], ['k', '1', '6', 'k', '6']))
# print("test3 for 'cake' and '케이크'",
#       compare_viseme3(['k', '4', 'k'], ['k', '1', '6', 'k', '6']))
# print()
#
# print("test for 'english' and '영어'",
#       compare_viseme(['6', 'k', 'k', 'e', '1', 'j', 'j'], ['6', '4', 'k', '4']))
# print("test2 for 'english' and '영어'",
#       compare_viseme2(['6', 'k', 'k', 'e', '1', 'j', 'j'], ['6', '4', 'k', '4']))
# print("test3 for 'english' and '영어'",
#       compare_viseme3(['6', 'k', 'k', 'e', '1', 'j', 'j'], ['6', '4', 'k', '4']))
# print()
#
# print("test for 'korea' and '고려'",
#       compare_viseme(['k', '3', 'd', '6', '1'], ['k', '8', 'j', '6', '4']))
# print("test2 for 'korea' and '고려'",
#       compare_viseme2(['k', '3', 'd', '6', '1'], ['k', '8', 'j', '6', '4']))
# print("test3 for 'korea' and '고려'",
#       compare_viseme3(['k', '3', 'd', '6', '1'], ['k', '8', 'j', '6', '4']))
# print()
#
# print("test for 'dream' and '꿈'",
#       compare_viseme(['j', 'd', '6', 'l'], ['k', '7', 'l']))
# print("test2 for 'dream' and '꿈'",
#       compare_viseme2(['j', 'd', '6', 'l'], ['k', '7', 'l']))
# print("test3 for 'dream' and '꿈'",
#       compare_viseme3(['j', 'd', '6', 'l'], ['k', '7', 'l']))
# print()
#
# print("test for 'mango' and '망고'",
#       compare_viseme(['l', '1', 'k', 'k', '8'], ['l', '2', 'k', 'k', '8']))
# print("test2 for 'mango' and '망고'",
#       compare_viseme2(['l', '1', 'k', 'k', '8'], ['l', '2', 'k', 'k', '8']))
# print("test3 for 'mango' and '망고'",
#       compare_viseme3(['l', '1', 'k', 'k', '8'], ['l', '2', 'k', 'k', '8']))
# print()
#
# print("test for 'desk' and '책상'",
#       compare_viseme(['j', '4', 'f', 'k'], ['g', '1', 'k', 'f', '2', 'k']))
# print("test2 for 'desk' and '책상'",
#       compare_viseme2(['j', '4', 'f', 'k'], ['g', '1', 'k', 'f', '2', 'k']))
# print("test3 for 'desk' and '책상'",
#       compare_viseme3(['j', '4', 'f', 'k'], ['g', '1', 'k', 'f', '2', 'k']))
# print()
#
# print("test for '키' and 'key'",
#       compare_viseme(['k', 'i'], ['k', 'i']))
# print("test2 for '키' and 'key'",
#       compare_viseme2(['k', 'i'], ['k', 'i']))
# print("test3 for '키' and 'key'",
#       compare_viseme3(['k', 'i'], ['k', 'i']))
# print()
#
# print("test for 'ah' and 'ah ah ah ah'",
#       compare_viseme(['1'], ['1', '1', '1', '1']))
# print("test2 for 'ah' and 'ah ah ah ah'",
#       compare_viseme2(['1'], ['1', '1', '1', '1']))
# print("test3 for 'ah' and 'ah ah ah ah'",
#       compare_viseme3(['1'], ['1', '1', '1', '1']))
# print()

# compare_file("Import_script/Death Bell_ENG.txt", "Import_script/Death Bell_KOR.txt",
# "sent_similarity/DeathBell_comp_basic.csv")
# print("Death Bell complete!")
#
# compare_file("Import_script/Bleak Night_ENG.txt", "Import_script/Bleak Night_KOR.txt",
#              "sent_similarity/BleakNight_comp_basic.csv")
# print("Bleak Night complete!")
#
# compare_file("Import_script/Find_kim_ENG.txt", "Import_script/Find_Kim_KOR.txt",
#              "sent_similarity/FindKim_comp_basic.csv")
# print("Find Kim complete!")

compare_file("Import_script/TheHost_ENG.txt", "Import_script/TheHost_KOR.txt",
             "sent_similarity/TheHost_comp_basic.csv")
print("The Host complete!")

compare_file("Import_script/WarOfFlower_ENG.txt", "Import_script/WarOfFlower_KOR.txt",
             "sent_similarity/WarOfFlower_comp_basic.csv")
print("War of Flower complete!")

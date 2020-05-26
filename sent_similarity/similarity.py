import math
import nltk
import korean2phoneme
import phoneme2viseme
from kor_letterdivide import divideKoreanLetter
from g2pk import G2p
import re

g2p = G2p()
# 21 visemes based on realistic interaction with social robots via facial expressions ...
visemes = {'1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'}

# the width and height of mouth shape, 5 stages each
mouthshape_width = {'1': 4, '2': 2, '3': 3, '4': 5, '5': 1, '6': 5, '7': 1, '8': 1, '9': 3, 'a': 2,
                    'b': 5, 'c': 2, 'd': 1, 'e': 4, 'f': 4, 'g': 3, 'h': 4, 'i': 4, 'j': 5, 'k': 4, 'l': 2}
mouthshape_height = {'1': 2, '2': 4, '3': 3, '4': 3, '5': 2, '6': 3, '7': 1, '8': 3, '9': 4, 'a': 4,
                     'b': 4, 'c': 1, 'd': 2, 'e': 3, 'f': 2, 'g': 3, 'h': 2, 'i': 1, 'j': 3, 'k': 3, 'l': 1}
# script2 viseme file
cmu_d = nltk.corpus.cmudict.dict()
f = open("../Import_script/Death Bell_ENG.txt", 'r')
out = open("../sent_similarity/eng_script_viseme.txt", 'w')
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
f.close()
out.close()

# f = open("../Import_script/Death Bell_KOR.txt", 'r', encoding='utf8')
# out = open("../sent_similarity/kor_script_viseme.txt", 'w', encoding='utf8')
# for l in f.readlines():
#     sent_pho = []
#     for w in l.split(): # w is each word in a line
#         entry = divideKoreanLetter(g2p(w))
#         for letter in entry:
#             if len(letter) == 1:
#                 continue
#             for i in range(3):
#                 atom = letter[i]
#                 if atom in korean2phoneme.kor2ipa_consonant:
#                     if i == 2:
#                         index = 1
#                     elif i == 0:
#                         index = 0
#                     letter[i] = korean2phoneme.kor2ipa_consonant[atom][index]
#                 elif atom in korean2phoneme.kor2ipa_vowels:
#                     letter[i] = korean2phoneme.kor2ipa_vowels[atom]
#             sent_pho.extend(phoneme2viseme.pho2vi(letter))
#     out.write("%s\n" % ' '.join(sent_pho))
# f.close()
# out.close()

# giving length penalty
def compare_viseme(l_vis1, l_vis2):
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


# arpa2vi_dict = {'AA': '2', 'AE': '1', 'AH': '1', 'AO': '3', 'AW': '9', 'AX': '1', 'AXR': '1', 'AY': 'b',
#                 'EH': '4', 'ER': '5', 'EY': '4', 'IH': '6', 'IX': '6', 'IY': '6', 'OW': '8', 'OY': 'a',
#                 'UH': '4', 'UW': '7', 'UX': '7', 'B': 'l', 'CH': 'g', 'D': 'j', 'DH': 'h', 'DX': 'd',
#                 'EL': 'e', 'EM': 'l', 'EN': 'j', 'F': 'i', 'G': 'k', 'HH': 'c', 'JH': 'g', 'K': 'k',
#                 'L': 'e', 'M': 'l', 'N': 'j', 'NG': 'k', 'P': 'l', 'Q': 'k', 'R': 'd', 'S': 'f', 'SH': 'g',
#                 'T': 'j', 'TH': 'h', 'V': 'i', 'W': '7', 'WH': '7', 'Y': '6', 'Z': 'f', 'ZH': 'g'}
# kor2ipa_consonant = {'ㄱ' : ['g', 'g'], 'ㅋ' : ['k','ERROR'], 'ㅇ' : [' ', 'ŋ'], 'ㅎ' : ['h','ERROR'],
#                     'ㄹ' : ['l','l'], 'ㄴ': ['n','n'], 'ㄷ':['t','t͈'], 'ㅁ':['m','m'],'ㅂ':['p', 'p_'],
#                     'ㅅ':['s','ERROR'],'ㅈ':['t͡ɕ','ERROR'],'ㅊ':['t͡ɕʰ','ERROR'],'ㅌ':['tʰ','ERROR'],'ㅍ':['pʰ','ERROR'],
#                     'ㄲ':['k͈','ERROR'],'ㄸ':['t͈','ERROR'],'ㅃ':['p͈','ERROR'],'ㅆ':['s͈','ERROR'],'ㅉ':['t͈͡ɕ','ERROR']}
#
# kor2ipa_vowels = {'ㅏ': 'a', 'ㅑ': 'ja', 'ㅓ': 'ʌ', 'ㅕ': 'jʌ', 'ㅗ': 'o', 'ㅛ': 'jo',
#                    'ㅜ': 'u', 'ㅠ': 'ju', 'ㅡ': 'ɯ','ㅣ': 'i', 'ㅢ': 'ɯj', 'ㅟ': 'wi',
#                    'ㅚ': 'e', 'ㅔ': 'e', 'ㅐ': 'ɛ', 'ㅖ': 'je', 'ㅒ': 'jɛ', 'ㅘ': 'wa',
#                    'ㅙ': 'wɛ', 'ㅞ': 'we', 'ㅝ': 'wʌ'}
# ipa2vi_dict = {'g': 'k', 'k': 'k', 'k͈': 'k', 'ŋ': 'k', 'h': 'c', 'l': 'j', 'n': 'j', 't': 'j', 't͈': 'j', 'm': 'l',
#                'p': 'l', 'p_': 'l', 's': 'f', 's͈': 'f', 't͡ɕ': 'g', 't͡ɕʰ': 'g', 'tʰ': 'j', 'pʰ': 'j', 'p͈': 'j',
#                't͈͡ɕ': 'g',
#                'a': '2', 'ja': '62',
#                'ʌ': '4', 'jʌ': '64',
#                'o': '8', 'jo': '68',
#                'u': '7', 'ju': '67',
#                'ɯ': '6', 'i': '6',
#                'je': '61', 'jɛ': '61',
#                'ɯj': '6', 'wi': '76', 'wa': '72', 'wɛ': '71', 'we': '71', 'wʌ': '72',
#                'e': '1', 'ɛ': '1'}

# test for 'cake' and '케이크'
print(compare_viseme(['k', '4', 'k'], ['k', '1', '6', 'k', '6']))
# test for 'english' and '영국'
print(compare_viseme(['6', 'k', 'k', 'e', '1', 'j', 'j'], ['6', '4', 'k', 'k', '7', 'k']))
# test for 'korea' and '고려'
print(compare_viseme(['k', '3', 'd', '6', '1'], ['k', '8', 'j', '6', '4']))
# test for 'dream' and '꿈'
print(compare_viseme(['j', 'd', '6', 'l'], ['k', '7', 'l']))
# test for 'mango' and '망고'
print(compare_viseme(['l', '1', 'k', 'k', '8'], ['l', '2', 'k', 'k', '8']))
# test for 'desk' and '책상'
print(compare_viseme(['j', '4', 'f', 'k'], ['g', '1', 'k', 'f', '2', 'k']))
# print(compare_viseme(['k', '4'], ['k', 'k']))
# print(compare_viseme(['k', '4','k','4'], ['k', 'k','k','k']))


# matching length
def compare_viseme2(l_vis1, l_vis2):
    pass

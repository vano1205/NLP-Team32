# Phonemes to Viseme based on below link and polly-dg.pdf(en-US)
# https://en.wikipedia.org/wiki/ARPABET
import nltk
import re

arpabet = {'AA', 'AE', 'AH', 'AO', 'AW', 'AX', 'AXR', 'AY', 'EH', 'ER', 'EY', 'IH', 'IX', 'IY', 'OW', 'OY',
           'UH', 'UW', 'UX', 'B', 'CH', 'D', 'DH', 'DX', 'EL', 'EM', 'EN', 'F', 'G', 'HH', 'JH', 'K', 'L',
           'M', 'N', 'NG', 'P', 'Q', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'WH', 'Y', 'Z', 'ZH'}
visemes = {'p', 't', 'S', 'T', 'f', 'k', 'i', 'r', 's', 'u', '@', 'a', 'e', 'E', 'i', 'o', 'O'}
cmu2vi_dict = {'AA': 'a', 'AE': 'a', 'AH': 'E', 'AO': 'O', 'AW': 'a', 'AX': '@', 'AXR': '@', 'AY': 'a',
               'EH': 'E', 'ER': 'E', 'EY': 'e', 'IH': 'i', 'IX': 'i', 'IY': 'i', 'OW': 'o', 'OY': 'O',
               'UH': 'u', 'UW': 'u', 'UX': 'u', 'B': 'p', 'CH': 'S', 'D': 't', 'DH': 'T', 'DX': 'r',
               'EL': 'l', 'EM': 'm', 'EN': 'n', 'F': 'f', 'G': 'k', 'HH': 'k', 'JH': 'S', 'K': 'k',
               'L': 't', 'M': 'p', 'N': 't', 'NG': 'k', 'P': 'p', 'Q': 'k', 'R': 'r', 'S': 's', 'SH': 'S',
               'T': 't', 'TH': 'T', 'V': 'f', 'W': 'u', 'WH': 'u', 'Y': 'i', 'Z': 's', 'ZH': 'S'}


def cmu2vi(phoneme_list):
    """ Convert list of phoneme into list of viseme. """
    result = []
    for i in phoneme_list:
        result.append(cmu2vi_dict[re.sub("\d", "", i)])
    return result

# For testing
# cmu_d = nltk.corpus.cmudict.dict()
# entries = nltk.corpus.cmudict.entries()
# for i in entries:
#     print('word:', i[0], 'phoneme:', ' '.join(i[1]), 'visem:', ' '.join(cmu2vi(i[1])))

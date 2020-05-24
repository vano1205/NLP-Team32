# Phonemes to Viseme based on below link and polly-dg.pdf(en-US)
# https://en.wikipedia.org/wiki/ARPABET
import nltk
import re

arpabet = {'AA', 'AE', 'AH', 'AO', 'AW', 'AX', 'AXR', 'AY', 'EH', 'ER', 'EY', 'IH', 'IX', 'IY', 'OW', 'OY',
           'UH', 'UW', 'UX', 'B', 'CH', 'D', 'DH', 'DX', 'EL', 'EM', 'EN', 'F', 'G', 'HH', 'JH', 'K', 'L',
           'M', 'N', 'NG', 'P', 'Q', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'WH', 'Y', 'Z', 'ZH'}
visemes = {'p', 't', 'S', 'T', 'f', 'k', 'i', 'r', 's', 'J', 'u', '@', 'a', 'e', 'E', 'i', 'o', 'O'}
# visemes = {'1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'}
arpa2vi_dict = {'AA': 'a', 'AE': 'a', 'AH': 'E', 'AO': 'O', 'AW': 'a', 'AX': '@', 'AXR': '@', 'AY': 'a',
                'EH': 'E', 'ER': 'E', 'EY': 'e', 'IH': 'i', 'IX': 'i', 'IY': 'i', 'OW': 'o', 'OY': 'O',
                'UH': 'u', 'UW': 'u', 'UX': 'u', 'B': 'p', 'CH': 'S', 'D': 't', 'DH': 'T', 'DX': 'r',
                'EL': 'l', 'EM': 'm', 'EN': 'n', 'F': 'f', 'G': 'k', 'HH': 'k', 'JH': 'S', 'K': 'k',
                'L': 't', 'M': 'p', 'N': 't', 'NG': 'k', 'P': 'p', 'Q': 'k', 'R': 'r', 'S': 's', 'SH': 'S',
                'T': 't', 'TH': 'T', 'V': 'f', 'W': 'u', 'WH': 'u', 'Y': 'i', 'Z': 's', 'ZH': 'S'}
ipa2vi_dict = {'g': 'k', 'k': 'k', 'k͈': 'k', 'ŋ': 'k', 'h': 'k', 'l': 't', 'n': 't', 't': 't', 't͈': 't', 'm': 'p',
               'p': 'p', 'p_': 'p', 's': 's', 's͈': 's', 't͡ɕ': 'J', 't͡ɕʰ': 'J', 'tʰ': 't', 'pʰ': 'p', 'p͈': 'p',
               't͈͡ɕ': 'J',
               'a': 'a', 'ja': 'ia',
               'ʌ': 'E', 'jʌ': 'E',
               'o': 'o', 'jo': 'io',
               'u': 'u', 'ju': 'iu',
               'ɯ': 'i', 'i': 'i',
               'je': 'iE', 'jɛ': 'iE',
               'ɯj': 'i', 'wi': 'ui', 'wa': 'ua', 'wɛ': 'wE', 'we': 'wE', 'wʌ': 'ua',
               'e': 'E', 'ɛ': 'E'}

# arpa2vi_dict = {'AA': '2', 'AE': '1', 'AH': '1', 'AO': '3', 'AW': '9', 'AX': '1', 'AXR': '1', 'AY': 'b',
#                 'EH': '4', 'ER': '5', 'EY': '4', 'IH': '6', 'IX': '6', 'IY': '6', 'OW': '8', 'OY': 'a',
#                 'UH': '4', 'UW': '7', 'UX': '7', 'B': 'l', 'CH': 'g', 'D': 'j', 'DH': 'h', 'DX': 'd',
#                 'EL': 'e', 'EM': 'l', 'EN': 'j', 'F': 'i', 'G': 'k', 'HH': 'c', 'JH': 'g', 'K': 'k',
#                 'L': 'e', 'M': 'l', 'N': 'j', 'NG': 'k', 'P': 'l', 'Q': 'k', 'R': 'd', 'S': 'f', 'SH': 'g',
#                 'T': 'j', 'TH': 'h', 'V': 'i', 'W': '7', 'WH': '7', 'Y': '6', 'Z': 'f', 'ZH': 'g'}
#
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
pho2vi_dict = {**arpa2vi_dict, **ipa2vi_dict}


def pho2vi(phoneme_list):
    """ Convert list of phoneme into list of viseme. """
    result = []
    for i in phoneme_list:
        if i in [' ', '']:
            continue
        a = pho2vi_dict.get(re.sub('[0-9]', '', i), None)
        assert a is not None, 'unknown phoneme: %s' % i
        if len(a) != 1:
            result.extend(list(a))
        else:
            result.append(a)
    return result


# cmu_d = nltk.corpus.cmudict.dict()
# f = open("../dataset/data.txt", 'r')
# out = open("../phoneme2viseme/en_viseme.txt", 'w')
# for l in f.readlines():
#     out.write("%s\n" % pho2vi(cmu_d[l.strip()][0]))
# f.close()
# out.close()
#
# out2 = open("../phoneme2viseme/ko_viseme.txt", 'w')
# for l in ko_pho:
#     out2.write("%s\n" % pho2vi(l))
# out2.close()


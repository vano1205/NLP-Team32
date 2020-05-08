# Phonemes to Viseme based on below link and polly-dg.pdf(en-US)
# https://en.wikipedia.org/wiki/ARPABET
import nltk
import re

arpabet = {'AA', 'AE', 'AH', 'AO', 'AW', 'AX', 'AXR', 'AY', 'EH', 'ER', 'EY', 'IH', 'IX', 'IY', 'OW', 'OY',
           'UH', 'UW', 'UX', 'B', 'CH', 'D', 'DH', 'DX', 'EL', 'EM', 'EN', 'F', 'G', 'HH', 'JH', 'K', 'L',
           'M', 'N', 'NG', 'P', 'Q', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'WH', 'Y', 'Z', 'ZH'}
visemes = {'p', 't', 'S', 'T', 'f', 'k', 'i', 'r', 's', 'J', 'u', '@', 'a', 'e', 'E', 'i', 'o', 'O'}
arpa2vi_dict = {'AA': 'a', 'AE': 'a', 'AH': 'E', 'AO': 'O', 'AW': 'a', 'AX': '@', 'AXR': '@', 'AY': 'a',
               'EH': 'E', 'ER': 'E', 'EY': 'e', 'IH': 'i', 'IX': 'i', 'IY': 'i', 'OW': 'o', 'OY': 'O',
               'UH': 'u', 'UW': 'u', 'UX': 'u', 'B': 'p', 'CH': 'S', 'D': 't', 'DH': 'T', 'DX': 'r',
               'EL': 'l', 'EM': 'm', 'EN': 'n', 'F': 'f', 'G': 'k', 'HH': 'k', 'JH': 'S', 'K': 'k',
               'L': 't', 'M': 'p', 'N': 't', 'NG': 'k', 'P': 'p', 'Q': 'k', 'R': 'r', 'S': 's', 'SH': 'S',
               'T': 't', 'TH': 'T', 'V': 'f', 'W': 'u', 'WH': 'u', 'Y': 'i', 'Z': 's', 'ZH': 'S'}
ipa2vi_dict = {'g': 'k', 'k': 'k', 'k͈': 'k', 'ŋ': 'k', 'h': 'k', 'l': 't', 'n': 't', 't': 't', 't͈': 't', 'm': 'p',
               'p': 'p', 'p_': 'p', 's': 's', 's͈': 's', 't͡ɕ': 'J', 't͡ɕʰ': 'J', 'tʰ': 't', 'pʰ': 'p', 'p͈': 'p',
               't͈͡ɕ': 'J',
               'a': 'a', 'ja': '',
               'ʌ': 'E', 'jʌ': '',
               'o': 'o', 'jo': '',
               'u': 'u', 'ju': '',
               'ɯ': 'i', 'i': 'i',
               'ɯj': '', 'wi': '', 'je': '', 'jɛ': '', 'wa': '', 'wɛ': '', 'we': '', 'wʌ': '',
               'e': 'E', 'ɛ': 'E', '': ''}

def pho2vi(phoneme_list):
    """ Convert list of phoneme into list of viseme. """
    result = []
    if ipa2vi_dict.get(phoneme_list[0], None) is not None:
        for i in phoneme_list:
            if i == '':
                continue
            a = ipa2vi_dict.get(i, None)
            assert a is not None, 'unknown phoneme: %s' % i
            result.append(a)
        return result
    elif arpa2vi_dict.get(re.sub("\d", "", phoneme_list[0]), None) is not None:
        for i in phoneme_list:
            a = arpa2vi_dict.get(re.sub("\d", "", i), None)
            assert a is not None, 'unknown phoneme: %s' % i
            result.append(a)
        return result
    else:
        assert False, 'unknown phoneme: %s' % (phoneme_list[0])


# For testing
# cmu_d = nltk.corpus.cmudict.dict()
# entries = nltk.corpus.cmudict.entries()
# for i in entries[1200:1210]:
#     print('word:', i[0], 'phoneme:', ' '.join(i[1]), 'visem:', ' '.join(pho2vi(i[1])))
# kor2ipa_consonant = {'ㄱ': ['g', 'g'], 'ㅋ': ['k', 'ERROR'], 'ㅇ': ['', 'ŋ'], 'ㅎ': ['h', 'ERROR'],
#                      'ㄹ': ['l', 'l'], 'ㄴ': ['n', 'n'], 'ㄷ': ['t', 't͈'], 'ㅁ': ['m', 'm'], 'ㅂ': ['p', 'p_'],
#                      'ㅅ': ['s', 'ERROR'], 'ㅈ': ['t͡ɕ', 'ERROR'], 'ㅊ': ['t͡ɕʰ', 'ERROR'], 'ㅌ': ['tʰ', 'ERROR'],
#                      'ㅍ': ['pʰ', 'ERROR'],
#                      'ㄲ': ['k͈', 'ERROR'], 'ㄸ': ['t͈', 'ERROR'], 'ㅃ': ['p͈', 'ERROR'], 'ㅆ': ['s͈', 'ERROR'],
#                      'ㅉ': ['t͈͡ɕ', 'ERROR']}
#
# kor2ipa_vowels = {'ㅏ': 'a', 'ㅑ': 'ja', 'ㅓ': 'ʌ', 'ㅕ': 'jʌ', 'ㅗ': 'o', 'ㅛ': 'jo',
#                   'ㅜ': 'u', 'ㅠ': 'ju', 'ㅡ': 'ɯ', 'ㅣ': 'i', 'ㅢ': 'ɯj', 'ㅟ': 'wi',
#                   'ㅚ': 'e', 'ㅔ': 'e', 'ㅐ': 'ɛ', 'ㅖ': 'je', 'ㅒ': 'jɛ', 'ㅘ': 'wa',
#                   'ㅙ': 'wɛ', 'ㅞ': 'we', 'ㅝ': 'wʌ'}
#
# for k in kor2ipa_vowels.values():
#     print(k, pho2vi([k]))
#
# for a, b in kor2ipa_consonant.values():
#     if a != 'ERROR':
#         print(a, pho2vi([a]))
#     if b != 'ERROR':
#         print(b, pho2vi([b]))

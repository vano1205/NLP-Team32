from fryme import divideKoreanLetter
from g2pk import G2p
# import kor_data.txt

consonants = ['k', 'k͈', 'n', 't', 't͈', 'r', 'l', 'm', 'p', 'p͈', 's', 's͈', 
            'ŋ', 't͡ɕ', 't͈͡ɕ', 't͡ɕʰ', 'kʰ', 'tʰ', 'pʰ', 'h', 'j', 'w', 'ɰ']

vowels = ['a', 'ʌ', 'ɛ', 'o', 'u', 'ɯ', 'i']

f = open('kor_data.txt', 'r')
words = open("kor_data.txt").read().split('\n')
f = open('kor_data.txt', 'r')
words = open("kor_data.txt").read().split('\n')
for word in words:
    pass
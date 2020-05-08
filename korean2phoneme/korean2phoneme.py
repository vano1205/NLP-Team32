from kor_letterdivide import divideKoreanLetter
from g2pk import G2p

resultlist=[]
g2p = G2p()
consonants = ['k', 'k͈', 'n', 't', 't͈', 'r', 'l', 'm', 'p', 'p͈', 's', 's͈', 
            'ŋ', 't͡ɕ', 't͈͡ɕ', 't͡ɕʰ', 'kʰ', 'tʰ', 'pʰ', 'h', 'j', 'w', 'ɰ']

vowels = ['a', 'ʌ', 'ɛ', 'o', 'u', 'ɯ', 'i']

f = open('kor_data.txt', 'r')
words = f.read().split('\n')
for word in words:
    entry=divideKoreanLetter(g2p(word))
    resultlist.append(entry)
    print(resultlist)

f.close()
from kor_letterdivide import divideKoreanLetter
from g2pk import G2p


# 7종성법에 의거하여 ㄱㄴㄷㄹㅁㅂㅇ 이외의 자음은 받침으로 올 수 없다. -> ERROR 처리
# first element is for consonant at upper part of the letter
# second element is for consonant at lower part of the letter
kor2ipa_consonant = {'ㄱ' : ['g', 'g'], 'ㅋ' : ['k','ERROR'], 'ㅇ' : [' ', 'ŋ'], 'ㅎ' : ['h','ERROR'],
                    'ㄹ' : ['l','l'], 'ㄴ': ['n','n'], 'ㄷ':['t','t͈'], 'ㅁ':['m','m'],'ㅂ':['p', 'p_'],
                    'ㅅ':['s','ERROR'],'ㅈ':['t͡ɕ','ERROR'],'ㅊ':['t͡ɕʰ','ERROR'],'ㅌ':['tʰ','ERROR'],'ㅍ':['pʰ','ERROR'],
                    'ㄲ':['k͈','ERROR'],'ㄸ':['t͈','ERROR'],'ㅃ':['p͈','ERROR'],'ㅆ':['s͈','ERROR'],'ㅉ':['t͈͡ɕ','ERROR']}

kor2ipa_vowels = {'ㅏ': 'a', 'ㅑ': 'ja', 'ㅓ': 'ʌ', 'ㅕ': 'jʌ', 'ㅗ': 'o', 'ㅛ': 'jo',
                   'ㅜ': 'u', 'ㅠ': 'ju', 'ㅡ': 'ɯ','ㅣ': 'i', 'ㅢ': 'ɯj', 'ㅟ': 'wi',
                   'ㅚ': 'e', 'ㅔ': 'e', 'ㅐ': 'ɛ', 'ㅖ': 'je', 'ㅒ': 'jɛ', 'ㅘ': 'wa',
                   'ㅙ': 'wɛ', 'ㅞ': 'we', 'ㅝ': 'wʌ'}

resultlist=[]
g2p = G2p()

def kor2phon(word):
    # entry is one word
    entry=divideKoreanLetter(g2p(word))
    # space ignored in a word
    for letter in entry:
        if len(letter)==1:
            continue
        for i in range(3):
            atom=letter[i]
            if atom in kor2ipa_consonant:
                if i==2:
                    index=1
                elif i==0:
                    index=0
                letter[i]=kor2ipa_consonant[atom][index]
            elif atom in kor2ipa_vowels:
                letter[i]=kor2ipa_vowels[atom]
    list_=[]
    for d2 in entry:
        if len(d2) is 3:
            list_.extend(d2)
    return list_

kor_data = open('dataset/kor_data.txt', 'r', encoding='utf8')
korean2phoneme = open('korean2phoneme/korean2phoneme.txt','w', encoding='utf8')

words = kor_data.read().split('\n')
kor_data.close()
for word in words:
    entry=kor2phon(word)
    korean2phoneme.write(str(entry)+'\n')

korean2phoneme.close()

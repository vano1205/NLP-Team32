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

f = open('kor_data.txt', 'r')
words = f.read().split('\n')
for word in words:
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
    resultlist.append(entry)

res = []
for d1 in resultlist:
    list_ = []
    for d2 in d1:
        if len(d2) is 3:
            list_.extend(d2)
    # while ' ' in list_:
    #     list_.remove(' ')
    res.append(list_)
print(res)
print(res[29])

f.close()
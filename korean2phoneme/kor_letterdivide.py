# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

consonants = ['k', 'k͈', 'n', 't', 't͈', 'r', 'l', 'm', 'p', 'p͈', 's', 's͈', 
            'ŋ', 't͡ɕ', 't͈͡ɕ', 't͡ɕʰ', 'kʰ', 'tʰ', 'pʰ', 'h', 'j', 'w', 'ɰ', 'p_']

vowels = ['a', 'ʌ', 'ɛ', 'o', 'u', 'ɯ', 'i']

def divideKoreanLetter(korean_word):
    r_lst = []
    for w in list(korean_word.strip()):
        ## 영어인 경우 구분해서 작성함. 
        if '가'<=w<='힣':
            ## 588개 마다 초성이 바뀜. 
            ch1 = (ord(w) - ord('가'))//588
            ## 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
        else:
            r_lst.append([w])
    return r_lst

# 7종성법에 의거하여 ㄱㄴㄷㄹㅁㅂㅇ 이외의 자음은 받침으로 올 수 없다. -> ERROR 처리
# first element is for consonant at upper part of the letter
# second element is for consonant at lower part of the letter
kor2ipa_consonant = {'ㄱ' : ['g', 'g'], 'ㅋ' : ['k','ERROR'], 'ㅇ' : ['', 'ŋ'], 'ㅎ' : ['h','ERROR'],
                    'ㄹ' : ['l','l'], 'ㄴ': ['n','n'], 'ㄷ':['t','t͈'], 'ㅁ':['m','m'],'ㅂ':['p', 'p_'],
                    'ㅅ':['s','ERROR'],'ㅈ':['t͡ɕ','ERROR'],'ㅊ':['t͡ɕʰ','ERROR'],'ㅌ':['tʰ','ERROR'],'ㅍ':['pʰ','ERROR'],
                    'ㄲ':['k͈','ERROR'],'ㄸ':['t͈','ERROR'],'ㅃ':['p͈','ERROR'],'ㅆ':['s͈','ERROR'],'ㅉ':['t͈͡ɕ','ERROR']}

kor2ipa_vowels = {'ㅏ': 'a', 'ㅑ': 'ja', 'ㅓ': 'ʌ', 'ㅕ': 'jʌ', 'ㅗ': 'o', 'ㅛ': 'jo',
                   'ㅜ': 'u', 'ㅠ': 'ju', 'ㅡ': 'ɯ','ㅣ': 'i', 'ㅢ': 'ɯj', 'ㅟ': 'wi',
                   'ㅚ': 'e', 'ㅔ': 'e', 'ㅐ': 'ɛ', 'ㅖ': 'je', 'ㅒ': 'jɛ', 'ㅘ': 'wa',
                   'ㅙ': 'wɛ', 'ㅞ': 'we', 'ㅝ': 'wʌ'}
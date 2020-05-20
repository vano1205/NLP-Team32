from nltk.tokenize import sent_tokenize, word_tokenize
import syllables

f_KOR = open("Import_script/Death Bell_KOR.txt", "r")
f_ENG = open("Import_script/Death Bell_ENG.txt", "r")

sentences_KOR=[]
sentences_ENG=[]

for line in f_KOR:
    sentences_KOR.append(line)

for line in f_ENG:
    sentences_ENG.append(line)

# sentences_KOR = sent_tokenize(f_KOR.read())
# sentences_ENG = sent_tokenize(f_ENG.read())

assert (len(sentences_ENG) == len(sentences_KOR))

pairs = [[]]

for iter in range(len(sentences_ENG)):
    token_KOR = word_tokenize(sentences_KOR[iter])
    token_ENG = word_tokenize(sentences_ENG[iter])
    pair_num = min(len(token_KOR),len(token_ENG))
    print(token_KOR)
    
    if len(token_KOR) == 1 or len(token_ENG) == 1:
        pairs[iter].append(token_KOR,token_ENG)
    
    elif len(token_KOR) == len(token_ENG):
        
        # Each token gets a single word, both in KOR and ENG
        for iter2 in range(len(token_KOR)):
            pairs[iter].append(([token_KOR[iter2]], [token_ENG[iter2]]))
            
    else:
        if pair_num == len(token_KOR):
            standard = token_KOR
            compare = token_ENG
        else:
            standard = token_ENG
            compare = token_KOR

        standard_syllable_cnt = []
        compare_syllable_cnt = []

        for standword in standard:
            syllable_num=syllables.estimate(standword)
            standard_syllable_cnt.append(syllable_num)

        for cmpword in compare:
            syllable_num=syllables.estimate(cmpword)
            compare_syllable_cnt.append(syllable_num)

        expected = [0.0]*len(standard)
        bitmap = []
        
        for iter3 in range(len(standard_syllable_cnt)):
            temp1 = standard_syllable_cnt[iter3]/sum(standard_syllable_cnt)
            expected[iter3] = sum(compare_syllable_cnt)*temp1

        
        for iter4 in range(len(expected)):
            save_ptr = 0
            
            while round(expected[iter4]) > compare_syllable_cnt[save_ptr]:
                if save_ptr < len(compare)-(len(standard)-len(bitmap)):
                    break
                save_ptr += 1
            
            bitmap[iter4] = save_ptr
        
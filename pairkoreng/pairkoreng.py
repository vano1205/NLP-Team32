from nltk.tokenize import sent_tokenize, word_tokenize
import syllables
import re

def print_paired(stan = [], comp = [], bitmap = []):
    print_list = []
    
    for iter5 in range(len(stan)):
        word_num = bitmap[iter5]
        pointer = sum(bitmap[:iter5])
        print_list.append((stan[iter5], comp[pointer: pointer+word_num]))
    
    for a, b in print_list:
        print (a+' / '+" ".join(b), end=", ")

f_KOR = open("Import_script/Death Bell_KOR.txt", "r")
f_ENG = open("Import_script/Death Bell_ENG.txt", "r")

f_result = open("pairkoreng/pair_result.txt", 'w',newline="")
result_pair=[]

sentences_KOR=[]
sentences_ENG=[]

for line in f_KOR:
    sentences_KOR.append(line)

for line in f_ENG:
    sentences_ENG.append(line)

# sentences_KOR = sent_tokenize(f_KOR.read())
# sentences_ENG = sent_tokenize(f_ENG.read())

assert (len(sentences_ENG) == len(sentences_KOR))

for iter in range(len(sentences_ENG)):
    alpha_KOR=[]
    alpha_ENG=[]

    pattern='[^\w\s]'

    #print(sentences_ENG[iter])
    resub_KOR=re.sub(pattern=pattern,repl='',string=sentences_KOR[iter])
    resub_ENG=re.sub(pattern=pattern,repl='',string=sentences_ENG[iter])
    token_KOR = word_tokenize(resub_KOR)
    token_ENG = word_tokenize(resub_ENG)

    for koreanword in token_KOR:
        alpha_KOR.append(koreanword)
    
    for englishword in token_ENG:
        alpha_ENG.append(englishword)

    pair_num = min(len(alpha_KOR),len(alpha_ENG))

    if (len(alpha_KOR) == 1) or (len(alpha_ENG) == 1):
        pair = (alpha_KOR,alpha_ENG)
        result_pair.append([pair])

    elif len(alpha_KOR) == len(alpha_ENG):
        pair=[]
        # Each token gets a single word, both in KOR and ENG
        for iter2 in range(len(alpha_KOR)):
            pair.append(([alpha_KOR[iter2]], [alpha_ENG[iter2]]))
        result_pair.append(pair)
        
    else:
        korean_syllable_cnt=[]
        english_syllable_cnt=[]
        standard_syllable_cnt = []
        compare_syllable_cnt = []
        
        for koreanword in alpha_KOR:
            syllable_num=len(koreanword)
            korean_syllable_cnt.append(syllable_num)
        
        for englishword in alpha_ENG:
            syllable_num=syllables.estimate(englishword)
            english_syllable_cnt.append(syllable_num)

        if pair_num == len(alpha_KOR):
            standard = alpha_KOR
            compare = alpha_ENG
            standard_syllable_cnt=korean_syllable_cnt
            compare_syllable_cnt=english_syllable_cnt
        else:
            standard = alpha_ENG
            compare = alpha_KOR
            standard_syllable_cnt=english_syllable_cnt
            compare_syllable_cnt=korean_syllable_cnt


        expected = [0.0]*len(standard)
        bitmap = []
        
        for iter3 in range(len(standard_syllable_cnt)):
            temp1 = standard_syllable_cnt[iter3]/sum(standard_syllable_cnt)
            expected[iter3] = sum(compare_syllable_cnt)*temp1

        
        save_ptr = 0
        for iter4 in range(len(expected)):
            bitmap.append(0)
            old_save_ptr = save_ptr
            
            while True:
                
                c1 = len(compare)-save_ptr
                c2 = len(standard)-len(bitmap)-1
                save_ptr += 1
                bitmap[iter4] = bitmap[iter4] + 1
                
                if c1 == c2 + 2:
                    break
                
                # print('save ptr: ', save_ptr)
                # print('c1, c2: ', c1, c2)
                minus_current = abs(round(expected[iter4])-sum(compare_syllable_cnt[old_save_ptr: save_ptr]))
                if save_ptr <= len(compare)-1:    
                    minus_future = abs(round(expected[iter4])-sum(compare_syllable_cnt[old_save_ptr: save_ptr+1]))
                else:
                    break
                if not minus_future < minus_current:
                    break
                
        bitmap[iter4] = len(compare)-sum(bitmap[:iter4])
        #print_paired(standard, compare, bitmap)
                
        base=0
        pair_list=[]
    
        for i in range(len(standard)):
            if standard==alpha_KOR:
                standard_pair=([standard[i]],compare[base:base+bitmap[i]])
            else:
                standard_pair=(compare[base:base+bitmap[i]],[standard[i]])
            pair_list.append(standard_pair)
            base+=bitmap[i]
        result_pair.append(pair_list)


for pair in result_pair:
    f_result.write(str(pair)+'\n')

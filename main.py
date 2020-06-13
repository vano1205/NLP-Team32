import sys
import os

sys.path.append(os.path.abspath("Best_synonyms"))
sys.path.append(os.path.abspath("sent_similarity"))

rom similarity import compare_file
import best_synonyms
#import pairkoreng
#from best_synonyms import best_synonyms
#from pairkoreng import pairkoreng

#file_en_1 ="Import_script/Death Bell_ENG.txt"
#file_ko_1 ="Import_script/Death Bell_KOR.txt"

#file_en_2 ="Import_script/Bleak Night_ENG.txt"
#file_ko_2 ="Import_script/Bleak Night_KOR.txt"

#file_en_3 ="Import_script/Bleak Night_ENG.txt"
#file_ko_3 ="Import_script/Bleak Night_KOR.txt"

#pairs = best_synonyms.best_pairs

#for i in range(1,3):
#    if i == 1:
#        word_pairs = pairkoreng.pair_words(file_en_1, file_ko_1)
#        pairs = best_synonyms.find_best_syn(file_en_1, file_ko_1, word_pairs)
#        filename = "Results/Death_Bell_translation.txt"
#    else:
#        word_pairs = pairkoreng.pair_words(file_en_2, file_ko_2)
#        pairs = best_synonyms.find_best_syn(file_en_2, file_ko_2, word_pairs)
#        filename = "Results/Bleak_Night_translation.txt"

#    f = open(filename,'w')

pairs = best_synonyms.best_pairs


f=open("Results/Death_Bell_translation_method2.txt", 'w')
for pair in pairs:
    i=0
    sent=''
    while i < len(pair):
        j=0
        while j < len(pair[i][1]):
            if sent != '':
                sent = sent+' '+pair[i][1][j]
            else:#first word, no space before
                sent = pair[i][1][j]
            j=j+1
        i=i+1
    f.write(sent+'\n')

f.close()

compare_file("Results/Death_Bell_translation_method2.txt", "Import_script/Death Bell_KOR.txt")

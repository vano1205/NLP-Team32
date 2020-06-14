import sys
import os

sys.path.append(os.path.abspath("Best_synonyms"))
sys.path.append(os.path.abspath("sent_similarity"))

from similarity import compare_file
from best_synonyms import find_best_syn
from pairkoreng import pair_words

file_en_1 ="Import_script/Death Bell_ENG.txt"
file_ko_1 ="Import_script/Death Bell_KOR.txt"

file_en_2 ="Import_script/Bleak Night_ENG.txt"
file_ko_2 ="Import_script/Bleak Night_KOR.txt"

file_en_3 ="Import_script/Find_Kim_ENG.txt"
file_ko_3 ="Import_script/Find_Kim_KOR.txt"

file_en_4 ="Import_script/TheHost_ENG.txt"
file_ko_4 ="Import_script/TheHost_KOR.txt"

file_en_5 ="Import_script/WarOfFlower_ENG.txt"
file_ko_5 ="Import_script/WarOfFlower_KOR.txt"


def writeTranslation(filename, pairs):
    f = open(filename,'w')
    for pair in pairs:
        i=0
        sent=''
        while i < len(pair):
            j=0
            while j < len(pair[i][1]):
                if sent != '':
                    sent = sent+' '+pair[i][1][j]
                else:
                    sent = pair[i][1][j]
                j=j+1
            i=i+1
        f.write(sent+'\n')
    f.close()

for i in range(1,6):
    if i == 1:
        word_pairs = pair_words(file_en_1, file_ko_1)
        pairs = find_best_syn(file_en_1, file_ko_1, word_pairs)
        filename = "Results/Death_Bell_translation.txt"
        writeTranslation(filename, pairs)
        compare_file(filename, file_ko_1, "sent_similarity/DeathBell_comp_trans.csv")
        print("Death Bell done")
    elif i == 2:
        word_pairs = pair_words(file_en_2, file_ko_2)
        pairs = find_best_syn(file_en_2, file_ko_2, word_pairs)
        filename = "Results/Bleak_Night_translation.txt"
        writeTranslation(filename, pairs)
        compare_file(filename, file_ko_2, "sent_similarity/BleakNight_comp_trans.csv")
        print("Bleak Night done")
    elif i == 3:
        word_pairs = pair_words(file_en_3, file_ko_3)
        pairs = find_best_syn(file_en_3, file_ko_3, word_pairs)
        filename = "Results/Find_Kim_translation.txt"
        writeTranslation(filename, pairs)
        compare_file(filename, file_ko_3, "sent_similarity/FindKim_comp_trans.csv")
        print("Find Kim done")
    elif i == 4:
        word_pairs = pair_words(file_en_4, file_ko_4)
        pairs = find_best_syn(file_en_4, file_ko_4, word_pairs)
        filename = "Results/TheHost_translation.txt"
        writeTranslation(filename, pairs)
        compare_file(filename, file_ko_4, "sent_similarity/TheHost_comp_trans.csv")
        print("The Host done")
    elif i == 5:
        word_pairs = pair_words(file_en_5, file_ko_5)
        pairs = find_best_syn(file_en_5, file_ko_5, word_pairs)
        filename = "Results/WarOfFlower_translation.txt"
        writeTranslation(filename, pairs)
        compare_file(filename, file_ko_5, "sent_similarity/WarOfFlower_comp_trans.csv")
        print("War of Flower done")


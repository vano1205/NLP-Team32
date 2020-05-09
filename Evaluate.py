#import korean2phoneme
from phoneme2viseme import phoneme2viseme

en_word = open("dataset/data.txt", 'r') # Import english word set
kr_word = open("dataset/kor_data.txt", 'r', encoding='UTF8') # Import korean word set
en_f = open("phoneme2viseme/en_viseme.txt", 'r') # Viseme result from english word
kr_f = open("phoneme2viseme/ko_viseme.txt", 'r') # Viseme result from trnaslated korean word
eval_f = open("Evaluation.txt", 'w') # Similarity result
all_visemes = phoneme2viseme.visemes

e_word = [] # Original english words are stored
k_word = [] # Translated korean words are stored
for ews in en_word.readlines():
    e_word.append(ews[:-1])
for kws in kr_word.readlines():
    k_word.append(kws[:-1])

english_viseme = [] # Viseme array each original english word
korean_viseme = [] # Viseme array each translated korean word

for ev_set in en_f.readlines():
    str_elem = ev_set[:-1]
    only_visemes = []
    for c in str_elem:
        if c in all_visemes:
            only_visemes.append(c)
    english_viseme.append(only_visemes)
    
for kv_set in kr_f.readlines():
    str_elem = kv_set[:-1]
    only_visemes = []
    for c in str_elem:
        if c in all_visemes:
            only_visemes.append(c)
    korean_viseme.append(only_visemes)

# Calculate similarity between two viseme sets E, K
# Referenced from 'Syntactic Clustering of the Web' in evaluate/SRC-TN-1997-015.pdf
def viseme_set_similarity(E, K):
    vis_word_E = ''.join(E)
    vis_word_K = ''.join(K)
    shingle_len = 2
    shingle_E = []
    shingle_K = []
    
    for i in range(len(vis_word_E)-(shingle_len-1)):
        shingle_E.append(''.join(vis_word_E[i:i+shingle_len]))
    for j in range(len(vis_word_K)-(shingle_len-1)):
        shingle_K.append(''.join(vis_word_K[j:j+shingle_len]))
    
    intersection = [w for w in shingle_E if w in shingle_K]
    union = set(shingle_E+shingle_K)

    resemblance = len(intersection) / len(union) * 100
    return resemblance

# Save result to Evaluation.txt
for i in range(len(english_viseme)):
    score = viseme_set_similarity(english_viseme[i], korean_viseme[i])
    data = "%s(%s) | %s(%s) -> %f\n" %(e_word[i], english_viseme[i], k_word[i], korean_viseme[i], score)
    eval_f.write(data)
    #print(score)

en_word.close()
kr_word.close()
en_f.close()
kr_f.close()
eval_f.close()
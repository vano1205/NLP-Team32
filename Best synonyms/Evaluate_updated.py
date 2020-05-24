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

    if (len(union) == 0):
        return 0
    resemblance = len(intersection) / len(union) * 100
    return resemblance

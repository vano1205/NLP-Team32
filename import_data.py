import nltk
import googletrans
from googletrans import Translator

eng=[]
kor=[]
engkor=[]

translator = Translator()

f=open('dataset/data.txt', 'r')
data = f.readlines()
for word in data:
    eng.append(word.rstrip())
    tmp = translator.translate(word.rstrip(), src='en', dest='ko')
    kor.append(tmp.text)
    engkor.append((word.rstrip(), tmp.text))
f.close()

#i=0
#while i < len(eng) :
#    print(eng[i])
#    print(kor[i])
#    print(engkor[i])
#    i=i+1

#with open('kor_data.txt', "w", encoding="utf-8") as f:
#    for elt in kor :
#        f.write(elt+'\n')
#f.close()

#if googletrans doesn't work, read kor_data.txt file

#f=open('kor_data.txt', 'r')
#data = f.readlines()
#i=0
#for word in data:
#    kor.append(word.rstrip())
#    engkor.append((eng[i], word.rstrip()))
#    i=i+1
#f.close()

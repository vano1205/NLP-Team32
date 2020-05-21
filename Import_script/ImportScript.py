#pip install docx2txt
#pip install --upgrade google-cloud-translate

import docx2txt
from google.cloud import translate_v2 as translate
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "My First Project-39d227f44795.json"
text = docx2txt.process("Import_script/Death Bell Script.docx")
#file_one = open("Death Bell_KJE.txt", 'w')
file_two = open("Import_script/Death Bell_KOR.txt", 'w', encoding='UTF8')
file_three = open("Import_script/Death Bell_ENG.txt", 'w')
client = translate.Client()

content = []
for line in text.splitlines():
  if line != '':
    if ":" in line:
        only_sen = line.split(':')[1]
        new_sen = ""
        checker = 1
        for i in range(len(only_sen)):
            if only_sen[i]=="(":
                checker = 0
            if checker == 1:
                new_sen += only_sen[i]
            if only_sen[i]==")":
                checker = 1
        while new_sen.startswith(' '):
            new_sen = new_sen[1:]
        content.append(new_sen)

for diag in content[2:]:
    if diag == '':
        continue
    file_two.write(diag+'\n')
    result = client.translate(diag, target_language='en', format_="text")
    file_three.write(result['translatedText']+'\n')
    tojap = client.translate(diag, target_language='ja', format_="text")
    toen = client.translate(tojap['translatedText'], target_language='en', format_="text")
    #file_one.write(toen['translatedText']+'\n')

#file_one.close()
file_two.close()
file_three.close()
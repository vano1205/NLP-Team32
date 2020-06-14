# NLP-Team32
Translation of movie scripts for automatic lip synchronization

#### Install Packages
* pip install -r requirements.txt
* https://brew.sh
* KoNLPy: https://konlpy.org/en/latest/install/
* Mecab: https://cleancode-ws.tistory.com/97

#### Run program
* python main.py

#### Makefile commands
* make all : runs the program
* make clean : clean all files produced by main.py

#### Dataset
* "Import_script" folder contains 5 Korean scripts from the movies Bleak Night, Death Bell, Find Kim, War of Flower and The Host.
They are translated into English with ImportScript.py

#### Results
* "Results" folder contains files with the translation done by our algorithm for the 5 scripts.
* In "sent_similarity" folder, the csv files show the scores of the translation for each sentence.

#### References
* https://pdfs.semanticscholar.org/9a0b/ac4d9fd4f3f913419fd8d5dd33c39b74cd49.pdf
* https://en.wikipedia.org/wiki/Korean_phonology
* https://en.wikipedia.org/wiki/ARPABET


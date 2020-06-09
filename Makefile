clean:
	rm ./Results/*.txt
	rm ./sent_similarity/*ENG_viseme.txt
	rm ./sent_similarity/*KOR_viseme.txt
	rm ./sent_similarity/*translation_viseme.txt
	rm ./sent_similarity/*.csv
	rm ./pairkoreng/*.txt
	rm ./Best_synonyms/*.txt

all:
	python main.py

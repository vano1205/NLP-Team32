clean:
	rm ./Results/*.txt
	rm ./sent_similarity/*.txt
	rm ./sent_similarity/*.csv
	rm ./pairkoreng/*.txt
	rm ./Best_synonyms/*.txt

all:
	python main.py

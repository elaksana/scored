Running the parser

To use this program, you must clone the stanford-corenlp-python repo, install packages, and add the dependencies below:

From the /parser directory...

1. sudo pip install pexpect unidecode 
2. clone https://github.com/dasmith/stanford-corenlp-python.git
3. mv ./stanford-corenlp-python/* . 
4. wget http://nlp.stanford.edu/software/stanford-corenlp-full-2014-08-27.zip
5. unzip stanford-corenlp-full-2014-08-27.zip

To run the program...

python main.py -i <input directory of json files> -o <output log directory> -n <number of top words to return>


This program will perform 2 tasks:
	1. Obtain the top N words that occur both on the abstract and journal levels of each journal in the input directory.
	2. Return a list of acronyms which are possibly datasets.


Upcoming developments:
	1. Map acronyms to their full names as listed in the abstracts/journals.
	2. Extract geographical references.
	3. N-Gram Analysis
		a. Some visualizations with datashader
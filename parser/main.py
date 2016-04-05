from json_parser import JsonParser
from argparse import ArgumentParser, FileType
import os, sys, jsonrpc, operator
reload(sys)
sys.setdefaultencoding("utf-8")
from corenlp import *

#Part of speech tags found here: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
unwanted_POS = ['DT', 'TO', 'RP', 'CC', 'IN', 'PRP', '.', ',' ,'!' ,'?', ';', ':']

#Annoying words that cannot be filtered with POS.
unwanted_words = ['be', 'have', 'its', 'it']

def _argparse():
	argparse = ArgumentParser('Obtain text Database Stats')
	argparse.add_argument('-i', '--input_dir', default='../jsonFilesAMS', help = 'Excepts a directory of json files to be parsed')
	argparse.add_argument('-n', '--num', default = -1, help = 'Top N results.  Set to -1 for all.')
	argparse.add_argument('-o', '--output_dir', default = '../outputs', help = 'Output Directory for log files')
	return argparse

def get_top_n(word_count, n):
	sorted_word_count = sorted(word_count.items(), key=operator.itemgetter(1), reverse = True)			
	top_string = ''
	if n > len(sorted_word_count): 
		print 'Did not find that many words!'
		exit(0)

	if n < 0: n = len(sorted_word_count)
	i = 0

	#Print top N words for each abstract
	for word in sorted_word_count:
		if i >= n: break
		top_string += word[0] + ': ' + str(word[1]) + '\n'					
		i += 1
	return top_string




if __name__ == '__main__':
	argp = _argparse().parse_args(sys.argv[1:])
	input_dir = argp.input_dir
	output_dir = argp.output_dir
	n = argp.num
	corenlp = StanfordCoreNLP()
	
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	

	
	corpus_list = open(os.path.join(output_dir, 'datasets.txt'), 'w')
	for filename in os.listdir(input_dir):
			if '.json' in filename:
				#abstract_word_count keeps track of words in only the abstract, while the journal_word_count keepts track of words in the entire journal.
				abstract_word_count = {}
				journal_word_count = {}
				word_set = set()
				counter_logger = open(os.path.join(output_dir, filename), 'w')
				j = JsonParser(os.path.join(input_dir, filename))
				print j.get_filepath()

				for section in j.get_json_data():
					#print section
					text = j.get_json_data()[section]
					results = corenlp.parse(text)
					parsed = json.loads(results)
					#If there is an issue with coreNLP, where it does not return the json structure that we need (likely due to a timeout), we skip that 
					#heading for now.  So far, the biggest issues have been with article reference.
					try:
						for sentence in parsed['sentences']:
							for word in sentence['words']:
								#Filters the undesired parts of speech, words, and ignores numbers.
								if word[1]['PartOfSpeech'] not in unwanted_POS and word[1]['Lemma'] not in unwanted_words and not str(word[1]['Lemma']).isdigit():
									#Lemma is the most primitive form of the word.  eg. rnning -> run, Cows -> cow
									if word[1]['Lemma'] not in abstract_word_count.keys():								
										if section == 'abstract': abstract_word_count[word[1]['Lemma']] = 0
										journal_word_count[word[1]['Lemma'].lower()] = 0
									if section == 'abstract': abstract_word_count[word[1]['Lemma']] += 1
									journal_word_count[word[1]['Lemma'].lower()] += 1
									word_set.add(word[1]['Lemma'])
					except KeyError:
						print 'Issue with ' + filename + ' in the ' + section + ' section.'	
					except:
						print 'Issue with ' + filename
						continue
				
				#Write word counts out to our loggers in the output directory.
				counter_logger.write('Abstract Count: \n')
				counter_logger.write(get_top_n(abstract_word_count, n))
				counter_logger.write('\nFull Journal Count:\n')
				counter_logger.write(get_top_n(journal_word_count, n))	
				counter_logger.close()
				
			
			potential_datasets = set()

			#Check to see if there are more than 2 capital letters in the word.  If so, it is likely to be a corpus.  Add it to the dataset list.
			#We need a better way to filter way.  An acronym such as JPL or NASA would screw us over.
			for word in word_set:
				if sum(1 for c in word if c.isupper()) > 2:
					potential_datasets.add(word)

			for item in potential_datasets:
				corpus_list.write(item + '\n')
	corpus_list.close()
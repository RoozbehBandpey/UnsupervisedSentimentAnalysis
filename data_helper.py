from os.path import join, exists, split
import pickle
from unicodedata import normalize
import string
import re
import os
import glob
import nltk
from nltk.tokenize import word_tokenize
from pprint import pprint

class DataHelper():
	"""
	A data helper class for data transactions

	@:author Roozbeh Bandpey
	"""
	input_dir = ""
	output_dir = ""
	project_root = ""
	
	
	def __init__(self):
		self.input_dir = "input"
		self.output_dir = "dumps"
		self.project_root = os.getcwd()
	
	def load_stopwords(self):
		file_name = "stopwords_en.txt"
		out_path = join(self.project_root, self.output_dir, "stopwords.pickle")
		if exists(out_path):
			print("Loading existing prepared file {0}".format(split(out_path)[-1]))
			try:
				with open(out_path, 'rb') as f_load:
					stopwords = pickle.load(f_load)
				return stopwords
			except IOError as e:
				print(e)
				return False
		else:
			file_path = join(self.project_root, self.input_dir, file_name)
			try:
				with open(file_path, "r", encoding='utf-8') as fin:
					content = fin.read()
					stopwords = content.split("\n")
			except IOError as e:
				print(e)
				return False
			try:
				with open(out_path, 'wb') as f_dump:
					pickle.dump(list(set(stopwords)), f_dump)
				return list(set(stopwords))
			except IOError as e:
				print(e)
				return False
			
	def load_lexicon(self):
		p_words_file_name = "opinion-lexicon-English/positive-words.txt"
		n_words_file_name = "opinion-lexicon-English/negative-words.txt"
		out_path_lst = join(self.project_root, self.output_dir, "lex_pol_list.pickle")
		out_path_dic = join(self.project_root, self.output_dir, "lex_pol_dict.pickle")
		if exists(out_path_lst):
			print("Loading existing prepared file {0}".format(split(out_path_lst)[-1]))
			try:
				with open(out_path_lst, 'rb') as f_load:
					lexicon_polarity_list = pickle.load(f_load)
				return lexicon_polarity_list
			except IOError as e:
				print(e)
				return False
		else:
			p_words_file_path = join(self.project_root, self.input_dir, p_words_file_name)
			n_words_file_path = join(self.project_root, self.input_dir, n_words_file_name)
			lexicon_polarity_list = []
			lexicon_polarity_dict = {}
			try:
				with open(p_words_file_path, "r", encoding='utf-8') as pfin, open(n_words_file_path, "r", encoding='utf-8') as nfin:
					p_list = [w+'.1' for w in pfin.read().split("\n") if ';' not in w and w !='']
					n_list = [w+'.0' for w in nfin.read().split("\n") if ';' not in w and w != '']
					lexicon_polarity_list = p_list + n_list
					
					lexicon_polarity_dict = {item.split('.')[0]:int(item.split('.')[1]) for item in lexicon_polarity_list}
					# print(lexicon_polarity_dict)
					
			except IOError as e:
				print(e)
			
			try:
				with open(out_path_lst, 'wb') as f_dump:
					pickle.dump(lexicon_polarity_list, f_dump)
				with open(out_path_dic, 'wb') as f_dump:
					pickle.dump(lexicon_polarity_dict, f_dump)
					
				return lexicon_polarity_list
			except IOError as e:
				print(e)
				return False
	
	
	def load_reviews(self):
		main_dir = "review_polarity"
		review_path = join(self.project_root, self.input_dir, main_dir, "*", "*")
		out_path = join(self.project_root, self.output_dir, "reviews.pickle")
		
		if exists(out_path):
			print("Loading existing prepared file {0}".format(split(out_path)[-1]))
			try:
				with open(out_path, 'rb') as f_load:
					reviews = pickle.load(f_load)
				return reviews
			except IOError as e:
				print(e)
				return False
		else:
			all_rev_path = glob.glob(review_path)
			review_data = {}
			for path in all_rev_path:
				try:
					with open(path, "r", encoding='utf-8') as fin:
						content = fin.read()
						if 'neg' in path:
							pol = 0
						elif 'pos' in path:
							pol = 1
						else:
							pol = None
						review_data[split(path)[-1].replace('.txt', '')] = {'text': self.__clean_data(content, remove_punc=True),
															'polarity': pol}
	
				except IOError as e:
					print(e)
					return False

			try:
				with open(out_path, 'wb') as f_dump:
					pickle.dump(review_data, f_dump)

				return review_data
			except IOError as e:
				print(e)
				return False



	def __clean_data(self, text, remove_punc=True, to_lower=True, remove_non_printable=True, unicode_normalize=True):
		"""
		char filtering with regex
		remove punctuation
		remove redundant spaces
		normalize unicode characters
		convert to unicode
		tokenize on white space
		convert to lowercase
		remove punctuation from each token
		remove non-printable chars form each token
	
		@:param text: text as str
		@:return: manipulated text as str
		"""
		
		if unicode_normalize:
			text = normalize('NFD', text).encode('ascii', 'ignore')
			text = text.decode('UTF-8')
		if to_lower:
			text = text.lower()
		if remove_punc:
			text = text.split()
			table = str.maketrans('', '', string.punctuation)
			text = [word.translate(table) for word in text]
			text = ' '.join(text)
		if remove_non_printable:
			re_print = re.compile('[^%s]' % re.escape(string.printable))
			text = [re_print.sub('', w) for w in text]
			text = ''.join(text)
		
		text = " ".join(text.split())
		return text
	
	
	def encode_umlauts(self, text):
		"""
		Replaces German umlauts and sharp s to its respective digraphs.

		@:param text: text as str
		@:return: manipulated text as str
		"""
		res = text
		res = res.replace('ä', 'ae')
		res = res.replace('ö', 'oe')
		res = res.replace('ü', 'ue')
		res = res.replace('Ä', 'Ae')
		res = res.replace('Ö', 'Oe')
		res = res.replace('Ü', 'Ue')
		res = res.replace('ß', 'ss')
		return res
	
	
	def decode_umlauts(self, text):
		"""
		Replaces German umlauts digraphs to its actual character.

		@:param text: text as str
		@:return: manipulated text as str
		"""
		res = text
		res = res.replace('ae', 'ä')
		res = res.replace('oe', 'ö')
		res = res.replace('ue', 'ü')
		res = res.replace('Ae', 'Ä')
		res = res.replace('Oe', 'Ö')
		res = res.replace('Ue', 'Ü')
		res = res.replace('ss', 'ß')
		return res
	
	
	def polarity_cluster(self):

		same_out_path = join(self.project_root, self.output_dir, "same_polarity.pickle")
		diff_out_path = join(self.project_root, self.output_dir, "different_polarity.pickle")
		
		if exists(same_out_path) and exit(diff_out_path):
			print("Loading existing prepared file {0}".format(split(same_out_path)[-1]))
			print("Loading existing prepared file {0}".format(split(diff_out_path)[-1]))
			try:
				with open(same_out_path, 'rb') as s_f_load:
					same_polarity = pickle.load(s_f_load)
				with open(diff_out_path, 'rb') as d_f_load:
					diff_polarity = pickle.load(d_f_load)
				return {"same_pol": same_polarity, "diff_pol": diff_polarity}
			except IOError as e:
				print(e)
				return False
		else:
			reviews = self.load_reviews()
			same_polarity = []
			diff_polarity = []
			for doc_id in reviews:
				review = reviews[doc_id]
				review_text = review['text']
				pos_tagged = nltk.pos_tag(word_tokenize(review_text))
				for i in range(len(pos_tagged)):
					if 0 < i < len(pos_tagged) - 1:
						prev_pos_token = pos_tagged[i - 1]
						cur_pos_token = pos_tagged[i]
						next_pos_token = pos_tagged[i + 1]
						prev_pos = prev_pos_token[1]
						token = cur_pos_token[0]
						next_pos = next_pos_token[1]
						
						prev_token = prev_pos_token[0]
						next_token = next_pos_token[0]
						if token == 'and':
							if 'JJ' in prev_pos and 'JJ' in next_pos:
								same_polarity.append(tuple([prev_token, next_token]))
							if 'RB' in prev_pos and 'RB' in next_pos:
								same_polarity.append(tuple([prev_token, next_token]))
						if token == 'but':
							if 'JJ' in prev_pos and 'JJ' in next_pos:
								diff_polarity.append(tuple([prev_token, next_token]))
							if 'RB' in prev_pos and 'RB' in next_pos:
								diff_polarity.append(tuple([prev_token, next_token]))

					
			try:
				with open(same_out_path, 'wb') as s_f_dump:
					pickle.dump(same_polarity, s_f_dump)
				with open(diff_out_path, 'wb') as d_f_dump:
					pickle.dump(diff_polarity, d_f_dump)

				return {"same_pol": same_polarity, "diff_pol": diff_polarity}
			except IOError as e:
				print(e)
				return False
	
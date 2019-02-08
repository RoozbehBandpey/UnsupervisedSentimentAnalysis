from os.path import join, exists, split
import pickle
from unicodedata import normalize
import string
import re
import os


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
		pWords_file_name = "opinion-lexicon-English/positive-words.txt"
		nWords_file_name = "opinion-lexicon-English/negative-words.txt"
		out_path = join(self.project_root, self.output_dir, "lex_pol.pickle")
		if exists(out_path):
			print("Loading existing prepared file {0}".format(split(out_path)[-1]))
			try:
				with open(out_path, 'rb') as f_load:
					lexicon_polarity = pickle.load(f_load)
				return lexicon_polarity
			except IOError as e:
				print(e)
				return False
		else:
			pWords_file_path = join(self.project_root, self.input_dir, pWords_file_name)
			nWords_file_path = join(self.project_root, self.input_dir, nWords_file_name)
			lexicon_polarity = {}
			try:
				with open(pWords_file_path, "r", encoding='utf-8') as fin:
					row = fin.readline()
					while row:
						lexicon_polarity.append(self.__clean_data(row, removePunc=False))
						row = fin.readline()
			except IOError as e:
				print(e)
			
			try:
				with open(out_path, 'wb') as f_dump:
					pickle.dump(list(set(lexicon_polarity)), f_dump)
				return list(set(lexicon_polarity))
			except IOError as e:
				print(e)
				return False
			


	def __clean_data(self, text, removePunc=True, toLower=True, removeNonPrintable=True, unicodeNormalize=True):
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
		
		if unicodeNormalize:
			text = normalize('NFD', text).encode('ascii', 'ignore')
			text = text.decode('UTF-8')
		if toLower:
			text = text.lower()
		if removePunc:
			text = text.split()
			table = str.maketrans('', '', string.punctuation)
			text = [word.translate(table) for word in text]
			text = ' '.join(text)
		if removeNonPrintable:
			re_print = re.compile('[^%s]' % re.escape(string.printable))
			text = [re_print.sub('', w) for w in text]
			text = ''.join(text)
		
		text = " ".join(text.split())
		return text
	
	
	def encodeUmlauts(self, text):
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
	
	
	def decodeUmlauts(self, text):
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
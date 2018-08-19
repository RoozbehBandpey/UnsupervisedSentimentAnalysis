import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
import glob
from collections import Counter
import pickle
import re
import math

class Corpus():

    def __init__(self, filePath = None):#Constructor to instantiate with the input file

        if filePath:
            self.file = open(filePath, 'r')
        else:
            pass


    def omit_header(self):
        tokens = []
        file = self.file.readlines()
        for token in file:
            new_token = token.replace("\n", "")
            if ";" not in new_token and new_token != "":
                tokens.append(new_token)
        return tokens

    def stopwords_data_structure(self):
        stopwords_file = open("Input_Files\\English_Stopwords.txt", "r")
        c = Corpus()
        stopwords = stopwords_file.readlines()
        print(len(set(stopwords)))
        lexicon = c.lexicon_data_structure()
        new_stopwords = []
        for item in stopwords:
            new_token = item.replace("\n", "")
            if (new_token not in lexicon[0]) and (new_token not in lexicon[1]):
                new_stopwords.append(new_token)
            else:
                print(new_token)

        new_stopwords = list(set(new_stopwords))
        print(stopwords)
        print(new_stopwords)
        print(len(stopwords))
        print(len(new_stopwords))


        #for token in file:
        #    print(token)


        #return positive_words, negative_words

    def lexicon_data_structure(self):
        Pwords = Corpus("Input_Files\\opinion-lexicon-English\\positive-words.txt")
        Pwords.__del__()
        positive_words = Pwords.omit_header()

        Nwords = Corpus("Input_Files\\opinion-lexicon-English\\negative-words.txt")
        Nwords.__del__()
        negative_words = Nwords.omit_header()

        return positive_words, negative_words

    def read_review_file(self):
        neg_rev_file_name_list = []
        pos_rev_file_name_list = []


        gold_standard = {}
        reviews = {}
        tagged_reviews = {}

        for file in glob.glob("Input_Files\\review_polarity\\neg\\*.txt"):
            new_neg_file = file.replace("Input_Files\\review_polarity\\neg\\", "")
            neg_rev_file_name_list.append(new_neg_file)
            gold_standard.__setitem__(new_neg_file, -1)

        for file in glob.glob("Input_Files\\review_polarity\\pos\\*.txt"):
            new_pos_file = file.replace("Input_Files\\review_polarity\\pos\\", "")
            pos_rev_file_name_list.append(new_pos_file)
            gold_standard.__setitem__(new_pos_file, 1)

        for file_name in neg_rev_file_name_list:
            negative_review = open("Input_Files\\review_polarity\\neg\\"+file_name, 'r')
            negative_sentence = negative_review.read()
            negative_review.close()
            reviews.__setitem__(file_name,word_tokenize(negative_sentence))
            tagged_reviews.__setitem__(file_name, nltk.pos_tag(word_tokenize(negative_sentence)))

        for file_name in pos_rev_file_name_list:
            positive_review = open("Input_Files\\review_polarity\\pos\\" + file_name, 'r')
            positive_sentence = positive_review.read()
            positive_review.close()
            reviews.__setitem__(file_name, word_tokenize(positive_sentence))
            tagged_reviews.__setitem__(file_name, nltk.pos_tag(word_tokenize(positive_sentence)))
            #print(positive)

        tagged_reviews_removed = {}
        tagged_reviews_removed_words = {}
        for item in tagged_reviews:
            review = []
            review_words = []
            for word_tag in tagged_reviews[item]:
                if word_tag[1] in ['CC', 'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']:
                    review.append(word_tag)
                    review_words.append(word_tag[0])
            tagged_reviews_removed.__setitem__(item, review)
            tagged_reviews_removed_words.__setitem__(item, review_words)
        #review_token_frequency = {}
        #for item in reviews:
        #    review_token_frequency.__setitem__(item, dict(Counter(reviews[item])))
#
        ##n-gram = zip(input_list, input_list[1:], input_list[2:], input_list[3:])
        #n_gram = {}
        #for item in reviews:
        #    window = zip(reviews[item], reviews[item][1:], reviews[item][2:], reviews[item][3:], reviews[item][4:])
        #    window = list(window)
        #    n_gram.__setitem__(item, window)
        #    #print(zip(reviews[item][1:], reviews[item]))
        #    #print(reviews[item])

        pickle_out_1 = open("Output_Files\\reviews.pickle", "wb")
        pickle.dump(reviews, pickle_out_1)
        pickle_out_1.close()

        pickle_out_2 = open("Output_Files\\tagged_reviews.pickle", "wb")
        pickle.dump(tagged_reviews, pickle_out_2)
        pickle_out_2.close()

        pickle_out_3 = open("Output_Files\\tagged_reviews_removed.pickle", "wb")
        pickle.dump(tagged_reviews_removed, pickle_out_3)
        pickle_out_3.close()

        pickle_out_4 = open("Output_Files\\tagged_reviews_removed_words.pickle", "wb")
        pickle.dump(tagged_reviews_removed_words, pickle_out_4)
        pickle_out_4.close()
#
        return (reviews, gold_standard, tagged_reviews, tagged_reviews_removed, tagged_reviews_removed_words)


    def neighbour_tokens(self):
        pickle_positive_lexicon = open("Output_Files\\positive_lexicon.pickle", "rb")
        positive_words = pickle.load(pickle_positive_lexicon)
        pickle_positive_lexicon.close()

        pickle_negative_lexicon = open("Output_Files\\negative_lexicon.pickle", "rb")
        negative_words = pickle.load(pickle_negative_lexicon)
        pickle_negative_lexicon.close()

        pickle_reviews = open("Output_Files\\reviews.pickle", "rb")
        reviews = pickle.load(pickle_reviews)
        pickle_reviews.close()

        biigram = {}
        for item in reviews:
            window = zip(reviews[item], reviews[item][1:])
            window = list(window)
            biigram.__setitem__(item, window)


        #positive_with_neighbours = {}
        #for positive in positive_words:
        #    neighbours = []
        #    for element in biigram:
        #        for win in biigram[element]:
        #            if positive in win:
        #                neighbours.append(win[0])
        #                neighbours.append(win[1])
        #    positive_with_neighbours.__setitem__(positive, list(set(neighbours)))
#
        #pickle_out = open("Output_Files\\positive_with_neighbours.pickle", "wb")
        #pickle.dump(positive_with_neighbours,pickle_out)
        #pickle_out.close()

        negative_with_neighbours = {}
        for negative in negative_words:
            neighbours = []
            for element in biigram:
                for win in biigram[element]:
                    if negative in win:
                        neighbours.append(win[0])
                        neighbours.append(win[1])
            negative_with_neighbours.__setitem__(negative, list(set(neighbours)))

        pickle_out = open("Output_Files\\negative_with_neighbours.pickle", "wb")
        pickle.dump(negative_with_neighbours, pickle_out)
        pickle_out.close()

    def all_reviews_with_frequency(self):
        pickle_reviews = open("Output_Files\\reviews.pickle", "rb")
        reviews = pickle.load(pickle_reviews)
        pickle_reviews.close()
        all_tokens = []
        for item in reviews:
            all_tokens += reviews[item]

        token_frequency = dict(Counter(all_tokens))
        return token_frequency

    def neighbour_reviews_with_frequency(self):
        pickle_reviews = open("Output_Files\\reviews.pickle", "rb")
        reviews = pickle.load(pickle_reviews)
        pickle_reviews.close()
        all_tokens = []
        for item in reviews:
            all_tokens += reviews[item]


        neighbours = zip(all_tokens, all_tokens[1:])
        neighbours = list(neighbours)

        neighbour_reviews = dict(Counter(neighbours))

        return neighbour_reviews

    def same_polarity(self):
        pickle_reviews = open("Output_Files\\tagged_reviews_removed_words.pickle", "rb")
        reviews = pickle.load(pickle_reviews)
        pickle_reviews.close()
        all_tokens = []
        for item in reviews:
            all_tokens += reviews[item]

        trigram = zip(all_tokens, all_tokens[1:], all_tokens[2:])
        trigram = list(trigram)
        #print(len(trigram))
        same_polarity = {}
        for item in trigram:
            if (item[1] == 'and'):
                same_polarity.__setitem__(item[0], item[2])
                same_polarity.__setitem__(item[2], item[0])

        #for i in same_polarity:
        #   print(i, same_polarity[i])
        #print(len(same_polarity))
        #print("Same polarity ends")
        return same_polarity

    def different_polarity(self):
        pickle_reviews = open("Output_Files\\tagged_reviews_removed_words.pickle", "rb")
        reviews = pickle.load(pickle_reviews)
        pickle_reviews.close()

        all_tokens = []
        for item in reviews:
            all_tokens += reviews[item]

        trigram = zip(all_tokens, all_tokens[1:], all_tokens[2:])
        trigram = list(trigram)
        #print(len(trigram))
        different_polarity = {}
        for item in trigram:
            if (item[1] == 'but'):
                different_polarity.__setitem__(item[0], item[2])
                different_polarity.__setitem__(item[2], item[0])
        #print("Different polarity ends")
        return different_polarity

    def PMI_data_structure(self):
        pickle_reviews = open("Output_Files\\reviews.pickle", "rb")
        reviews = pickle.load(pickle_reviews)
        pickle_reviews.close()

        all_tokens = []
        for item in reviews:
            all_tokens += reviews[item]

        all_tokens_frequency = dict(Counter(all_tokens))
        poor_hit = all_tokens_frequency["poor"]
        excellent_hit =  all_tokens_frequency["excellent"]
        print(poor_hit)
        print(excellent_hit)

        n_gram = zip(all_tokens, all_tokens[1:], all_tokens[2:], all_tokens[3:], all_tokens[4:])
        n_gram = list(n_gram)

        PMI_dictrionary = all_tokens_frequency

        for element in PMI_dictrionary:
            PMI_dictrionary[element] = [0.001,0.001]


        i = 0
        j = 0
        for window in n_gram:
            for gram in window:
                if (gram in window) and ("excellent" in window):
                    PMI_dictrionary[gram][0] += 1
                if (gram in window) and ("poor" in window):
                    PMI_dictrionary[gram][1] += 1
                if (gram in window) and ("poor" in window) and ("excellent" in window):
                    PMI_dictrionary[gram][0] += 1
                    PMI_dictrionary[gram][1] += 1

        corpus_size = len(all_tokens)
        PMI_data_structure = {}
        for element in PMI_dictrionary:
            PMI_data_structure.__setitem__(element, math.log2((PMI_dictrionary[element][0]*poor_hit)/(PMI_dictrionary[element][1]*excellent_hit)))

        pickle_out = open("Output_Files\\PMI_data_structure.pickle", "wb")
        pickle.dump(PMI_data_structure, pickle_out)
        pickle_out.close()


    def __del__(self):  # destructor to kill the objects and close the input file
        #self.file.close()
        pass
from corpus import Corpus
import pickle
import random
import time
import sys
import math

class Model:

    def __init__(self, modelfile = None):#Initializing the Model
        self.table_statistics = []
        self.table_statistics.append(['Features', 'Words', 'Sentences'])
        if modelfile:
            self.load(modelfile)
        else:
            self.feature_dictionary = {'#': 0}
            self.sentiment_dictionary = {}
            self.sentiment_dictionary_reverse = {}

    def count_based_prediction(self):

        pickle_positive_lexicon = open("Output_Files\\positive_lexicon.pickle", "rb")
        positive_words = pickle.load(pickle_positive_lexicon)
        pickle_positive_lexicon.close()

        pickle_negative_lexicon = open("Output_Files\\negative_lexicon.pickle", "rb")
        negative_words = pickle.load(pickle_negative_lexicon)
        pickle_negative_lexicon.close()

        pickle_reviews = open("Output_Files\\reviews.pickle", "rb")
        reviews = pickle.load(pickle_reviews)
        pickle_reviews.close()

        print("count_based_prediction runs, please wait..")
        predict = {}
        i = 0
        for item in reviews:
            rev_score = 0

            for token in reviews[item]:
                if token in positive_words:
                    rev_score += 1
                if token in negative_words:
                    rev_score -= 1

            if rev_score >= 1:
                rev_score = 1
            elif rev_score < -1:
                rev_score = -1
            #else:
            #    rev_score = random.choice([1,-1])
            predict.__setitem__(item, rev_score)
            sys.stdout.write("\r%d%%" % i)
            sys.stdout.flush()
            i += 100/len(reviews)

        return predict


    def count_based_prediction_conjunction(self):

        pickle_positive_lexicon = open("Output_Files\\positive_lexicon.pickle", "rb")
        positive_words = pickle.load(pickle_positive_lexicon)
        pickle_positive_lexicon.close()

        pickle_negative_lexicon = open("Output_Files\\negative_lexicon.pickle", "rb")
        negative_words = pickle.load(pickle_negative_lexicon)
        pickle_negative_lexicon.close()

        pickle_reviews = open("Output_Files\\reviews.pickle", "rb")
        reviews = pickle.load(pickle_reviews)
        pickle_reviews.close()

        c1 = Corpus()
        c2 = Corpus()
        same_pol = c1.same_polarity()
        diff_pol = c2.different_polarity()

        print("count_based_prediction_conjunction runs, please wait..")
        predict = {}
        i = 0
        for item in reviews:
            rev_score = 0
            for token in reviews[item]:
                if (token in positive_words):
                    rev_score += 3
                if (token in same_pol.keys()):
                    if same_pol[token] in positive_words:
                        rev_score += 1
                if (token in diff_pol.keys()):
                    if diff_pol[token] in positive_words:
                        rev_score -= 1
                if token in negative_words:
                    rev_score -= 3
                if (token in same_pol.keys()):
                    if same_pol[token] in negative_words:
                        rev_score -= 1
                if (token in diff_pol.keys()):
                    if diff_pol[token] in negative_words:
                        rev_score += 1

            if rev_score >= 1:
                rev_score = 1
            elif rev_score < -1:
                rev_score = -1
            predict.__setitem__(item, rev_score)
            sys.stdout.write("\r%d%%" % i)
            sys.stdout.flush()
            i += 100/len(reviews)

        return predict

    def count_based_prediction_conjunction_pmi(self):

        pickle_positive_lexicon = open("Output_Files\\positive_lexicon.pickle", "rb")
        positive_words = pickle.load(pickle_positive_lexicon)
        pickle_positive_lexicon.close()

        pickle_negative_lexicon = open("Output_Files\\negative_lexicon.pickle", "rb")
        negative_words = pickle.load(pickle_negative_lexicon)
        pickle_negative_lexicon.close()

        pickle_reviews = open("Output_Files\\reviews.pickle", "rb")
        reviews = pickle.load(pickle_reviews)
        pickle_reviews.close()

        c1 = Corpus()
        c2 = Corpus()
        same_pol = c1.same_polarity()
        diff_pol = c2.different_polarity()

        # m = Model()
        pmi = open("Output_Files\\PMI_data_structure.pickle", "rb")
        PMI_data_structure = pickle.load(pmi)
        pmi.close()

        # print(gold_standard)
        # print(len(gold_standard))
        print("Predict runs, please wait..")
        predict = {}
        i = 0
        for item in reviews:
            rev_score = 0
            for token in reviews[item]:
                rev_score += PMI_data_structure[token]
                if (token in positive_words):
                    rev_score += 30
                if (token in same_pol.keys()):
                    if same_pol[token] in positive_words:
                        rev_score += 1
                if (token in diff_pol.keys()):
                    if diff_pol[token] in positive_words:
                        rev_score -= 1
                if token in negative_words:
                    rev_score -= 20
                if (token in same_pol.keys()):
                    if same_pol[token] in negative_words:
                        rev_score -= 1
                if (token in diff_pol.keys()):
                    if diff_pol[token] in negative_words:
                        rev_score += 1

            if rev_score >= 1:
                rev_score = 1
            elif rev_score < -1:
                rev_score = -1
            predict.__setitem__(item, rev_score)
            sys.stdout.write("\r%d%%" % i)
            sys.stdout.flush()
            i += 100 / len(reviews)

        return predict

    def pointwise_mutual_information(self, token):
        pmi = open("Output_Files\\PMI_data_structure.pickle", "rb")
        PMI_data_structure = pickle.load(pmi)
        pmi.close()

        negative_pmi = 0
        positive_pmi = 0
        #bigger_one = 0
        #less_one = 0
        for i in PMI_data_structure:
            if PMI_data_structure[i] > 0:
                positive_pmi += 1
            if PMI_data_structure[i] < 0:
                negative_pmi += 1
        #    if PMI_data_structure[i] > 1:
        #        bigger_one += 1
        #    if PMI_data_structure[i] < 1:
        #        less_one += 1
        print("negative_pmi ", negative_pmi)
        print("positive_pmi ", positive_pmi)
        #print("bigger_one ", bigger_one)
        #print("less_one# ", less_one)

        #if PMI_data_structure[token] > 0:
        #    return 1
        #if PMI_data_structure[token] < 0:
        #    return -1
        #else:
        #    print("Erorr")
        #    return 0




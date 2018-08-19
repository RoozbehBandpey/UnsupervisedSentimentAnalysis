import datetime
import re

from model import Model
from evaluation import Evaluation
import nltk
import pickle

from corpus import Corpus
import winsound
import os
import sys
import time

################################################################################################
m = Model()
#pred = m.count_based_prediction()
#pred = m.count_based_prediction_conjunction()
pred = m.count_based_prediction_conjunction_pmi()
#
Eval = Evaluation()
result = Eval.Evaluate( pred)
print("\n")
print(result[0])
print("F-measure micro: "+result[1]+"   F-measure macro: "+result[2])
##################################################################################################

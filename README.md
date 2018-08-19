# UnsupervisedSentimentAnalysis
Classification of Amazon Product Reviews: With Lexical Sentiment Analysis and Lexicon Polarity Generation

Corpus.py reads all the files and build the proper data structure
Test file: This dataset is the one used by Pang et al. (2002).
It consists of two folders, pos and neg, each containing 1000 positive and negative documents, respectively.
The provided data by Hu and Liu (2004), meant no make predictions.
This dataset consists of two ﬁles, positive-words.txt and negative-words.txt,
containing several thousand positive and negative words, respectively.
The ﬁles also contain some header information that you have to remove or ignore when processing.

Corpus --> Constructor : If the name of the file is passed it will open the file for further use


    lexicon_data_structure : reads the positive or negative word list and omit the header information
    by calling the omit_header function, and make list of positive or negative words.

    read_review_file : Get the list of name of all positive and negative files in the directory
    then read them step by step base on mentioned lists and fetch the review and make a list with name of the file
    and content of it.

    Tokenize : the content of reviews should be tokenized
    Stop words : I should omit the stop word, the idea is stop words don't carry sentiment (hmmmmmmmmmmmm!!!????)


Model --> take the finale product of corpus and try to predict the review


###########################################Dear reader###########################################

All the input data are provided

I order to run the code
Just run the main.py

In order to run and test different methods comment and uncomment the lines 17, 18, 19 in main.py

################################################################################################

corpus.py --> carrie the main duty of reading file and costructing the premitive data structures
evaluation.py --> takes the predicted and gold-standard and shows the acuuracy, etc.,
model.py --> models are implemented

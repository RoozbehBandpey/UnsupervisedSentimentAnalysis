from terminaltables import AsciiTable
import pickle


class Evaluation():

    def __int__(self):
        pass

    def Evaluate(self, predicted = {}):
        pickle_gold_standard = open("Output_Files\\gold_standard.pickle", "rb")
        gold_standard = pickle.load(pickle_gold_standard)
        pickle_gold_standard.close()


        table_data = []
        sentiments = [1, -1]
        table_data.append(['Rows',
                           'Polarity',
                           'FP',
                           'TP',
                           'FN',
                           'TN',
                           'GSF',
                           'PSF',
                           'Precision',
                           'Recall',
                           'Accuracy',
                           'F1-Score'])


        false_negative = 0
        false_positive = 0
        true_positive = 0
        true_negative = 0
        F1_micro = 0.0
        for sentiment in sentiments:
            gold_sentiment_frequency = 0
            predicted_sentiment_frequency = 0
            sentiment_false_negative = 0
            sentiment_false_positive = 0
            sentiment_true_positive = 0
            sentiment_true_negative = 0
            corpus_count = 0
            for gold_review_file in gold_standard:
                if sentiment == gold_standard[gold_review_file]:
                    gold_sentiment_frequency += 1
                    if sentiment == predicted[gold_review_file]:
                        sentiment_true_positive += 1
                        true_positive += 1
                    else:
                        sentiment_false_negative += 1
                        false_negative += 1
            for pred_review_file in predicted:
                if sentiment == predicted[pred_review_file]:
                    predicted_sentiment_frequency += 1
                    if sentiment != gold_standard[pred_review_file]:
                        sentiment_false_positive += 1
                        false_positive += 1
                corpus_count += 1
                sentiment_true_negative = len(gold_standard) - (sentiment_true_positive +\
                                                                sentiment_false_positive+\
                                                                sentiment_false_negative)
            if sentiment == -1:
                sent = "Negative"
            else:
                sent = "Positvie"
            table_data.append([str(sentiments.index(sentiment)+1),
                               str(sent),
                               str(int(sentiment_false_positive)),
                               str(int(sentiment_true_positive)),
                               str(int(sentiment_false_negative)),
                               str(int(sentiment_true_negative)),
                               str(int(gold_sentiment_frequency)),
                               str(int(predicted_sentiment_frequency)),
                               str(round(self.Precision(float(sentiment_true_positive), float(sentiment_false_positive)), 3)),
                               str(round(self.Recall(float(sentiment_true_positive), float(sentiment_false_negative)), 3)),
                               str(round(self.Accuracy(float(sentiment_true_negative), float(sentiment_false_positive),
                                                       float(sentiment_false_negative), float(sentiment_true_negative)), 3)),
                               str(round(
                                   self.F1Score(self.Precision(float(sentiment_true_positive), float(sentiment_false_positive)),
                                                self.Recall(float(sentiment_true_positive), float(sentiment_false_negative))), 3))])

            F1_micro += round(self.F1Score(self.Precision(float(sentiment_true_positive), float(sentiment_false_positive)),
                                  self.Recall(float(sentiment_true_positive), float(sentiment_false_negative))), 3)

        true_negative = len(gold_standard) - (true_positive + false_positive + false_negative)
        F1total = self.F1Score(self.Precision(float(true_positive), float(false_positive)),
                               self.Recall(float(true_positive), float(false_negative)))

        F1_micro = F1_micro / len(sentiments)
        table = AsciiTable(table_data)


        return (table.table, str(round(F1_micro, 3)), str(round(F1total, 3)))


    def Precision(self, TruePositive, FalsePositive):
        if TruePositive == 0:
            return 0
        else:
            return (TruePositive / (TruePositive + FalsePositive))

    def Recall(self, TruePositive , FalseNegative):
        if TruePositive == 0:
            return 0
        else:
            return (TruePositive / (TruePositive + FalseNegative))

    def Accuracy(self, TruePositive, FalsePositive, FalseNegative,TrueNegative):
        TrueAll = TruePositive + TrueNegative
        FalseAll = FalsePositive + FalseNegative
        return (TrueAll / (TrueAll + FalseAll))

    def F1Score(self, precision , recall):
        if precision == 0:
            return 0
        else:
            return ((2 * precision * recall) / (precision + recall))




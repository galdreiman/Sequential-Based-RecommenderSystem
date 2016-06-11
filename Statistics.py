from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt


class Statistics(object):

    def __init__(self):
        self.correct_predictions = 0
        self.incorrect_predictions = 0
        self.num_of_nodes = 0
        self.num_of_edges = 0


    def print_prediction_stats(self,y_test, y_score):
        self.print_correct()
        self.print_incorrect()
        self.print_num_of_edges()
        self.print_num_of_nodes()
        # self.draw_ROC_curve(y_test, y_score)

    def print_num_of_nodes(self):
        print 'num of nodes'
        print self.num_of_nodes

    def print_num_of_edges(self):
        print 'num of edges'
        print self.num_of_edges

    def print_incorrect(self):
        total_guesses = self.correct_predictions + self.incorrect_predictions
        incorrect_precentage =  float(self.incorrect_predictions)/ float(total_guesses)
        print "correct:"
        print "   {}/{}  [{}]".format(self.incorrect_predictions, total_guesses, incorrect_precentage)

    def print_correct(self):
        total_guesses = self.correct_predictions + self.incorrect_predictions
        correct_precentage =  float(self.correct_predictions)/ float(total_guesses)
        print "incorrect:"
        print "   {}/{}  [{}]".format(self.correct_predictions, total_guesses, correct_precentage)

    def correct_prediction(self):
        self.correct_predictions += 1

    def incorrect_prediction(self):
        self.incorrect_predictions += 1

    def draw_ROC_curve(self, y_test, y_score):
        print y_test
        print y_score
        fpr, tpr, _ = roc_curve(y_test, y_score)
        roc_auc = auc(fpr, tpr)
        print fpr
        print tpr

        plt.figure()
        plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic example')
        plt.legend(loc="lower right")
        plt.show()
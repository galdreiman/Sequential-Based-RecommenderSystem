



class Statistics(object):

    def __init__(self):
        self.correct_predictions = 0
        self.incorrect_predictions = 0
        self.num_of_nodes = 0
        self.num_of_edges = 0


    def print_prediction_stats(self):
        self.print_correct()
        self.print_incorrect()
        self.print_num_of_edges()
        self.print_num_of_nodes()

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
        print "   {}/{}  [{}]".format(self.correct_predictions, total_guesses, correct_precentage)

    def correct_prediction(self):
        self.correct_predictions += 1

    def incorrect_prediction(self):
        self.incorrect_predictions += 1
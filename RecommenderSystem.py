import csv
from numpy import genfromtxt
from GraphDrawer import GraphDrawer
from Purchase import Purchase
from Click import Click
import Config
from Statistics import Statistics


class RecSys:

    def __init__(self):
        print(' ')

    def main(self):

        #------------------------------------------------------------------
        # create the training & test sets, skipping the header row with [1:]
        # trainset = self.read_csv_file('Data/buys_small.dat')
        trainset, testset = self.read_csv_file(Config.DATA_FILENAME)
        # self.print_session(trainset,'140806')

        graph = GraphDrawer()
        graph.build_graph(trainset)
        graph.fit()
        #graph.print_all_edges()
        # graph.print_all_nodes()
        # graph.print_edges_data()
        # graph.print_successors(('-1', '-1', '1046'))
        y_true, y_score = graph.predict(testset)
        # graph.draw()
        graph.print_prediction_stats()
        # graph.roc(y_true, y_score)


    def print_session(self,dataset, sessionID):
        for p in dataset[sessionID]:
            print p

    def read_csv_file(self, filename):
        '''
        dataset is a dictionary that maps  'sessionID' --> 'Purchases'
        '''
        dataset = dict()
        with open(filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                sessionId = row[0]
                if Config.DATA_TYPE == Config.PURCHASES:
                    if sessionId not in dataset:
                        dataset[sessionId] = [Purchase(row[1:])]
                    else:
                        dataset[sessionId].append(Purchase(row[1:]))
                else:
                    if Config.DATA_TYPE == Config.CLICKS:
                        if sessionId not in dataset:
                            dataset[sessionId] = [Click(row[1:])]
                        else:
                            dataset[sessionId].append(Click(row[1:]))

        # split the dataset into trainset and testset
        trainset_size = int(len(dataset) * Config.TRAINSET_SIZE)

        train = dict(dataset.items()[trainset_size:])
        test  = dict(dataset.items()[:trainset_size])

        return train, test












if __name__=="__main__":
    k = RecSys()
    k.main()
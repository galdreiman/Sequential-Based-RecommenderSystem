import csv
from numpy import genfromtxt
from GraphDrawer import GraphDrawer
from Purchase import Purchase
import Config


class RecSys:

    def __init__(self):
        print(' ')

    def main(self):

        #------------------------------------------------------------------
        # create the training & test sets, skipping the header row with [1:]
        # trainset = self.read_csv_file('Data/buys_small.dat')
        trainset, testset = self.read_csv_file('Data/buys_small.dat')
        # self.print_session(trainset,'140806')

        graph = GraphDrawer(trainset)
        graph.build_graph()
        graph.fit()
        #graph.print_all_edges()
        # graph.print_all_nodes()
        # graph.print_edges_data()
        # graph.print_successors(('-1', '-1', '1046'))
        graph.predict(testset)


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
                if sessionId not in dataset:
                    dataset[sessionId] = [Purchase(row[1:])]
                else:
                    dataset[sessionId].append(Purchase(row[1:]))

        # split the dataset into trainset and testset
        trainset_size = int(len(dataset) * Config.TRAINSET_SIZE)

        train = dict(dataset.items()[trainset_size:])
        test  = dict(dataset.items()[:trainset_size])

        return train, test












if __name__=="__main__":
    k = RecSys()
    k.main()
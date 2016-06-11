import csv
from numpy import genfromtxt
from GraphDrawer import GraphDrawer
from Purchase import Purchase
from Click import Click
import Config
from Statistics import Statistics
import random


class RecSys:

    def __init__(self):
        print(' ')

    def main(self):

        #------------------------------------------------------------------
        # create the training & test sets, skipping the header row with [1:]
        # trainset = self.read_csv_file('Data/buys_small.dat')
        trainset, testset = self.read_csv_file(Config.DATA_FILENAME)
        train_keys = list(trainset.keys())

        graph = GraphDrawer()
        graph.build_graph(trainset,train_keys)
        graph.fit()
        y_true, y_score = graph.predict(testset)
        graph.print_prediction_stats(y_true, y_score)

        ###########
        # Shuffle keys for validations:
        print 'VALIDATION:'
        shuffled_keys = self.get_shuffled_list(trainset)
        valid_graph = GraphDrawer()
        valid_graph.build_graph(trainset,shuffled_keys)
        valid_graph.fit()
        valid_y_true, valid_y_score = valid_graph.predict(testset)
        valid_graph.print_prediction_stats(valid_y_true, valid_y_score)

    def get_shuffled_list(self, trainset):
        train_keys = list(trainset.keys())
        # shuffled_keys = random.shuffle(train_keys)
        x = [[x] for x in train_keys]
        random.shuffle(x)
        shuffled_keys = [x[0] for x in x]
        return shuffled_keys

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
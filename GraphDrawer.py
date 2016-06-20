import networkx as nx
import Config
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
from Statistics import Statistics


class GraphDrawer():

    def __init__(self):
        self.dataset = None
        self.Graph = nx.DiGraph()
        self.K =2
        self.items = dict()
        self.stats = Statistics()


    def build_graph(self, dataset, keys):
        self.dataset = dataset
        for sessionID in keys:
            try:
                session_purchases = self.dataset[sessionID]
            except:
                print sessionID
            session_states = self.extract_states(session_purchases)
            self.insert_states(session_states)
        # self.print_edges_data()
        self.mark_popular_item()
        self.stats.num_of_edges = self.Graph.number_of_edges()
        self.stats.num_of_nodes = self.Graph.number_of_nodes()

    def mark_popular_item(self):
        max = 0
        for item in self.items.keys():
            if self.items[item] > max:
                max = self.items[item]
                self.most_popular_item = item

    def print_all_nodes(self):
        for n in self.Graph.nodes(): print str(n)

    def print_all_edges(self):
        for e in self.Graph.edges(): print e

    def print_successors(self,source_state):
        succ_list = self.Graph.successors(source_state)
        for succ in succ_list: print succ

    def print_edges_data(self):
        for edge in self.Graph.edges():
            print '{0} -->  {1}    {2}'.format(edge[0], edge[1],self.Graph.get_edge_data(edge[0], edge[1], None))

    def draw(self):
        # nx.draw(self.Graph)
        # nx.draw_networkx(self.Graph)
        pos = nx.shell_layout(self.Graph)
        nx.draw(self.Graph, pos)

        # show graph
        plt.show()
        raw_input('press any key to continue')

    def fit(self):
        """
        this method goes over all nodes and counts the number of out edges,
        then, it normalize the weight of each edge according to:
            for each node t in successor(s) do:
                sum += weight(s,t)
            for each node t in successors(s) do:
                normalized_weight(s,t)  =   weight(s,t)/sum
        :return: void
        """
        nodes = self.Graph.nodes()
        print "---- number of nodes in the graph = {0}".format(len(nodes))
        for curr_node in nodes:
            node_successors = self.Graph.successors(curr_node)
            sum = 0
            for s in node_successors:
                edge_data =self.Graph.get_edge_data(curr_node, s, None)
                # print edge_data
                count = edge_data[Config.COUNT]
                sum += count

            # print sum
            # print 'curr:  ' + str(curr_node)
            for s in node_successors:
                count = self.Graph[curr_node][s][Config.COUNT]
                self.Graph[curr_node][s][Config.WEIGHT] = float(count) / float(sum)
                # print 'succ:   ' + str(s) + ' ' + str(self.Graph[curr_node][s])

    def predict(self,testset):
        """
        :param testset: a map - 'itemIP' --> list<Purchase>

        the main idea is:
            1. for each session
                1.1 hide the last item purchased
                1.2 predict the last item using the model
                1.3 save the
        """
        y_true = []
        y_pred = []
        y_score = []

        for key in testset.keys():
            sequence = testset[key]
            seq_length = len(sequence)
            if seq_length > 1:
                actual = sequence[-1].itemID
                prediction, is_popularity_prediction = self.__predict_sequence__(sequence[:-1])

                if prediction != None and is_popularity_prediction:
                    y_true.append(1)
                    if actual in prediction[Config.PRED_ITEMS]:
                        y_pred.append(1)
                        y_score.append(prediction[Config.PRED_PROB]) #distanse 0
                        self.stats.correct_prediction()
                    else:
                        y_score.append(0)
                        y_pred.append(0)
                        self.stats.incorrect_prediction()
                    # print '**************'
                    # raw_seq = [x.itemID for x in sequence]
                    # print raw_seq
                    # print 'prediction[{0}]  actual[{1}]  success[{2}]'.format(prediction[Config.PRED_ITEMS], actual, actual in prediction[Config.PRED_ITEMS])
                    # print '----------------------'
                    # print ' '
        return y_true,y_score, y_pred

    def roc(self,y_true, y_score):
        self.stats.draw_ROC_curve(y_true,y_score)



    def print_prediction_stats(self,y_true, y_score,y_pred):
        self.stats.print_prediction_stats(y_true, y_score,y_pred)

    def __predict_sequence__(self,sequence):
        states = self.extract_states(sequence)
        last_state = states[-1]
        best_succ = dict()
        best_succ[Config.PRED_PROB] = 0.0
        best_succ[Config.PRED_ITEMS] = []

        is_popularity_prediction = False
        if self.Graph.__contains__(last_state):
            successors = self.Graph.successors(last_state)
            max_weight = 0.0
            for succ in successors:
                edge = self.Graph[last_state][succ]
                max_weight = edge[Config.WEIGHT]
                if float(edge[Config.WEIGHT]) > max_weight:
                    best_succ[Config.PRED_PROB] = max_weight
                    best_succ[Config.PRED_ITEMS] = [succ[-1]]
                else:
                    if float(edge[Config.WEIGHT]) == max_weight:
                        best_succ[Config.PRED_PROB] = max_weight
                        best_succ[Config.PRED_ITEMS].append(succ[-1])

                # print '{0}  --->   {1}  count[{2}]  weight[{3}]'.format(last_state,succ,edge[Config.COUNT], edge[Config.WEIGHT])
                is_popularity_prediction = True
        else:
            best_succ[Config.PRED_PROB] = 0.0
            best_succ[Config.PRED_ITEMS].append(self.most_popular_item)
            # print 'popularity:  last state: {0} best: {1}'.format(last_state, best_succ)

        return best_succ, is_popularity_prediction


    def insert_states(self, states):

        # insert all states:
        for state in states:
            self.Graph.add_node(state)

        # insert all edges:
        for i in range(len(states) -1):
            self.add_to_edge(states[i], states[i+1], Config.COUNT, 1)
        # in this case there are nodes without a successor
        # therefore we need to handle them by finding the closest node/nodes and
        # connect them with a new edge
        if len(states) == 1:
            for node in states:
                if self.K == 3:
                    if node[0] == '-1' and node[1] == '-1':
                        # this is the case of there is only one item in a state(sequence of purchases)
                        # and now we're going to find all state that this item is in
                        # then, add edges accordingly
                        item = node[2]
                        for s in self.Graph.nodes():
                            if s[0] == '-1' and item == s[1] and s != node:
                                self.add_to_edge(node,s,Config.COUNT,1)
                    else:
                        first_item = node[1]
                        second_item = node[2]
                        for s in self.Graph.nodes():
                            if s[0] == first_item and s[1] == second_item:
                                if s != node:
                                    self.add_to_edge(node,s,Config.COUNT,1)
                if self.K == 2:
                    if node[0] == '-1':
                        item = node[1]
                        for s in self.Graph.nodes():
                            if s[1] == item and s != node:
                                self.add_to_edge(node,s,Config.COUNT,1)





    def add_to_edge(self,u,v,attr, value):
        if(self.Graph.get_edge_data(u, v,None) is None):
                self.Graph.add_edge(u, v,{attr:value})

        else:
            self.Graph[u][v][attr] += value

    def extract_states(self,purchases):
        items = []
        for purchase in purchases:
            items.append(purchase.itemID)
            self.count_item(purchase.itemID)
        items_length = len(items)
        if items_length < 3:
            for i in range(self.K - items_length):
                items.insert(0,'-1')

        states = zip(*(items[i:] for i in range(self.K)))
        # for p in purchases: print p
        # print states
        return states

    def count_item(self, itemID):
        if itemID in self.items:
            self.items[itemID] += 1
        else:
            self.items[itemID] = 1


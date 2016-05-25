import sys
import networkx as nx
import Config



class GraphDrawer():

    def __init__(self, dataset):
        self.dataset = dataset
        self.Graph = nx.DiGraph()
        self.K = 3


    def build_graph(self):

        for sessionID in self.dataset.keys():
            session_purchases = self.dataset[sessionID]
            session_states = self.extract_states(session_purchases)
            self.insert_states(session_states)
        # self.print_edges_data()

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

    def fit(self):
        """
        this method goes over all nodes and count the number of out edges,
        then, it normalize the weight of each edge according to:
            for each node t in successor(s) do:
                sum += weight(s,t)
            for each node t in successors(s) do:
                normalized_weight(s,t)  =   weight(s,t)/sum
        :return: void
        """
        nodes = self.Graph.nodes()
        print "---- len = {0}".format(len(nodes))
        print self.Graph.number_of_nodes()
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
        for key in testset.keys():
            print '---   {}   ---'.format(key)
            for p in testset[key]:
                print p

    def insert_states(self, states):

        # insert all states:
        for state in states:
            self.Graph.add_node(state)

        # insert all edges:
        for i in range(len(states) -1):
            self.add_to_edge(states[i], states[i+1], Config.COUNT, 3)
        # in this case there are nodes without a successor
        # therefore we need to handle them by finding the closest node/nodes and
        # connect them with a new edge
        if len(states) == 1:
            for node in states:
                if node[0] == '-1' and node[1] == '-1':
                    # this is the case of there is only one item in a state(sequence of purchases)
                    # and now we're going to find all state that this item is in
                    # then, add edges accordingly
                    item = node[2]
                    for s in self.Graph.nodes():
                        if (item == s[0] or item == s[1]) and s != node:
                            self.add_to_edge(node,s,Config.COUNT,1)
                else:
                    first_item = node[1]
                    second_item = node[2]
                    for s in self.Graph.nodes():
                        if s[0] == first_item and s[1] == second_item:
                            if s != node:
                                self.add_to_edge(node,s,Config.COUNT,1)



    def add_to_edge(self,u,v,attr, value):
        if(self.Graph.get_edge_data(u, v,None) is None):
                self.Graph.add_edge(u, v,{attr:value})

        else:
            self.Graph[u][v][attr] += value

    def extract_states(self,purchases):
        items = []
        for purchase in purchases:
            items.append(purchase.price)
        items_length = len(items)
        if items_length < 3:
            for i in range(self.K - items_length):
                items.insert(0,'-1')

        states = zip(*(items[i:] for i in range(self.K)))
        return states



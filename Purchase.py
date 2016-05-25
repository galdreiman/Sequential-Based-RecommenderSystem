


class Purchase():

    def __init__(self,row):
        self.timestamp = row[0]
        self.itemID = row[1]
        self.price = row[2]
        self.quantity = row[3]


    def __str__(self):
        str = "timestamp[{0}]  itemID[{1}] price[{2}]  quantity[{3}]".format(self.timestamp, self.itemID, self.price, self.quantity)
        return str
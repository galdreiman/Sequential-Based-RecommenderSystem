


class Click():

    def __init__(self,row):
        self.timestamp = row[0]
        self.itemID = row[1]
        self.category = row[2]


    def __str__(self):
        str = "timestamp[{0}]  itemID[{1}] category[{2}]".format(self.timestamp, self.itemID, self.category)
        return str
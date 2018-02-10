from Queue import PriorityQueue

class MyPriorityQueue(PriorityQueue):
    ppp = {}
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item

    def getItemAndPriority(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item,self.ppp[item]

    def getPriority(self,item):
        return self.ppp[item]
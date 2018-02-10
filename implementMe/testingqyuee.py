from Queue import PriorityQueue
from Pstack import *

class MyPriorityQueue(PriorityQueue):
    ppp={}
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1
        self.ppp[item]=priority

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item,self.ppp[item]





queue = MyPriorityQueue()
print type(queue)
queue.put('item2', 7)
queue.put('item1', 1)
queue.put('apploe',5)
queue.put('pineapple',2)
queue.put('orange',3)
queue.put('apple',4)

s=Stack()

s.push("hererere")
s.push("asds")
s.push("asdaqweq")


while not queue.empty():
    print queue.get()


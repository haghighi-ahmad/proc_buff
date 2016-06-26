#!/usr/bin/python

import pickle


class event_list():

    def __init__(self):
        self.tail = -1
        self.head = 0
        self.event_lst = []

    def push(self, item):
        self.tail += 1
        self.event_lst.append(item)
        return self.tail

    def pop(self, indx):
        if indx <= self.tail:
            return self.event_lst[indx]

    def fifo(self):
        if self.head <= self.tail:
            tmpp = self.event_lst[self.head]
            self.head += 1
            return tmpp


a=event_list()
a.push("ahmad")
a.push("auafefjklwhakjfhaejlhalcjkahdadscsdjkch \n loawdkjsokjocfhdslcfjdshfjklasdhfldsf")
x= a.push("asasasasasasasasasasasasasasasasa")

print a.fifo()
print a.fifo()
print a.fifo()
print a.fifo()
print a.fifo()

with open('/tmp/company_data.pkl', 'wb') as output:
    pickle.dump(a, output, pickle.HIGHEST_PROTOCOL)

del a

with open('/tmp/company_data.pkl', 'rb') as input:
    b = pickle.load(input)
    print b.pop(0)
    print b.pop(1)
    print b.pop(2)
    print b.pop(3)
    print b.pop(4)


from FibonacciHeap import FibHeap


class FibPQ():
    def __init__(self):
        self.heap = FibHeap()

    def __len__(self):
        return self.heap.count

    def insert(self, node):
        self.heap.insert(node)

    def minimum(self):
        return self.heap.minimum()

    def removeminimum(self):
        return self.heap.removeminimum()

    def decreasekey(self, node, new_priority):
        self.heap.decreasekey(node, new_priority)

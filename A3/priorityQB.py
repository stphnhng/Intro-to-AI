'''This is an implementation of a priority queue that supports
the remove operation as well as insert and deletemin.
It is based on the heapdict implementation at 
https://github.com/DanielStutzbach/heapdict

Version B0.22, S. Tanimoto, Jan. 20, 2018.
 Supports access by key to previously enqueued elements.
 This requires the version of heapdict named heapdictB.

Prior development:
A method getpriority(elt) was added on Oct. 21.

This data structure is provided to support implementations
of A* in Python.

'''
from heapdictB import heapdictB

class PriorityQB:
  def __init__(self):
    self.h = heapdictB()

  def insert(self, elt, priority):
    if elt in self.h:
      raise Exception("Key is already in the priority queue: "+str(elt))
    self.h[elt] = priority

  def deletemin(self):
    # Returns the element having smallest priority value.
    return self.h.popitem()

  def remove(self, elt):
    # Removes an arbitrary element from the priority queue.
    # This allows updating a priority value for a key by
    # first removing it and then inserting it again with its
    # new priority value.
    del self.h[elt]  # invokes the __delitem__ method of heapdict.

  def getpriority(self, elt):
    return self.h[elt]

  def getEnqueuedElement(self, key):
    return self.h.getEnqueuedElement(key)

  def __len__(self):
    return len(self.h)

  def __contains__(self, elt):
    return elt in self.h

  def __str__(self):
    return 'PriorityQ'+str(self.h.d)

  def print_pq(self, name, priority_val_name):
    size = len(self)
    lst = self.h.heap
    # The following sorting is by priority value.
    # This is problem-independent.
    # It's needed because humans want to see the
    # priority queue as a sorted list, not as a 
    # semi-sorted binary heap.
    # The sorting might seem to undo the efficiency
    # gains of using the binary heap.  True, and if
    # that is an issue in some application, we just comment
    # out the call to this optional function that is for
    # the benefit of humans inspecting the alg's behavior.
    lst.sort(key=lambda t:t[0])
    print(name+" is now: ",end='')
    for idx,pq_item in enumerate(lst):
      if idx < size-1: 
        print(self.pq_item_str(pq_item, priority_val_name),end=', ')
      else:
        print(self.pq_item_str(pq_item, priority_val_name))

  def pq_item_str(self, pq_item, priority_val_name):
    '''Format one item from the priority queue.'''
    (p, s, i) = pq_item
    return str(s)+'('+priority_val_name+' = '+str(p)+')'
  

class LinkedList:
    value = None
    nxt = None
    
    def __init__(self, value_, nxt_):
        self.value = value_
        self.nxt = nxt_
   
# car - первый
def car(lst):
    return lst.value

# cdr - хвост
def cdr(lst):
    return lst.nxt

# cons - конструктор нового элемента
def cons(val, lst):
    return LinkedList(val, lst)

def isList(val):
    return isinstance(val, LinkedList)

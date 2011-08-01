#!/usr/bin/python2 -B
# -*- coding: utf-8 -*-

class Index(object):
    def __init__(self, iterable=(), key=None, cmp_=None):
        self.key = key or (lambda x: x)
        self.cmp = cmp_ or cmp
        
        self.list = list(sorted(iterable, key=self.key, cmp=self.cmp))
    
    def _bisect_right(self, x):
        lo, hi = 0, len(self.list)
        
        while lo < hi:
            mid = (lo+hi) // 2
            if self.cmp(x, self.key(self.list[mid])) < 0:
                hi = mid
            else:
                lo = mid+1
        return lo
    
    def _bisect_left(self, x):
        lo, hi = 0, len(self.list)
        
        while lo < hi:
            mid = (lo+hi) // 2
            if self.cmp(x, self.key(self.list[mid])) > 0:
                lo = mid+1
            else:
                hi = mid
        return lo

    def insert(self, x):
        self.list.insert(self._bisect_right(self.key(x)), x)
    
    def index(self, item):
        i = self._bisect_left(self.key(item))
        j = self._bisect_right(self.key(item))
        for i in range(i, j):
            if x is self.list[i]:
                return i
    
    def has_changed(self, item):
        self.remove(item)
        self.insert(item)

    def remove(self, item):
        i = self.index(item)
        if i == None:
            raise KeyError("Element does not exist")
        del self.list[i]
    
    def query(self, key=None, startkey=None, endkey=None, skip=None, limit=None, reverse=False, inclusive_end=True):
        if key is not None:
            startkey = key
            endkey = key

        if startkey is None:
            i = 0
        else:
            i = self._bisect_left(startkey)

        if endkey is None:
            j = len(self.list)
        else:
            if inclusive_end:
                j = self._bisect_right(endkey)
            else:
                j = self._bisect_left(endkey)
        
        if reverse:
            if skip is not None:
                j = max(j - skip, i)
            
            if limit is not None:
                i = max(j - limit, i)
            
            for x in range(j-1,i-1, -1):
                yield self.list[x]
                
        else:
            if skip is not None:
                i = min(i + skip, j)
            
            if limit is not None:
                j = min(i + limit, j)
            
            for x in range(i,j):
                yield self.list[x]
    

if __name__ == "__main__":
    from copy import deepcopy
    def testicle(text): #testtitle (testicle easier to type)
        print
        print
        print
        print "-"*20, text, "-"*20
    
    err = lambda x: x[1]
    test = Index(key = err)

    from random import randint

    lol = [[x, randint(1,10)] for x in range(10)]
    
    for x in lol:
        test.insert(x)
    
    #testicle("Original randomized list")
    #print lol
    #testicle("OrderedList Content")
    #print test.list

    testicle("Contains")
    print all([x in test for x in lol])

    testicle("Index")
    print all([test.list[test.index(x)] is x for x in lol])
    
    testicle("Remove (and deepcopy)")
    remtest = deepcopy(test)
    remlol = list(remtest.list)
    for x in remlol:
        remtest.remove(x)
    print remtest.list == []

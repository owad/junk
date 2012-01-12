#!/usr/bin/env python
#
from pprint import pprint, pformat
import random
import string

words = set(word for word in open('words.txt').read().split() if len(word) > 3)
results = dict()
try:
    print "Loading Word tree..."
    WordTree = eval(open('wordtree2.py').read(), {}, {})
    print "Loaded Word tree"
except Exception, e:
    print e
    print "Generating word tree..."
    WordTree = {} # This nested dictionary can be used to find word starts
    for word in words:
        d = WordTree
        for letter in word:
            letter = letter.lower()
            if letter not in d: d[letter] = {}
            d = d[letter]
        d['is_word'] = word
    open('wordtree2.py', 'w').write(pformat(WordTree))
    print "Generated word tree"

class Cell(object):
    def __init__(self, value): self._value = value

    def __call__(self): return self._value

    def __repr__(self): return self()


class Grid(object):
    def __init__(self, size=8):
        self._size = size
        self.content = [[Cell(random.choice(string.ascii_lowercase)) for x in range(size)] for y in range(size)]

    def __str__(self):
        return '\n'.join([' '.join([str(x) for x in y]) for y in self.content])


class Chain(object):
    def __init__(self, grid, (posx, posy)):
        self._chain = [grid.content[posx][posy]]
        self._grid = grid
        self._wordtree = WordTree.get(self._chain[-1]())
        self.cx = posx
        self.cy = posy

    def __str__(self):
        return ''.join([c() for c in self._chain])

    def next(self):
        return [x for x in self]

    def __iter__(self):
        for x in range(self.cx - 1, self.cx + 2):
            if x not in range(self._grid._size): continue
            for y in range(self.cy - 1, self.cy + 2):
                if y not in range(self._grid._size): continue
                potential = self._grid.content[x][y]
                if potential in self._chain: continue
                l = potential()
                if l not in self._wordtree:
                    if l == 'q' and 'u' in self._wordtree:
                        l == 'u'
                if l in self._wordtree:
                    newchain = ChainCopy(self, (x,y))
                    yield newchain
        return

class ChainCopy(Chain):
    def __init__(self, chain, (posx,posy)):
        """
        This replaces rather than enhances the init
        function of its superclass, acting as a copy
        constructor.
        """
        self._chain = [x for x in chain._chain]
        self._grid = chain._grid
        self.cx, self.cy = posx, posy
        self._chain.append(self._grid.content[posx][posy])
        self._wordtree = chain._wordtree.get(self._chain[-1]())
        word = self._wordtree.get('is_word')
        if word and word not in results:
            results[word] = word_score(word)

class Solver(object):
    def __init__(self, grid):
        self.grid = grid

    def rec(self, chains):
        for chain in chains:
            self.rec(chain.next())

    def solve(self):
        for x in range(self.grid._size):
            for y in range(self.grid._size):
                self.rec(Chain(self.grid, (x, y)))
def word_score(word):
    l = len(word)
    if l  < 3:
        return 0
    elif l == 3:
        return 1
    elif l < 8:
        return l - 3
    else:
        return 11
def get_score():
    score = sum(results.values())
    msg = "\nFound %d words out of a dictionary of %d, resulting in a score of %d points\n"%(len(results), len(words), score)
    print msg
    pprint(results)
    print msg

if __name__ == "__main__":
    print "\nGenerating grid\n"
    G = Grid(6)
    S = Solver(G)
    print G
    print "\nSolving:"
    S.solve()
    get_score()

#!/usr/bin/env python
#
from pprint import pprint, pformat
import random
import string

words = set(word for word in open('words.txt').read().split() if len(word) > 3)
results = dict()
try:
    print "Loading Word tree..."
    WordTree = eval(open('wordtree.py').read(), {}, {})
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
        d['is_word'] = True
    open('wordtree.py', 'w').write(pformat(WordTree))
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
                newchain = ChainCopy(self)
                newchain.add((x, y))
                if isWordStart(str(newchain)):
                    yield newchain
        return


def isWordStart(string_in):
    list_in = (letter for letter in string_in)
    string_out = ''
    d = WordTree
    for letter in list_in:
        if letter not in d:
            if string_out[-1] == 'q' and 'u' in d:
                string_out += 'u' + letter
                for letter in list_in: string_out += letter
                return isWordStart(string_out)
            else:
                return False
        string_out += letter
        d = d[letter]
    if 'is_word' in d and string_in not in results: results[string_in] = word_score(string_in)
    return True


class ChainCopy(Chain):
    def __init__(self, chain):
        """
        This replaces rather than enhances the init
        function of its superclass, acting as a copy
        constructor.
        """
        self._chain = [x for x in chain._chain]
        self._grid = chain._grid
        self.cx, self.cy = chain.cx, chain.cy

    def add(self, (posx, posy)):
        self.cx, self.cy = posx, posy
        self._chain.append(self._grid.content[posx][posy])


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
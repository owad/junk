#!/usr/bin/env python
#
from pprint import pprint
import random
import string

words = set(word for word in open('words.txt').read().split() if len(word) > 3)
results = set()

WordTree = {} # This nested dictionary can be used to find word starts
for word in words:
    d = WordTree
    for letter in word:
        if letter not in d: d[letter] = {}
        d = d[letter]
    d['is_word'] = True

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
    d = WordTree
    for letter in string_in:
        if letter not in d: return False
        d = d[letter]
    return True


def isLegalWord(string_in):
    if len(string_in) <= 3: return False
    if string_in in words: return True


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
        if isLegalWord(self.__str__()):
            if self.__str__() not in results:
                results.add(str(self))

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


if __name__ == "__main__":
    G = Grid(128)
    S = Solver(G)
    print G
    S.solve()

    print len(results), '/', len(words)
    pprint(results)
    print len(results), '/', len(words)
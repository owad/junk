class Cell(object):
  def __init__(self, value):
    self._value = value
  def __call__(self): return self._value

class Grid(object):
  def __init__(self, size=8):
	import random
	import string
	self._size = size
	self.content = [[Cell(random.choice(string.ascii_lowercase)) for x in range(size)] for y in range(size)]
  def __repr__(self):
	out_string = ''
	for y in self.content:
		out_string += ' '.join([x() for x in y]) + '\n'
	return out_string

class Chain(object):
  def __init__(self, grid, (posx, posy)):
    self._chain = [grid.content[posx][ posy]]
    self._grid = grid
    self.cx = posx
    self.cy = posy   

  def __str__(self):
    return ''.join([c() for c in self._chain])

  def partOfRealword(self, nextletter):
	return True
 
  def next(self):
	nextchains = []
	for x in range(self.cx-1, self.cx+2):
		if x not in range(self._grid._size): continue
		for y in range(self.cy-1, self.cy+2):
			if y not in range(self._grid._size): continue
			potential = self._grid.content[x][y]
			if potential in self._chain: continue
			# if not self.partOfRealword(potential()): continue
			newchain = ChainCopy(self)
			newchain.add((x,y))
			if isWordStart(newchain.__str__()):
				nextchains.append(newchain)
	return nextchains
words = set(open('words.txt').read().split())
results = set()
def isWordStart(string_in):
  for word in words:
    if len(word) < len(string_in): continue
    if word.startswith(string_in): return True
  return False
def isLegalWord(string_in):
  #print 'DEBUG: ', string_in
  #if len(string_in) > 8: exit
  if len(string_in) <= 3: return False
  if string_in in words: return True
class ChainCopy(Chain):
  def __init__(self, chain):
    self._chain = [x for x in chain._chain]
    self._grid = chain._grid
    self.cx, self.cy = chain.cx, chain.cy
    if isLegalWord(self.__str__()):
	if self.__str__() not in results:
            results.add(self.__str__())
            print self
  def add(self, (posx, posy)):
    self.cx, self.cy = posx, posy
    self._chain.append(self._grid.content[posx][posy])

class Solver(object):
	def __init__(self, grid):
		self.grid = grid
	def rec(self, chains):
		for chain in chains: self.rec(chain.next())
	def solve(self):
		"""import solution"""
		grid = self.grid
		for x in range(grid._size): 
			for y in range(grid._size):
				self.rec( Chain(self.grid, (x,y)).next() )
				
		

G = Grid(8)
S = Solver(G)
print G
S.solve()
print len(results)

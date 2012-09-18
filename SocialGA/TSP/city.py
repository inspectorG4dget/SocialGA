'''
Created on Sep 14, 2012

@author: ashwin
'''

from itertools import count
from collections import defaultdict
from math import sqrt
from pprint import pprint

class City:
	ID = count(1)
	def __init__(self, (X, Y)):
		self.id = self.ID.next()
		self.x = float(X)
		self.y = float(Y)
		
	def __hash__(self):
		return hash(self.id)
	
	def __repr__(self):
		return str(self.id)
	
	def __eq__(self, other):
		if isinstance(other, City): return self.id == other.id
		elif isinstance(other, int): return self.id == other

def getCities(fpath):
	
	cities = []
	for line in open(fpath):
		cities.append(City(line.strip(",\n").split(',')))
	return cities

def dist(source, dest):
	return sqrt((source.x-dest.x)**2 + (source.y-dest.y)**2)

def getAdjMatrix(cities):
	answer = defaultdict(dict)
	for source in cities:
		for dest in cities:
			if source != dest:
				answer[source][dest] = dist(source, dest)
	
	return answer

if __name__ == "__main__":
	print 'starting'
	
	cities = getCities('berlin52.txt')
	dists = getAdjMatrix(cities)
	pprint(dict(dists))
	
	print 'done'
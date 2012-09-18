'''
Created on Sep 14, 2012

@author: ashwin
'''

import pygame as pg
import draw
import substring as subs
from city import *

from random import sample, random as rand, choice as choose, shuffle as shaker
from itertools import permutations as perms, chain
from math import sqrt
from sys import exit as crash
from pprint import pprint

def initPop(N, numcities):
	answer = set()
	popsize = 0
	while popsize != N:
		p = tuple(sample(range(1, numcities+1), numcities))
		if p not in answer:
			answer.add(p)
			popsize += 1
	
	return answer

def score(tour, DIST):
#	print type(tour[0]); crash()	##
#	print "tour:", tour	##
	answer = 0
	numcities = len(tour)
	for i,source in enumerate(tour):
		dest = tour[(i+1)%numcities]
		answer += DIST[source.id][dest.id]
	return answer

def simselect(p, pop, simLow, simHigh, MATCHES):
	for _ in xrange(10):
		try:
			return next(i for i in pop if simLow <= subs.similarity(p, i, MATCHES) <= simHigh)
		except:
			pass
	return p

def pmapco(p1, p2):
	""" Partially Mapped Crossover, from the handout """
	
#	print "p1:", p1	##
#	print "p2:", p2	##
	
	numcities = len(p1)
	a,b = sample(range(numcities), 2)
	if a > b: a,b = b,a
	
#	print "a,b:", a,b	##
	answer = [None for _ in xrange(numcities)]
	
	for i in xrange(a, b+1): answer[i] = p1[i]	# copy over p1 genes to the answer
	
	for i in chain(xrange(a), xrange(b+1, numcities)):
		if p2[i] not in answer: answer[i] = p2[i]
	
	remainder = (i for i in xrange(1, numcities+1) if i not in answer)
	for i, city in enumerate(answer):
		if city==None:
			answer[i] = cities[next(remainder)]
	
#	print "*"*40	##
#	print p1	##
#	print p2	##
#	print a,b	##
#	print "pmap answer:", answer	##
	return answer

def injectionco(p1, p2):
	""" Order CrossOver from the handout """
	
	answer = []
	a,b = sample(range(len(p1)), 2)
	if a < b: a,b = b,a
	q = choose(range(len(p1)))
	
	ab = p1[a:b]
	for i in xrange(q):
		if p2[1] not in ab: answer.append(p2[i])
	answer.extend(ab)
	for city in p2:
		if city not in answer: answer.append(city)
	
	return answer

def swapmut(p, mutprob):
	""" Pick any two random cities and swap their positions in the tour """
#	i,j = sample(range(len(p)), 2)
#	if rand() <= mutprob: p[i], p[j] = p[j], p[i]
	for i in range(len(p)):
		if rand() <= mutprob:
			j = choose([ii for ii in range(len(p)) if ii != i])
			p[i], p[j] = p[j], p[i]
	return p

def revmut(p, mutprob):
	""" Choose a random pair of points on the chromosome.
		Reverse the order of the genes between those two points on the chromosome """
#	print 'p:', p	##
	if rand() <= mutprob:
		answer = []
		a,b = sample(range(len(p)), 2)
		if a>b: a,b = b,a
#		print 'rev a,b:', a,b
		answer.extend(p[:a])
		answer.extend(p[a:b+1][::-1])
		answer.extend(p[b+1:])
#		print 'rev answer:', answer	##
		return answer
	else:
		return p
def swaprevmut(p, threshold, mutprob):
	if rand() <= mutprob:
		a = choose(range(len(p)))
		b = choose([i for i in range(max(0, a-threshold), min(a+threshold, len(p))) if i!=a])
		if a>b: a,b = b,a
		return p[:a] + p[a:b+1][::-1] + p[b+1:]
	else:
		return p

def revswapmut(p, threshold, mutprob):
	p = p[:]
	for a in xrange(len(p)):
		if rand() <= mutprob:
			a = choose(range(len(p)))
			b = choose([i for i in range(max(0, a-threshold), min(a+threshold, len(p))) if i!=a])
			p[a], p[b] = p[b], p[a]
	
	return p

def shufflemut(p, mutprob):
	if rand() <= mutprob:
		shaker(p)
	return p

def kill(pop, popsize, DIST):

	pop.sort(key=lambda p: score(p, DIST))
	return pop[:popsize]

def runGA(cities, initFunc, initSize, selectFunc, selectParams, coFunc, scoreFunc, mutateFunc, mutparams, killFunc, maxGen, targetScore):
	
	window = draw.makescreen()
	g = 0
	pop = initFunc(initSize, len(cities))
	pop = map(lambda tour: [cities[i] for i in tour], pop)
	best = min(pop, key=lambda p: scoreFunc(p, DIST)); bestsofar='',None
	print 'Best:', scoreFunc(best, DIST)	##
	draw.draw(best, g, window, DIST)
	
	while g <= maxGen and bestsofar[0] > targetScore:
		children = []
		for p in pop:
#			if not _%10: print _,	##
#			print 'sel',	##
			mate = selectFunc(p, pop, *selectParams)
#			print '/sel',	##
			children.append(mutateFunc(coFunc(p[:], mate[:]), *mutparams))
			children.append(mutateFunc(coFunc(mate[:], p[:]), *mutparams))
			
#		print set((scoreFunc(c) for c in children))	##
#		pop = killFunc(pop, children)
		pop = kill(pop+children, initSize, DIST)
		g += 1
#		best = max((scoreFunc(p) for p in pop))
		best = min(pop, key=lambda p: scoreFunc(p, DIST))
		if scoreFunc(best, DIST) < bestsofar[0]:
			bestsofar = scoreFunc(best, DIST), best
			window = draw.makescreen()
			pg.display.init(); draw.draw(bestsofar[1], g, window, DIST)
#		if not g%10: print g, scoreFunc(best), "|", bestsofar[0]	##
		print g, scoreFunc(best, DIST), "|", bestsofar[0], len(set((c.id for c in bestsofar[1])))	##
	
	raw_input("Hit <ENTER> to continue")
	return bestsofar[0]

if __name__ == "__main__":
	print 'starting'
	
	b52 = 'berlin52.txt'
	cities = dict(((c.id, c) for c in getCities(b52)))
	DIST = getAdjMatrix(cities.values())
	MATCHES = {}
	
	runGA(cities, initFunc=initPop, initSize=500, selectFunc=simselect, selectParams=(0.1, 0.4, MATCHES), coFunc=pmapco,
			scoreFunc=score, mutateFunc=revmut, mutparams=(0.05,), killFunc=kill, maxGen=500, targetScore=7600)
#		scoreFunc=score, mutateFunc=revswapmut, mutparams=(20, 0.05,), killFunc=kill, maxGen=1000, targetScore=7542)

#	p = [9, 37, 44, 20, 32, 25, 15, 13, 28, 41, 50, 3, 29, 22, 27, 23, 38, 21, 12, 46, 40, 35, 24, 31, 8, 14, 6, 36, 10, 48, 11, 51, 16, 33, 17, 52, 45, 43, 2, 1, 34, 18, 7, 30, 19, 5, 26, 42, 49, 39, 47, 4]
#	revmut(p, 2)
	print 'done'

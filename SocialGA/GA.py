'''
Created on Sep 12, 2012

@author: ashwin
'''

from random import choice as choose, randint, uniform as randfloat, sample as sample

def genPop(N, G):
	"""Return a population of N individuals. Each individual has G chromosomes"""
	
	answer = set()
	while N:
		indiv = ''.join(choose('01') for _ in range(G))
		if indiv not in answer:
			N -= 1
			answer.add(indiv)
	
	return list(answer)

def crossover(p1, p2, crossprob):
	G = len(p1)
	crosspoint = randint(0,G-1)
	
	if randfloat(0,1) <= crossprob:
		c1 = p1[:crosspoint] + p2[crosspoint:]
		c2 = p2[:crosspoint] + p1[crosspoint:]
		return c1, c2
	else:
		return p1, p2

def mutate(p, mutprob):
	answer = []
	for g in p:
		if randfloat(0,1) <= mutprob:
			answer.append((int(g) +1) %2)
		else:
			answer.append(g)
	
	return ''.join(str(i) for i in answer)

def canMate(p, m, simLims, diffLims):
	pm = zip(p,m)
	sim = sum(1 for i,j in pm if i==j)/float(len(p))
	diff = sum(1 for i,j in pm if i!=j)/float(len(p))
	
	return simLims[0] <= sim <= simLims and diffLims[0] <= diff <= diffLims

def findMate(p1, pop, simLims, diffLims):
#	prospects = [p for p in pop if canMate(p1, p, simLims, diffLims)]
	try:
		return next(p for p in pop if canMate(p1, p, simLims, diffLims))
	except:
		return None

def score(p, scores):
	if p not in scores:
		scores[p] = p.count('1')/float(len(p))
	return scores[p]

def kill(pop, popSize, scores):
	pop.sort(key=lambda p: score(p, scores), reverse=True)
#	return sample(pop[:int(popSize*0.67)], popSize/2) + sample(pop[-int(popSize*0.67):], popSize/2)
#	return pop[:popSize/2] + pop[-popSize/2:]
	return pop[:popSize]
#	q = len(pop)/popSize
#	start = choose(range(q))
#	return pop[start::q]

def runGA(popSize, chromSize, crossProb, mutprob, maxGens, simLims, diffLims, targetFitnes, scores={}):
	pop = genPop(popSize, chromSize)
	fittest = max(pop, key=lambda p: score(p, scores))
	topscore = score(fittest, scores)
	print 0, "fittest: %s\t%s" %(fittest, topscore), "p", len(pop)
	
	for g in xrange(1,maxGens+1):
		print g,
		newPop = []
		for p1 in pop:
			p2 = None
			tries = 10
			while p2 is None and tries:
				p2 = findMate(p1, sample(pop, popSize/2), simLims, diffLims)
				tries -= 1
			if not p2: p2=p1
			children = [mutate(c, mutprob) for c in crossover(p1, p2, crossProb)]
			newPop.extend(sample(children, 2))
		pop = kill(newPop+pop, popSize, scores)
		fittest = max(pop, key=lambda p: score(p, scores))
		topscore = score(fittest, scores)
		print "fittest: %s\t%s" %(fittest, topscore), "p", len(pop)
		if topscore >= targetFitnes:
			return fittest, g
	return fittest, g

if __name__ == "__main__":
	print 'starting'
	
	trials = 30
	results = []
	for t in xrange(1, trials+1):
		print 'TRIAL', t
		results.append(runGA(popSize=1000, chromSize=30, crossProb=0.9, mutprob=0.1, maxGens=100, simLims=(0.35, 0.60), diffLims=(0.25, 0.40), targetFitnes=1.0)[1])
		print '='*80

	results.sort()
	print "*"*30
	print results
	print "average:", sum(results)/float(trials)
	print "*"*30
	
	
	
	print 'done'
'''
Created on Sep 17, 2012

@author: ashwin
'''

from itertools import product as cross

def makeMatrix(s1, s2):
	pairs = list(cross(s1, s2)); length = len(s1)
	pairs = [pairs[length*i:length*(i+1)] for i in xrange(length)]
	answer = [[0 for _ in xrange(len(s2)+1)] for _ in xrange(len(s1)+1)]
	
	for r, row in enumerate(answer[1:], 1):
		for c, _ in enumerate(row[1:], 1):
#			if len(set(pairs[((r-1)*len(s1))  +c-1])) >1:
			if len(set(pairs[r-1][c-1])) >1:
				row[c] = 0
			else:
				row[c] = answer[r-1][c-1]+1
	
	return answer

def similarity(s1, s2, MATCHES):
	fs = frozenset(s1,s2)
	if fs not in MATCHES:
		matrix = makeMatrix(s1, s2)
		answer = max(i for m in matrix for i in m)/float(len(s1))
		MATCHES[fs] = answer
	return MATCHES[fs]

if __name__ == "__main__":
	print similarity('abab', 'baba')
'''
Created on Sep 14, 2012

@author: ashwin
'''

import pygame as pg
import city
from random import shuffle
from time import sleep
import TSP as tsp

def makescreen(W=640, H=640):
	pg.init()
	window = pg.display.set_mode((W, H))
	return window

def normalize(point, (olow, ohigh), (low, high)):
	return low + ((point/(ohigh-olow)) * (high-low))

def draw(tour, gen, window, DIST):
	
	fon = pg.font.SysFont('monospace', 15)
	fon = fon.render("%s/%s %s: %s "%(len(set((c.id for c in tour))), len(tour), gen, tsp.score(tour, DIST)), False, (0,255,255))
	window.blit(fon, (300,600))
	pg.display.init()
	
	numcities = len(tour)
	for i, source in enumerate(tour):
		dest = tour[(i+1) %numcities]
		x,a = map(lambda x: normalize(x, (0.0,1800.0), (0,640)), [source.x, dest.x])
		y,b = map(lambda x: normalize(x, (0.0,1200.0), (0,640)), [source.y, dest.y])
		
		pg.draw.circle(window, (255,0,0), (int(x),int(y)), 3, 0)
		pg.draw.line(window, (255,255,255), (x,y), (a,b))
	
	pg.display.flip()
	return None

def killscreen():
	pg.display.quit()
	return None

if __name__ == "__main__":
	print 'starting'
	
	window = makescreen()
	cities = city.getCities('berlin52.txt')
	shuffle(cities)
	draw(cities, window)
	sleep(5)
	window = makescreen()
	shuffle(cities)
	draw(cities, window)
	sleep(5)
	killscreen()
#	print normalize(point, (olow, ohigh), (low, high))
	
	print 'done'
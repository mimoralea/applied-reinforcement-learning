# tile timing tests
import random
random.seed(65597)

import tiles
import tilesn
import timeit

def runit (num=10, ct=2048, numt=1):
    for i in xrange(num):
        for j in xrange(num):
            t = tiles.tiles(numt, ct, [i*0.5, j*0.5])
def runitn (num=10, ct=2048, numt=4):
    for i in xrange(num):
        for j in xrange(num):
            t = tilesn.tiles(numt, ct, [i*0.5, j*0.5])
def runit2 (num=10, ct=2048, numt=1):
    for i in xrange(num):
        for j in xrange(num):
            t = tiles.tiles(numt, ct, [i*0.5, j*0.5, float(i+j)/2, float(i-j)/2], [i, j])
def runitw (num=10, ct=2048, numt=1):
    for i in xrange(num):
        for j in xrange(num):
            t = tiles.tileswrap(numt, ct, [i*0.5, j*0.5], [10, 1])
def runitl (num=10, ct=2048, numt=1):
    tlist = [None for i in range(num*num*numt)]
    for i in xrange(num):
        for j in xrange(num):
            t = tiles.loadtiles(tlist, i*num*numt+j, numt, ct, [i*0.5, j*0.5])
def runitlw (num=10, ct=2048, numt=1):
    tlist = [None for i in range(num*num*numt)]
    for i in xrange(num):
        for j in xrange(num):
            tiles.loadtileswrap(tlist, i*num*numt+j, numt, ct, [i*0.5, j*0.5], [10, 1])
    return tlist

def initct(mem=16384):
    global ctu, cts, ctss
    ctu=tiles.CollisionTable(mem, safetyval='unsafe')
    cts=tiles.CollisionTable(mem, safetyval='safe')
    ctss=tiles.CollisionTable(mem, safetyval='super safe')

def timetest(command, info, info2='2 floats', num=100, numt=1, mem=16384):            
    initct(mem)
    print " "
    print info
    print "Timing over", num*num, "calls to tiles,", numt, "tiling each for", info2
    t= timeit.Timer(command + '('+str(num)+','+str(mem)+','+str(numt)+')', 'from __main__ import ' + command)
    print "With no collision table", t.timeit(1), "seconds"
    t= timeit.Timer(command + '('+str(num)+', ctu'+','+str(numt)+')', 'from __main__ import ctu, ' + command)
    print "With unsafe collision table", t.timeit(1), "seconds"
    print ctu
    t= timeit.Timer(command + '('+str(num)+', cts'+','+str(numt)+')', 'from __main__ import cts, ' + command)
    print "With safe collision table", t.timeit(1), "seconds"
    print cts
    t= timeit.Timer(command + '('+str(num)+', ctss'+','+str(numt)+')', 'from __main__ import ctss, ' + command)
    print "With super safe collision table", t.timeit(1), "seconds"
    print ctss
    print " "
    print "Timing over", num*num, "calls to tiles, 16 tilings each for", info2
    t= timeit.Timer(command + '('+str(num)+', 16384, 16)', 'from __main__ import ' + command)
    print "With no collision table", t.timeit(1), "seconds"

timetest('runit', "Standard test", numt=4)
timetest('runit2', 'Testing with more input variables','4 floats, 2 ints', 100, 3, 32768)
timetest('runitw', 'WRAP version', numt=4)
timetest('runitl', 'Load version', '2 floats', 100, 4) # only do 10 x 10 calls, but with 4 tilings each
timetest('runitlw', 'Load WRAP version', '2 floats', 100, 4)

"""
print " "   
print "Tiles with num array"
ctu=tilesn.CollisionTable(16384, safetyval='unsafe')
cts=tilesn.CollisionTable(16384, safetyval='safe')
ctss=tilesn.CollisionTable(16384, safetyval='super safe')
print "Timing over 10000 calls to tiles with numarray, 4 tiling each for 2 floats"
t= timeit.Timer('runitn(100, 16384)', 'from __main__ import runitn')
print "With no collision table", t.timeit(1), "seconds"
t= timeit.Timer('runitn(100, ctu)', 'from __main__ import runitn, ctu')
print "With unsafe collision table", t.timeit(1), "seconds"
print ctu
t= timeit.Timer('runitn(100, cts)', 'from __main__ import runitn, cts')
print "With safe collision table", t.timeit(1), "seconds"
print cts
#t= timeit.Timer('runitn(100, ctss)', 'from __main__ import runitn, ctss')
#print "With super safe collision table", t.timeit(1), "seconds"
#print ctss     # need different array comparisons for super safe
print " "
print "Timing over 10000 calls to tiles with numarray, 16 tilings each for 2 floats"
t= timeit.Timer('runitn(100, 16384, 16)', 'from __main__ import runitn')
print "With no collision table", t.timeit(1), "seconds"
"""



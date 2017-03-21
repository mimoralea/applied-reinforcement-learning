"""    fancytiles - alternate sizes and shapes of tiles

The tiles routine in the tiles module assumes tiles that are uniform squares of size 1. By
doing some transformations on the numbers before going into the tiles routine, you can get the
effect of different sizes, non uniform sizes, and different shapes.

Here are some transformation routines to get different tile effects. You may
apply both size changing and shape changing routines to get the effect you want.

Tile size transformations:
    scalefloats(floats, scalewidths)
        Scales the floats so that their tiles will have the widths specified
        by scalewidths. If you do not wish a particular dimension to have its
        scale changed, use 1 for that element.
    logfloats(floats)
        manipulates the floats so that their tiles are logarithmic sizes (small
        to large) in each dimension of floats
    expfloats(floats)
        manipulates the floats so that their tiles are exponential sizes (large
        to small) in each dimension of floats

Tile shape transformations:
    diagonalstripe(floats)
        For 2 dimensions only. Returns a single number that is the difference
        between the two numbers. This gives diagonal stripe tiles (from top
        left to botton right).
    backdiagonalstripe(floats)
        For 2 dimensions only. Returns a single number that is the sum of the
        two numbers. This gives backwards diagonal stripe tiles (from top right
        to bottom left).
    diagonalfloats(floats)
        For any number of dimensions > 1. Does pairwise diagonalstripe calls.
        Returns a smaller number of floats than originally called with.
    backdiagonalfloats(floats)
        For any number of dimensions > 1. Does pairwise backdiagonalstripe calls.
        Returns a smaller number of floats than originally called with.
    diamondfloats(floats)
        Returns a new set of floats with exactly two numbers - one for a diagonal
        stripe and one for a back diagonal stripe. This creates tiles with a
        diamond shape.

After manipulating your floats with these routines, you can then call the tiles
functions to get the actual tiles.

Instead, you may call one of the following routines to do the manipulations and
call tiles for you:

To get tiles of different sizes:
    scaletiles(numtilings, memctable, floats, widths, ints=[])
        returns tiles for the given parameters which are of the sizes given by widths
    logtiles(numtilings, memctable, floats, ints=[])
        returns logarithmic sized tiles for the given parameters
    exptiles(numtilings, memctable, floats, ints=[])
        returns exponential sized tiles for the given parameters

To get tiles of different shapes (and possibly sizes):
    stripetiles(numtilings, memctable, floats, widths=None, ints=[])
        calls tiles for each number in floats separately and combines all the
        tiles into one list. If widths is specified, the tiles are scaled first
        according to those sizes.
    diagonaltiles(numtilings, memctable, floats, widths=None, ints=[])
        returns tiles corresponding to diagonal stripes for the given parameters.
        If widths is specified, the tiles are scaled first according to those sizes.
    backdiagonaltiles(numtilings, memctable, floats, widths=None, ints=[])
        returns tiles corresponding to back diagonal stripes for the given parameters.
        If widths is specified, the tiles are scaled first according to those sizes.
    diamondtiles(numtilings, memctable, floats, widths=None, ints=[])
        returns diamond shaped tiles for the given parameters.
        If widths is specified, the tiles are scaled first according to those sizes.
    
There is also a routine that tries to do it all for you.

    fancytiles(numtilings, floats, tileshape="square", tilesize="uniform", \
               tilewidths=None, memctable=2048, ints=[]):
       Does appropriate manipulations to get special shaped or sized tiles, and
       calls tiles for you to get them.
       Tileshapes are 'square' - square or rectangular tiles (the default),
                      'stripe' - stripes for each dimension, and
                      'diagonal' - diagonal stripes for each pair of dimensions
                      'backdiagonal' diagonal stripes the other way
                      'alldiagonal' - diagonal stripes for all dimensions at once
                      'allbackdiagonal' - diagonal stripes the other way for all dimensions at once
                      'diamond' - diagonal stripes and back diagonal stripes are applied
       Tilesizes are 'uniform' - all tiles are the same size (the default), 
                     'log' - tile sizes vary logarithmically from small to large, and
                     'exp' - tile sizes vary exponentially from large to small
       Scaling is handled first if tilewidths is set - there should be a width for every
       element of the float vector. If you don't wish to apply scaling to the floats,
       tilewidths may be set to None, or to a vector of 1's the same length as floats.
       memctable, numtilings and ints are the same as for the regular tiles routine.
       Note that you may get back more tiles than numtilings - for stripes or diagonal stripes
       you may get a larger number of tiles back.
"""

import math
import operator
import tiles
import random

# Routines to change the tile sizes

def scalefloats (floats, scalewidths=None):
    "Scales floats so that their tiles will have the given widths"
    if scalewidths != None and len(scalewidths) == len(floats):
        l = []
        for v, w in zip(floats, scalewidths):
            l.append(float(v) / w)
        return l
    else:
        return floats

def logfloats (floats):
    """Manipulates floats so that their tiles are logarithmic sizes 
       small to large"""
    # must ensure that none of the floats are 0 or less
    flist = floats[:]
    for i in xrange(len(flist)):
        if flist[i] <= 0:
            flist[i] = .0000001
    return [math.log(i) for i in flist]

def expfloats (floats):
    """Manipulates floats so that their tiles are logarithmic sizes 
       large to small"""
    return [math.exp(i) for i in floats]

# Routines to change the tile shapes

def diagonalfloats (floats):
    """Manipulate floats so that you get diagonal stripes for tiles - does
       pairwise subtraction. Returns a different sized list than the original.
    """
    l = []
    flist = floats[:]
    while len(flist) > 1:
        current = flist[0]
        for next in flist[1:]:
            l.extend(diagonalstripe([current, next]))
        flist = flist[1:]
    return l

def backdiagonalfloats (floats):
    """Manipulate floats so that you get backwards diagonal stripes for tiles - does
       pairwise addition. Returns a different sized list than the original.
    """
    l = []
    flist = floats[:]
    while len(flist) > 1:
        current = flist[0]
        for next in flist[1:]:
            l.extend(backdiagonalstripe([current, next]))
        flist = flist[1:]
    return l

def backdiagonalstripe (floats):
    "For two dimensions only"
    return [round(floats[0] + floats[1], 1)]

def diagonalstripe (floats):
    "For two dimensions only"
    return [round(floats[0] - floats[1], 1)]

# Fancy tile routines - some examples using the above transformations to get different tile shapes
# and sizes

def scaletiles (numtilings, memctable, floats, widths=None, ints=[]):
    "returns tiles scaled by widths"
    floats = scalefloats(floats, widths)
    return tiles.tiles(numtilings, memctable, floats, ints)

def logtiles (numtilings, memctable, floats, ints=[]):
    "returns tiles which vary in size logarithmically from small to large"
    floats = logfloats(floats)
    return tiles.tiles(numtilings, memctable, floats, ints)

def exptiles (numtilings, memctable, floats, ints=[]):
    "returns tiles which vary in size exponentially from large to small"
    floats = expfloats(floats)
    return tiles.tiles(numtilings, memctable, floats, ints)

def stripetiles(numtilings, memctable, floats, widths=None, ints=[]):
    "returns tiles in the shape of stripes (scaled by widths), a set for each dimension in floats"
    floats = scalefloats(floats, widths)
    # should another int be added here for each dimension if there is more than one?
    return reduce(operator.add, [tiles.tiles(numtilings, memctable, [f], ints) for f in floats])

def diagonaltiles(numtilings, memctable, floats, widths=None, ints=[]):
    "returns tiles in the shape of diagonal stripes"
    floats = scalefloats(floats, widths)
    floats = diagonalfloats(floats)
    return stripetiles(numtilings, memctable, floats, ints)

def backdiagonaltiles(numtilings, memctable, floats, widths=None, ints=[]):
    "returns tiles in the shape of backward diagonal stripes"
    floats = scalefloats(floats, widths)
    floats = backdiagonalfloats(floats)
    return stripetiles(numtilings, memctable, floats, ints)

def diamondtiles(numtilings, memctable, floats, widths=None, ints=[]):
    "returns tiles in the shape of diamonds"
    floats = scalefloats(floats, widths)
    floats1 = diagonalfloats(floats)
    floats2 = backdiagonalfloats(floats)
    return tiles.tiles(numtilings, memctable, floats1+floats2, ints)


def fancytiles(numtilings, floats, tileshape="square", tilesize="uniform", \
               tilewidths=None, memctable=2048, ints=[]):
    """Does appropriate manipulations to get special shaped or sized tiles.
       Tileshapes are 'square' - square or rectangular tiles (the default),
                      'stripe' - stripes for each dimension, and
                      'diagonal' - diagonal stripes for each pair of dimensions
                      'backdiagonal' diagonal stripes the other way
                      'alldiagonal' - diagonal stripes for all dimensions at once
                      'allbackdiagonal' - diagonal stripes the other way for all dimensions at once
                      'diamond' - diagonal stripes and back diagonal stripes are applied
       Tilesizes are 'uniform' - all tiles are the same size (the default), 
                     'log' - tile sizes vary logarithmically from small to large, and
                     'exp' - tile sizes vary exponentially from large to small
       Scaling is handled first if tilewidths is set - there should be a width for every
       element of the float vector. If you don't wish to apply scaling to the floats,
       tilewidths may be set to None, or to a vector of 1's the same length as floats.
       memctable, numtilings and ints are the same as for the regular tiles routine.
       Note that you may get back more tiles than numtilings - for stripes or diagonal stripes
       you may get a larger number of tiles back.
    """
    if tilewidths != None:                  # apply scaling, if desired
            floats = scalefloats(floats, tilewidths)
    if tilesize == "log":                   # logarithmic sized tiles
        floats = logfloats(floats)
    elif tilesize == "exp":                 # exponential sized tiles
        floats = expfloats(floats)
        
    if tileshape == "stripe":               # stripes - do one set for each variable in floats
        return reduce(operator.add, [tiles.tiles(numtilings, memctable, [f], ints) for f in floats])
    elif tileshape == "diagonal":           # diagonal stripes for every pair of dimensions
        flist = floats[:]
        tlist = []
        while len(flist) > 1:
            current = flist[0]
            for next in flist[1:]:
                tlist.extend(tiles.tiles(numtilings, memctable, diagonalstripe([current, next]), ints))
            flist = flist[1:]
        return tlist
    elif tileshape == "backdiagonal":       # diagonal stripes for every pair of dimensions
        flist = floats[:]
        tlist = []
        while len(flist) > 1:
            current = flist[0]
            for next in flist[1:]:
                tlist.extend(tiles.tiles(numtilings, memctable, backdiagonalstripe([current, next]), ints))
            flist = flist[1:]
        return tlist
    elif tileshape == "alldiagonal":        # diagonal stripe through all dimensions at once - no different than diag?
        return tiles.tiles(numtilings, memctable, diagonalfloats(floats), ints)
    elif tileshape == "allbackdiagonal":    # diagonal stripe through all dimensions at once
        return tiles.tiles(numtilings, memctable, backdiagonalfloats(floats), ints)
    elif tileshape == "diamond":            # diamond shaped tiles 
        floats1 = diagonalfloats(floats)
        floats2 = backdiagonalfloats(floats)
        return tiles.tiles(numtilings, memctable, floats1+floats2, ints)
    else:                                   # square/rectangular - do the regular tiles
        return tiles.tiles(numtilings, memctable, floats, ints)
   
"""
for i in xrange(10):
    print "reg",i, [fancytiles(1,[float(i), float(j)]) for j in xrange(10)]
    print "diamond", i, [fancytiles(1,[float(i), float(j)], 'diamond') for j in xrange(10)]
    print "diagonal", i, [fancytiles(1,[float(i), float(j)], 'diagonal') for j in xrange(10)]
    print "stripes", i, [fancytiles(1,[float(i), float(j)], 'stripe') for j in xrange(10)]
    print "expstripes", i, [fancytiles(1,[float(i), float(j)], 'stripe', 'exp') for j in xrange(10)]
    print "logstripes", i, [fancytiles(1,[float(i), float(j)], 'stripe', 'log') for j in xrange(10)]
"""

"""
print "diagonaltiles", diagonaltiles(1, 2048, [1.2, 7.5, 3.8])
print "fancy diagonaltiles", fancytiles(1,[1.2, 7.5, 3.8], 'diagonal')
print "fancy alldiagonaltiles", fancytiles(1,[1.2, 7.5, 3.8], 'alldiagonal')

print "diagonaltiles", diagonaltiles(5, 2048, [1.2, 7.5])
print "fancy diagonaltiles", fancytiles(5,[1.2, 7.5], 'diagonal')
print "fancy alldiagonaltiles", fancytiles(5,[1.2, 7.5], 'alldiagonal')
"""

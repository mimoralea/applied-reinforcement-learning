This folder contains the C version of tile coding, as well as the python routines which call the c version of tiles.

The following files are here:

Makefile - compiles both the C version and the Python->C version (for Mac)
tiles.h - header for C version of tiles
tiles.cpp - c++ version of tiles
tiletimes.cpp - timing code for c calling c version of tiles
tilesInt.C - interface so that Python can call the c version
tiletimes.py - timing code for the python calling c version of tiles
fancytiles.py - code to get different shapes and sizes of tiles
tilesdemo.py - illustration and testing demo for tiles
tilesdemocomp.py - the tiles demo modified to compare the python and c versions

To use these:
In a terminal window:
move to the directory ...RLtoolkit/CTiles
make
... this creates the tiles.so and tiles.o files

From python, you can now import RLtoolkit.CTiles.tiles to use the c tile functions

To run the timing code for the c version (c calling c)
c++ -o tilestest tiletimes.cpp tiles.cpp
./tilestest


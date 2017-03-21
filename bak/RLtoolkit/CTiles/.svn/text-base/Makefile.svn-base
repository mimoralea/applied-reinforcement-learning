.PHONY : tiles

tiles: tiles.so

tilesInt.o: tilesInt.C
	c++ -fno-strict-aliasing -Wno-long-double -no-cpp-precomp -mno-fused-madd -fno-common -dynamic -DNDEBUG -g -O3 -Wall -Wstrict-prototypes -I/System/Library/Frameworks/Python.framework/Versions/2.3/include/python2.3 -c tilesInt.C -o tilesInt.o

tiles.o: tiles.cpp
	c++ -fno-strict-aliasing -Wno-long-double -no-cpp-precomp -mno-fused-madd -fno-common -dynamic -DNDEBUG -g -O3 -Wall -Wstrict-prototypes -I/System/Library/Frameworks/Python.framework/Versions/2.3/include/python2.3 -c tiles.cpp -o tiles.o

tiles.so: tiles.o tilesInt.o
	c++ -Wl,-F. -Wl,-F. -bundle -framework Python tiles.o tilesInt.o -o tiles.so

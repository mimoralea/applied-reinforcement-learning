# G tests
from RLtoolkit.g import *

w = Gwindow(gdViewport=(0,20,600,420))
gClear(w, 'yellow')

v1 = Gview(w)
gdSetViewport(v1, 0, 0, 200, 400)
gClear(v1, 'green')
v2=Gview(w)
gdSetViewportR(v2, 200, 0, 100, 200)
gClear(v2, 'blue')

for i in range(10):
    gdDrawPoint(v1, 50+i, 30, 'red')
gdDrawLine(v1, 49, 49, 20, 120, 'black')
gdDrawLineR(v1, 20, 120, 150, 0, 'purple')
gdDrawLine(v1, 170, 120, 49, 49, 'yellow')
gdOutlineRect(v1, 100, 200, 150, 250, 'pink')
gdOutlineRectR(v1, 100, 300, 60, 80, 'magenta')

gdFillRect(v2, 10, 10, 50, 100, 'orange')
gdFillRectR(v2, 40, 100, 40, 60, 'light blue')
gdFillRect(v2, 0, 0, 10,10, 'white')
print(gdGetCS(v2))


gStartEventLoop()

# G tests - color and font
from RLtoolkit.g import *

w = Gwindow(gdViewport=(0,20,600,800))

# named colors
colors = ['black', 'white', 'pink', 'red', 'orange', 'yellow', 'green', \
          'dark green', 'light blue', 'blue', 'purple', 'brown', 'tan', \
          'light gray', 'gray', 'dark gray', 'cyan', 'magenta']
i = 0
for c in colors:
    gdFillRect(w, i, 0, i+20, 20, c)
    i += 20

gdDrawLine(w, 0, 21, 600, 21)

# colors globals
colors = [gBlack, gWhite, gPink, gRed, gOrange, gYellow, gGreen, \
          gDarkGreen, gLightBlue, gBlue, gPurple, gBrown, gTan, \
          gLightGray, gGray, gDarkGray, gCyan, gMagenta]

i = 0
j = 22
for c in colors:
    gdFillRect(w, i, j, i+20, j+20, c)
    i += 20

gdDrawLine(w, 0, 43, 600, 43)

# Now try calculating shades of one color given intensity in 256 range (red)
i = 0
j = 44
for c in range(256):
    col = gColorRGB255(w, 255, 255-c, 255-c)
    gdFillRect(w, i, j, i+20, j+20, col)
    i+=20
    if i > 580:
        i = 0
        j +=20

j+=21
gdDrawLine(w, 0, j, 600, j)

# Now try calculating black and white shades
i = 0
j +=1
for c in range(256):
    col = gColorBW(w, float(c) / 256)
    gdFillRect(w, i, j, i+20, j+20, col)
    i+=20
    if i > 580:
        i = 0
        j +=20

j+=21
gdDrawLine(w, 0, j, 600, j)

# Now try calculating shades of one color with intensities 0-1 (green)
i = 0
j +=1
for c in range(256):
    col = gColorRGB(w, float(255-c)/256, 1.0, float(255-c)/256)
    gdFillRect(w, i, j, i+20, j+20, col)
    i+=20
    if i > 580:
        i = 0
        j +=20

j+=21
gdDrawLine(w, 0, j, 600, j)

# change pen sizes to get thicker lines
j +=5
p=gColorPen(w, 'red')
gdDrawLine(w, 0, j, 600, j, p)
j +=5
p2=gColorPen(w, p, xsize=2)
gdDrawLine(w, 0, j, 600, j, p2)
j +=5
p3=gColorPen(w, p, '', 'copy', 3, 2)
gdDrawLine(w, 0, j, 600, j, p3)
j +=5
gdDrawLine(w, 0, j, 600, j)

# Draw lines and text with default color, color for view and specified color
gSetColor(w, 'purple')
gdDrawLine(w, 0, j+5, 600, j+5)
gdDrawText(w, 'purple', None, 10, j+20)
gdDrawText(w, 'red', None, 100, j+20, p2)
gdDrawText(w, 'black', None, 190, j+20, 'black')

# check out fonts
f=gFont('Times', 14, 'italic')
gdDrawText(w, 'purple', f, 10, j+50)
f2=gFont('Times', 14, 'bold')
gdDrawText(w, 'red', f2, 100, j+50, p2)
f3=gFont('Times', 14, 'bold italic')
gdDrawText(w, 'black', f3, 190, j+50, 'black')
        

gStartEventLoop()

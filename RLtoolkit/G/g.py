#<html><body><pre>
# Source Code for g, a lowlevel, deviceindependent, graphics language
# for Python. See http://rlai.cs.ualberta.ca/RLAI/RLtoolkit/g.html for
# <a href="http://rlai.cs.ualberta.ca/RLAI/RLtoolkit/g.html">documentation</a>.

# This package is based on Tkinter (python's version of tk)

import tkinter
import tkinter.colorchooser
import tkinter.filedialog
import sys

# The color chooser currently starts up its own python application and will not appear until
#    you click on the bouncing python icon in your dock.

# Last update: Dec 7, 2004

#### OBJECTS

class CSinfo:
    """Coordinate system info for windows, views and devices"""
    
    def __init__(self, width=1, height=1):
        "Initialize coordinate system values"
        self.csLeft = 0.                        # Normalized coordinate values
        self.csBottom = 0. 
        self.csRight =  1.  
        self.csTop =  1.  
        self.offsetx = self.offsety = 0
        self.scalex = self.scaley = 1.0
        self.x = self.y = 0                     # Device coordinate values
        self.wwidth = width
        self.wheight = height

class Gview(CSinfo, tkinter.Canvas):                                      #<a name="Gview"></a>[<a href="g.html#Gview">Doc</a>]
    "Main graphical view class"
    parent = None
    childviews = []
    
    def __init__ (self, parent, vwidth=10, vheight=10, **kwargs):  #<a name="Gview...)"</a>[<a href="g.html#Gview...)">Doc</a>]
        "Initialization for Gview"
        global GDEVICE
        tkinter.Canvas.__init__(self, parent, borderwidth=0, highlightthickness=0, \
                                width=vwidth, height=vheight)
        CSinfo.__init__(self, vwidth, vheight)
        self.color = None
        self.backcolor = None
        self.gSetParent(parent) 
        self.place(in_=self.parent, anchor=tkinter.NW)  
        gUpdateNormalization(self)
        # Now set up to handle events
        self.bind("<Button-1>", self.viewClickEventHandler)
        self.bind("<ButtonRelease-1>", self.windowMouseUpEventHandler)
        self.bind("<Key>", self.viewKeyEventHandler)
        self.bind("<Control-Key>", self.viewControlKeyEventHandler)
        self.bind("<Motion>", self.viewMotionEventHandler)
    
    def gGetChildren(self):                  #<a name="gGetChildren"</a>[<a href="g.html#gGetChildren">Doc</a>]
        """get the child views of this view"""
        return self.childviews 
        
    def gGetParent(self):
        """get the parent of this view"""
        return self.parent
        
    def gSetParent (self, newparent):
        """Set the parent for this view. Things are slightly different if the parent is
           a Gwindow"""
        parent = self.gGetParent()
        if parent != None and parent != newparent and not isinstance(newparent, tkinter.Toplevel):
            self.parent.childviews.remove(self)
        self.parent = newparent
        if newparent != GDEVICE and not isinstance(self, Gwindow) and not isinstance(newparent, tkinter.Toplevel):
            newparent.childviews = newparent.childviews + [self]
    
    def setViewContainer(self):
        """check that parent is big enough to hold all its childviews; if not, resize it"""
        curxmax = self.wwidth
        curymax = self.wheight
        for c in self.gGetChildren():
            x, y, xmax, ymax = gdGetViewport(c)
            if xmax > curxmax:
                curxmax = xmax
            if ymax > curymax:
                curymax = ymax
        if curymax > self.wheight or curxmax > self.wwidth:
            self.setViewSize(curxmax, curymax)
        
    def setViewSize (self, h, v=None, changegeom=True):
        """update size and normalization attributes for view. changegeom flag is used for the
           Gwindow method only but is included here so that the methods have the same calling
           sequence"""
        if isinstance(h, (list, tuple)):
            v = h[1]
            h = h[0]
        self.wwidth = h
        self.wheight = v
        self.config(width=h, height=v)
        self.gAcceptNewViewportSize()
        gUpdateNormalization(self)

    def setViewPosition (self, xpos, ypos=None):
        """Update attributes for new position"""
        if isinstance(xpos, (list, tuple)):
            ypos = xpos[1]
            xpos = xpos[0]
        if xpos != None and ypos != None:
            self.place(x=xpos, y=ypos)
        self.x = xpos
        self.y = ypos
        self.gAcceptNewViewportPosition()

    def gAcceptNewViewportSize (self):       #<a name="gAcceptNewViewportSize"</a>[<a href="g.html#gAcceptNewViewportSize">Doc</a>]
        """Notice and handle the new viewport size. If there are subviews, check to make
           sure they all fit"""
        if not isinstance(self, Gwindow) and self.parent != GDEVICE:
            self.parent.setViewContainer()
        
    def gAcceptNewViewportPosition (self):
        """Notice and handle new viewport position"""
        pass 
        
    ### EVENTS
    """
    def viewDrawContents(self):
        "Draw the contents of this view"
        self.gDrawView()
    """

    def gDrawView(self):                        #<a name="gDrawView"</a>[<a href="g.html#gDrawView">Doc</a>]
        """This is the default for drawing a view. If there are subviews, draw them all"""
        for child in self.gGetChildren():
            child.gDrawView()

    # To respond to a Mouse click on a view you specialize a method
    #   gdClickEventHandler(self, dx, dy)
    # or gClickEventHandler(self, x, y)
    # which will be called each time there is a Mouse click in that view.

    def viewClickEventHandler(self, event):
        "Determines the coordinates of the click event and calls the appropriate routines"
        self.focus_set()
        dx = self.canvasx(event.x) 
        dy = self.canvasy(event.y) 
        self.gdClickEventHandler(dx, dy)
        self.gClickEventHandler(gCoordx(self, dx), gCoordy(self, dy))

    def gdClickEventHandler (self, dx, dy):   #<a name="gdClickEventHandler"</a>[<a href="g.html#gdClickEventHandler">Doc</a>]
        "Specialize this method (or gClickEventHandler) to handle mouse clicks for your application"
        pass
        
    def gClickEventHandler (self, x, y):          #<a name="gClickEventHandler"</a>[<a href="g.html#gClickEventHandler">Doc</a>]
        "Specialize this method (or gdClickEventHandler) to handle mouse clicks for your application"
        pass
    
    # To respond to mouse movement on a view you specialize a method
    #   gdMotionEventHandler(self, dx, dy)
    # or gMotionEventHandler(self, x, y)
    # which will be called at intervals along the mouse path
    
    def viewMotionEventHandler(self, event):
        "Determines the coordinates of the motion and calls the appropriate routines"
        self.focus_set()
        dx = self.canvasx(event.x) 
        dy = self.canvasy(event.y) 
        self.gdMotionEventHandler(dx, dy)
        self.gMotionEventHandler(gCoordx(self, dx), gCoordy(self, dy))

    def gdMotionEventHandler (self, dx, dy):   #<a name="gdClickEventHandler"</a>[<a href="g.html#gdClickEventHandler">Doc</a>]
        "Specialize this routine (or gMotionEventHandler) to handle mouse motion for your application"
        pass
        
    def gMotionEventHandler (self, x, y):          #<a name="gClickEventHandler"</a>[<a href="g.html#gClickEventHandler">Doc</a>]
        "Specialize this routine (or gdMotionEventHandler) to handle mouse motion for your application"
        pass


    # To respond to a mouse button being released on a view you specialize a method
    #   gdMouseUpEventHandler(self, dx, dy)
    # or gMouseUpEventHandler(self, x, y)
    # which will be called when the mouse button is released.
    
    def windowMouseUpEventHandler(self, event):
        "Determines the coordinates of the mouse up event and calls the appropriate routines"
        self.focus_set()
        dx = self.canvasx(event.x) 
        dy = self.canvasy(event.y) 
        self.gdMouseUpEventHandler(dx, dy)
        self.gMouseUpEventHandler(gCoordx(self, dx), gCoordy(self, dy))

    def gdMouseUpEventHandler (self, dx, dy):
        "Specialize this routine (or gMouseUpEventHandler) to handle mouse button releases for your application"
        pass
        
    def gMouseUpEventHandler (self, x, y):
        "Specialize this routine (or gdMouseUpEventHandler) to handle mouse button releases for your application"
        pass

    # To respond to a mouse button being released on a view you specialize a method
    #    gKeyEventHandler(self, key)
    # which will be called whenever a key is pressed.
    
    def viewKeyEventHandler (self, event):
        "Determines what key was pressed and calls the key event handler"
        self.focus_set()
        self.gKeyEventHandler(event.keysym)
        
    def viewControlKeyEventHandler (self, event):
        "Determines what key was pressed and calls the key event handler"
        self.focus_set()
        self.gKeyEventHandler(event.keysym)
        
    def gKeyEventHandler (self, key):
        "Specialize this routine to handle key presses for your application"
        # Note- not handling alt or ctl key combos
        pass
        
    def gCursor (self, cursorname):                      #<a name="gCursor"</a>[<a href="g.html#gCursor">Doc</a>]
        "Sets the cursor for the view"
        self.config(cursor=cursorname)

    def gCloseView(self):
        "Close the Window and let the parent know this view is no longer in use"
        self.parent.childviews.remove(self)
        self.destroy()
        
gViewport = 'gViewport'
gdViewport = 'gdViewport'
gViewportR = 'gViewportR'
gdViewportR = 'gdViewportR'
windowTitle = 'windowTitle'
resizable = 'resizable'

class Gwindow(Gview):
    """Window for g drawing. Because we can't have an object that is both a tk canvas and
       a tk toplevel at the same time, we let the window be the canvas object so that it can
       be drawn on, and have it point to a parent which is a toplevel object so that we get a window"""
    
    def __init__ (self, **kwargs):  #<a name="Gwindow...)"</a>[<a href="g.html#Gwindow...)">Doc</a>]
        "Initialization for Gwindow"
        global GDEVICE
        new = tkinter.Toplevel(GDEVICE)            # make a Toplevel window, and put a canvas(Gview) under it
        self.screenx = 25                   # default placement for Toplevel window on screen device
        self.screeny = 65
        self.menu = None
        GDEVICE.childwindows.append(self)   # keep track of this guy in main device
        new.lift()                          # try to make this window come out on top of others
        new.tkraise()
        new.config(takefocus=True)
        new.config(width=200, height=200)               # tk default for new windows
        Gview.__init__(self, new, 200, 200, **kwargs)
        self.title = kwargs.get(windowTitle)            # Check for window attributes
        if self.title == None:                          # window title
            self.title = 'Gwindow'
        if self.title != None:                          # make the title show up on the Toplevel
            new.title(self.title)
        resize = kwargs.get(resizable)                  # resizable attribute
        if resize == False:
            new.resizable(0,0)
        gvp = kwargs.get(gViewport)                     # Now check for viewports
        if gvp != None:
            gSetViewport(self, gvp[0], gvp[1], gvp[2], gvp[3])
        gdvp = kwargs.get(gdViewport)
        if gdvp != None:
            gdSetViewport(self, gdvp[0], gdvp[1], gdvp[2], gdvp[3])
        gvpr = kwargs.get(gViewportR)
        if gvpr != None:
            gSetViewportR(self, gvpr[0], gvpr[1], gvpr[2], gvpr[3])
        gdvpr = kwargs.get(gdViewportR)
        if gdvpr != None:
            gdSetViewportR(self, gdvpr[0], gdvpr[1], gdvpr[2], gdvpr[3])
        self.place(in_=self.parent, anchor=tkinter.NW, relheight=1, relwidth=1, relx=0, rely=0)
        gUpdateNormalization(self)      
        self.bind("<Configure>", self.gResize)      # set up to catch certain events
        self.bind("<Destroy>", self.gDestroy)
        
    def setViewSize(self, h, v=None, changegeom=True):
        "Change the size of the window to new values"
        if v ==None: 
            v=h
        Gview.setViewSize(self, h, v, changegeom)
        if changegeom:              # window needs to be resized, not just new values saved
            parent = self.parent
            parent.config(width=h, height=v)
            geom = str(self.wwidth) + 'x' + str(self.wheight) + '+' + str(self.screenx) + '+' + str(self.screeny)
            parent.geometry(geom)
        
    def setViewPosition(self, x, y):
        "Change the position of the window"
        self.screenx = x
        self.screeny = y
        self.x = x
        self.y = y
        self.gAcceptNewViewportPosition()

    def gGetParent(self):
        global GDEVICE
        return GDEVICE
        
    def gAcceptNewViewportSize (self):       #<a name="gAcceptNewViewportSize"</a>[<a href="g.html#gAcceptNewViewportSize">Doc</a>]
        "Handle window changing size"
        pass
        
    def gAcceptNewViewportPosition (self):       #<a name="gAcceptNewViewportPosition"</a>[<a href="g.html#gAcceptNewViewportPosition">Doc</a>]
        "Handle window moving"
        pass

    def gCloseView(self):       #<a name="gCloseView"</a>[<a href="g.html#gCloseView">Doc</a>]
        "Close the window"
        self.gDestroy(None)

    def gDestroy(self, event):
        """Called when window closed by any means, as well as by gCloseView. Removes the
           window from the screen and from the list of current windows"""
        global GDEVICE
        if self in GDEVICE.childwindows:        # remove this window from the window list
            GDEVICE.childwindows.remove(self)
        self.parent.destroy()                   # destroy the toplevel object
        # if this is the only window, should we Quit? Let applications decide this.
        
    def gResize(self, event):
        "This routine automatically resizes windows as long as you have an appropriate gDrawView routine"
        width = event.width
        height = event.height
        if width != self.wwidth or height != self.wheight:
            self.setViewSize(width, height, False)
            self.gDrawView()                                # redraw window contents
        

class Gdevice (CSinfo, tkinter.Tk):                         #<a name="Gdevice"</a>[<a href="g.html#Gdevice">Doc</a>]
    """Object for a device, such as a screen or printer"""
    
    def __init__(self):
        "Initialization for Gdevice"
        tkinter.Tk.__init__(self)
        CSinfo.__init__(self, self.winfo_screenwidth(), self.winfo_screenheight())
        self.lower()                    # don't want it visible
        self.withdraw()
        self.childwindows = []
        gUpdateNormalization(self)

### Viewports
        
def viewSize (view):
    "returns the size of the view, a tuple of width and height"
    return view.wwidth, view.wheight
    
def viewPosition (view):
    "returns the position of the view, a tuple of x and y values"
    return view.x, view.y

def gdGetViewport (view):                              #<a name="gdGetViewport"</a>[<a href="g.html#gdGetViewport">Doc</a>]
    "returns the current device viewport values for view as a tuple (x1, y1, x2, y2)"
    x1, y1 = viewPosition(view)
    w, h = viewSize(view)
    return x1, y1, x1+w-1, y1+h-1

def gGetViewport (view):                                  #<a name="gGetViewport"</a>[<a href="g.html#gGetViewport">Doc</a>]
    "returns the normalized values for the viewport for the view as a tuple (x1, y1, x2, y2)"
    parent = view.gGetParent()
    dx1, dy1, dx2, dy2 = gdGetViewport(view)
    x1, y1 = gCoords(parent, dx1, dy1)
    x2, y2 = gCoords(parent, dx2, dy2)
    return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
          
def gdGetViewportR (view):                            #<a name="gdGetViewportR"</a>[<a href="g.html#gdGetViewportR">Doc</a>]
    "Returns the device viewport values for the view as a tuple (x, y, width, height)"
    x1, y1 = viewPosition(view)
    w, h = viewSize(view)
    return x1, y1, w, h

def gGetViewportR (view):                          #<a name="gGetViewportR"</a>[<a href="g.html#gGetViewportR">Doc</a>]
    "Returns the normalized viewport values for the view as a tuple (x, y, width, ehgith)"
    parent = view.gGetParent()
    dx1, dy1, w, h = gdGetViewportR(view)
    x1, y1 = gCoords(parent, dx1, dy1)
    w2, h2 = gOffset(parent, w, h)
    return x1, y1, abs(w2), abs(h2)

          
def gdSetViewport (view, dx1, dy1, dx2, dy2):      #<a name="gdSetViewport"</a>[<a href="g.html#gdSetViewport">Doc</a>]
    "Sets the device viewport values for a view to the given values"
    posx = min(dx1, dx2)
    posy = min(dy1, dy2)
    width = 1 + abs(dx1-dx2)
    height = 1 + abs(dy1-dy2)
    view.setViewPosition(posx, posy)
    if view.gGetChildren() != []:           # check to see if it can handle its children
        view.setViewContainer()
        width = max(width, view.wwidth)
        height = max(height, view.wheight)
    view.setViewSize(width, height) 

def gSetViewport (view, vpx1, vpy1, vpx2, vpy2):              #<a name="gSetViewport"</a>[<a href="g.html#gSetViewport">Doc</a>]
    "Sets the normal viewport values for a view to the given values"
    if isinstance(view, Gwindow):
        parent = GDEVICE
    else:
        parent = view.gGetParent()
    gdSetViewport(view, \
        gdCoordx(parent, vpx1), \
        gdCoordy(parent, vpy1), \
        vpx2 and gdCoordx(parent, vpx2), \
        vpy2 and gdCoordy(parent, vpy2))
    
                                                              #<a name="gdSetViewportR"</a>[<a href="g.html#gdSetViewportR">Doc</a>]
def gdSetViewportR (view, dx, dy, deltax=None, deltay=None):
    "Sets the device viewport values for a view to the given values"
    if dx == None:
        dx = gdGetViewport(view)[0]
    if dy == None:
        dy = gdGetViewport(view)[1]
    if deltax == None:
        deltax = gdGetViewportR(view)[2]
    if deltay == None:
        deltay = gdGetViewportR(view)[3]
    gdSetViewport(view, dx, dy, dx + deltax-1,  dy + deltay-1)

def gSetViewportR (view, x, y, deltax=None, deltay=None):  #<a name="gSetViewportR"</a>[<a href="g.html#gSetViewportR">Doc</a>]
    "Sets the normal viewport values for a view to the given values"
    oldv = gGetViewport(view)
    if x == None:
        x = oldv[0]
    if y == None:
        y = oldv[1]
    if deltax == None:
        deltax = oldv[2]
    if deltay == None:
        deltay = oldv[3]
    if isinstance(view, Gwindow):
        parent = GDEVICE
    else:
        parent = view.gGetParent()
    gdSetViewportR(view, \
        gdCoordx(parent, x), \
        gdCoordy(parent, y), \
        gdOffsetx(parent, deltax), \
        gdOffsety(parent, deltay) )
    #gSetViewport(view, x, y, x + deltax,  y + deltay)


### Coordinate Systems
    
def gGetCoordinateSystem (view):                        #<a name="gGetCoordinateSystem"</a>[<a href="g.html#gGetCoordinateSystem">Doc</a>]
    """Returns the normal values associated with this view as a tuple
         (x1, y1, x2, y2, corner)
         where x1 and x2 are the left and right values
         and y1 and y2 are the top and bottom values
         and corner specifies which corner values are relative to"""
    if view.csLeft <= view.csRight:
        if view.csBottom <= view.csTop:
            corner = 'lowerLeft'
        else:
            corner = 'upperLeft'
    elif view.csBottom <= view.csTop:
        corner = 'lowerRight'
    else:
        corner = 'upperRight'
    return min(view.csLeft, view.csRight), min(view.csTop, view.csBottom), \
              max(view.csRight, view.csLeft), max(view.csTop, view.csBottom), \
              corner 

gGetCS = gGetCoordinateSystem

def gdGetCoordinateSystem (view):                     #<a name="gdGetCoordinateSystem"</a>[<a href="g.html#gdGetCoordinateSystem">Doc</a>]    # 
    """Returns the device values associated with this view as a tuple
         (left, top, right, bottom, 'upperleft')  - the corner is always upperleft for device coords"""
    x1, y1 = 0, 0 #viewPosition(view)
    w, h = viewSize(view)
    if w==1 or h==1:
        return x1, y1, x1+w, y1+h, 'upperLeft'
    else:
        return x1, y1, x1+w-1, y1+h-1, 'upperLeft'

gdGetCS = gdGetCoordinateSystem

                                                              #<a name="gGetCoordinateSystemR"</a>[<a href="g.html#gGetCoordinateSystemR">Doc</a>]
def gGetCoordinateSystemR (view):
    """Returns the relative normal values associated with this view as a tuple
         (x, y, width, height, corner)
         where x and y are the coordinates of the corner
         and width and height are the relative width and height of the view
         and corner specifies which corner values are relative to"""
    x1, y1, x2, y2, corner = gGetCoordinateSystem(view)
    return x1, y1,  x2 - x1,   y2 - y1, corner

gGetCSR = gGetCoordinateSystemR

                                                              #<a name="gdGetCoordinateSystemR"</a>[<a href="g.html#gdGetCoordinateSystemR">Doc</a>]
def gdGetCoordinateSystemR (view):
    """Returns the relative device values associated with this view as a tuple
         (left, top, width, height, 'upperleft')  - the corner is always upperleft for device coords"""
    x1, y1, x2, y2, corner = gdGetCoordinateSystem(view)
    return x1, y1,  x2 - x1+1,  y2 - y1+1, corner

gdGetCSR = gdGetCoordinateSystemR

                                                              #<a name="gGetCoordinateSystemScale"</a>[<a href="g.html#gGetCoordinateSystemScale">Doc</a>]
def gGetCoordinateSystemScale (view):
    "Returns the first coordinates (corner), the scaling values, and the corner location"
    x1, y1, x2, y2, corner = gGetCoordinateSystem(view)  # return offset??
    return x1, y1, view.scalex, view.scaley, corner

                                                              #<a name="gGetCSScale"</a>[<a href="g.html#gGetCSScale">Doc</a>]
gGetCSScale = gGetCoordinateSystemScale
                                                              #<a name="gSetCoordinateSystem"</a>[<a href="g.html#gSetCoordinateSystem">Doc</a>]
def gSetCoordinateSystem (view, x1, y1, x2, y2, corner='lowerLeft'):
    """Sets the coordinate system for a view to the one specified"""
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    if x1 == x2:
        print("Attempt to Set left and right of g Coordinate System to same values.")
        x2 = x1 + 1
    elif y1 == y2:
        print("Attempt to Set top and bottom of g Coordinate System to same values.")
        y2 = y1 + 1
    else:
        if corner in ['lowerLeft', 'upperLeft']:
            view.csLeft = x1
            view.csRight = x2
        else:
            view.csLeft = x2
            view.csRight = x1
        if corner in ['lowerLeft', 'lowerRight']:
            view.csBottom = y1
            view.csTop = y2
        else:
            view.csBottom = y2
            view.csTop = y1
    gUpdateNormalization(view)

gSetCS = gSetCoordinateSystem

                                                              #<a name="gSetCoordinateSystemR"</a>[<a href="g.html#gSetCoordinateSystemR">Doc</a>]
def gSetCoordinateSystemR (view, x, y, deltax, deltay, corner='lowerLeft'):
    """Sets the coordinate system for a view using relative values"""
    gSetCoordinateSystem(view, x, y, x + deltax, y + deltay, corner)

gSetCSR = gSetCoordinateSystemR

Scales = {'inches':72, 'centimeters':28.35, 'pixels':1, 'points':1}
                                                              #<a name="gSetCoordinateSystemScale"</a>[<a href="g.html#gSetCoordinateSystemScale">Doc</a>]
def gSetCoordinateSystemScale (view, x, y, xScale, yScale=None, corner='lowerLeft'):
    """Sets the coordinate system scale for a view to the given values"""
    if yScale == None:
        yScale = xScale
    if not isinstance(xScale,(int,float)):
        xScale = _Scales.get(xScale, 1)
    if not isinstance(yScale,(int,float)):
        yScale =_Scales.get(yScale, xScale)
    dx1, dy1, dx2, dy2 = gdGetViewport(view)
    x2 = x + (abs( dx1 - dx2) / float(xScale))
    y2 = y +  (abs( dy1 - dy2) / float(yScale))
    gSetCoordinateSystem(view, x, y, x2, y2, corner)

                                                              #<a name="gSetCSScale"</a>[<a href="g.html#gSetCSScale">Doc</a>]
gSetCSScale = gSetCoordinateSystemScale

def gUpdateNormalization (view):
    "Updates state variables of Normalized Coordinate System"
    x1, y1, x2, y2, corner = gdGetCoordinateSystem(view)
    if view.csRight == view.csLeft:
        print("Error - Attempt to establish invalid (zero area) g Coordinate System")
    else:
        view.scalex = float(x2 - x1) /  float( view.csRight - view.csLeft)  
        view.offsetx = x1 - (view.csLeft * view.scalex)
    if  view.csBottom == view.csTop:
        print("Error - Attempt to establish invalid (zero area) g Coordinate System")
    else:
        view.scaley =  float( y2 - y1) / float(view.csBottom - view.csTop)   
        view.offsety = y1 - (view.csTop * view.scaley)

        

### Converting from normal to device coordinates
        
def gdCoordx (view, x):                               #<a name="gdCoordx"</a>[<a href="g.html#gdCoordx">Doc</a>]
    return int(round(view.offsetx + (x * view.scalex)))

def gdCoordy (view, y):                                #<a name="gdCoordy"</a>[<a href="g.html#gdCoordy">Doc</a>]
    return int(round(view.offsety + (y * view.scaley)))

def gdCoords (view, x, y):
    return gdCoordx(view, x), gdCoordy(view, y)
                                                              #<a name="gdOffsetx"</a>[<a href="g.html#gdOffsetx">Doc</a>]
def gdOffsetx (view, xoffset):
    "Returns the length in device coords (pixels) of the xdistance in Normal coords"
    return int(round(xoffset * view.scalex))
                                                              #<a name="gdOffsety"</a>[<a href="g.html#gdOffsety">Doc</a>]
def gdOffsety (view, yoffset):
    "Returns the length in device coords (pixels) of the ydistance in Normal coords"
    return int(round(yoffset * view.scaley))

def gdOffset (view, xoffset, yoffset):
    return gdOffsetx(view, xoffset), gdOffsety(view, yoffset)

### Converting from device to Normal Coordinates

def gCoordx (view, dx):                                #<a name="gCoordx"</a>[<a href="g.html#gCoordx">Doc</a>]
    return float(dx - view.offsetx) / view.scalex

def gCoordy (view, dy):                                #<a name="gCoordy"</a>[<a href="g.html#gCoordy">Doc</a>]
    return  float( dy - view.offsety) / view.scaley

def gCoords (view, dx, dy):
    return gCoordx(view, dx), gCoordy(view, dy)

def gOffsetx (view, dxoffset):                          #<a name="gOffsetx"</a>[<a href="g.html#gOffsetx">Doc</a>]
    return float(dxoffset) / view.scalex

def gOffsety (view, dyoffset):                          #<a name="gOffsety"</a>[<a href="g.html#gOffsety">Doc</a>]
    return float(dyoffset) / view.scaley

def gOffset (view, dxoffset, dyoffset):
    return gOffsetx(view, dxoffset), gOffsety(view, dyoffset)

### Converting Coordinates between Views:

                                                              #<a name="gdConvertx"</a>[<a href="g.html#gdConvertx">Doc</a>]
def gdConvertx (fromView, toView, dx):
    # convert to parent window view, then to other view - views must be in same window
    return dx

                                                              #<a name="gdConverty"</a>[<a href="g.html#gdConverty">Doc</a>]
def gdConverty (fromView, toView, dy):
    return dy 


                                                              #<a name="gConvertx"</a>[<a href="g.html#gConvertx">Doc</a>]
def gConvertx (fromView, toView, x):
    n = gCoordx(toView, gdConvertx(fromView, toView, gdCoordx(fromView, x)))
    return n

                                                              #<a name="gConverty"</a>[<a href="g.html#gConverty">Doc</a>]
def gConverty (fromView, toView, y):
    n = gCoordy(toView, gdConverty(fromView, toView, gdCoordy(fromView , y)))
    return n


## Color Routines

                                                              #<a name="gColorPen"</a>[<a href="g.html#gColorPen">Doc</a>]
def gColorPen (view, color='black', pattern=None, mode=None, xsize=None, ysize=None):
    """Returns a new color With specified pen characteristics
       pattern may be 'gray12', 'gray25', 'gray50', 'gray75', or '' although it doesn't seem
          to be used on the mac
       mode currently is ignored"""
    if ysize == None:
        ysize = xsize
    usecolor, pat, md, (xs, ys) = useColor(color)
    if pattern != None:         # update if necessary
        pat = pattern
    if mode != None:
        md = mode
    if xsize != None:
        xs = xsize
    if ysize != None:
        ys = ysize
    return usecolor, pat, md, (xs, ys)
    
def gFont(fontname="Times", fontsize=12, fontface='normal'):
    """ Returns a font specification to use with the draw text routines
         fontname must be a string, fontsize and integer
        fontface is also a string normal, bold or italic; for bold and italic,
        make fontface "bold italic"
    """
    return fontname, fontsize, fontface
    
def getColor (view, colorcode=None):
    "gets color to use for current drawing"
    if colorcode == None:               # use view default if there is one, or regular default
        if view.color == None:
            return useColor()
        else:   
            return useColor(view.color)
    else:                                           # use new colorcode         
        return useColor(colorcode)
    
def useColor (colorcode='black', pattern="", mode='copy', xsize=1, ysize=None):
    "separates color into color, pattern, mode, and sizes - pattern and mode ignored currently"
    if isinstance(colorcode, (tuple, list)):    # pen list
        color = colorcode[0]
        pattern = colorcode[1]
        mode = colorcode[2]
        xsize, ysize = colorcode[3]
    else:                                       # integer or string color
        color = colorcode
    if ysize == None:
        ysize = xsize
    return color, pattern, mode, (xsize, ysize)

def gColorSize (view, color, xsize, ysize=None):
    "sets the color and size components of the pen for drawing"
    return gColorPen(view, color, None, None, (xsize, ysize))

def gColorPenInvisible (view):
    "returns the invisible pen"
    return gColorInvisible(view)

def gColorInvisible (view):
    "returns the off color to blend in with the default background"
    if view.backcolor != None:
        return view.backcolor
    else:
        return gColorOff(view)
    
def gColorPenFlip (view):
    "returns the inverted color pen for the view on color"
    return gColorFlip(view)

def gColorFlip (view):
    """returns the inverted color for the view on color. Previous versions used a mode of XOR to do this
       This version returns the off color"""
    return gColorOff(view)  

def gColorRGB (view, red, green, blue):                #<a name="gColorRGB"</a>[<a href="g.html#gColorRGB">Doc</a>]
    "Returns a color - red, green and blue span from 0.0 to 1.0"
    red = min(1.0, max(0.0, red))                   # bound the values between 0.0 and 1.0
    green = min(1.0, max(0.0, green))
    blue = min(1.0, max(0.0, blue))
    red = int(255 * red)                            # Now get the corresponding 256 color number
    green = int(255 * green)
    blue = int(255 * blue)
    return "#%02x%02x%02x" % (red, green, blue)     # format colors into something tk likes

def gColorRGB255 (view, red, green, blue):                #<a name="gColorRGB255"</a>[<a href="g.html#gColorRGB255">Doc</a>]
    "Returns a color - red, green and blue go from 0 to 255"
    red = int(min(255, max(0, red)))                # bound the values between 0 and 255, make sure integer
    green = int(min(255, max(0, green)))
    blue = int(min(255, max(0, blue)))
    return "#%02x%02x%02x" % (red, green, blue)     # format colors into something tk likes
                                                              #<a name="Selecting Colors by Name"</a>[<a href="g.html#Selecting Colors by Name">Doc</a>]
def gColorBlack (view): return 'black'
def gColorWhite (view): return 'white'
def gColorPink (view): return 'pink' 
def gColorRed (view): return 'red'
def gColorOrange (view): return 'orange'
def gColorYellow (view): return 'yellow'
def gColorGreen (view): return 'green'
def gColorDarkGreen (view): return 'dark green'
def gColorLightBlue (view): return 'light blue'
def gColorBlue (view): return 'blue'
def gColorPurple (view): return 'purple'
def gColorBrown (view): return 'brown'
def gColorTan (view): return 'tan'
def gColorLightGray (view): return 'light gray'
def gColorGray (view): return 'gray'
def gColorDarkGray (view): return 'dark gray'
def gColorCyan (view): return 'cyan'   
def gColorMagenta (view): return 'magenta'

def gColorOn (view):
    if view not in [None, True, False] and view.color != None:
        return view.color
    else:
        return 'black'
    
def gColorOff (view):
    if view not in [None, True, False] and view.color != None:
        return view.color
    else:
        if sys.platform in ['mac', 'darwin']:
            return 'white'
        else:
            return gColorRGB255(True, 204, 204, 204)    # light grey

gBlack = gColorBlack(None)
gWhite = gColorWhite(None)
gPink = gColorPink(None)   
gRed = gColorRed(None)
gOrange = gColorOrange(None)
gYellow = gColorYellow(None)
gGreen = gColorGreen(None)
gDarkGreen = gColorDarkGreen(None)
gLightBlue = gColorLightBlue(None)
gBlue = gColorBlue(None)
gPurple = gColorPurple(None) 
gBrown = gColorBrown(None)
gTan = gColorTan(None)
gLightGray = gColorLightGray(None)
gGray = gColorGray(None)
gDarkGray = gColorDarkGray(None)
gCyan = gColorCyan(None)
gMagenta = gColorMagenta(None)

gOn = gColorOn(None)    # default on color
gOff = gColorOff(None)  # default off color

def gColorBW (view, intensity):                        #<a name="gColorBW"</a>[<a href="g.html#gColorBW">Doc</a>]
    "returns a shade of grey corresponding to intensity"
    intensity = ( 1 - intensity)        #white is most intense for tk, but not for people
    return gColorRGB(view, intensity, intensity, intensity)

def gColorUserPick (view, **args):                   #<a name="gColorUserPick"</a>[<a href="g.html#gColorUserPick">Doc</a>]
    "call up tk's color picker - currently doesn't come out until you click the bouncing python icon in the dock"
    #return tkColorChooser.askcolor(parent=view, **args)[1]
    b = tkinter.colorchooser.Chooser(view)
    return b.show()[1]

def gSetColor (view, color):                              #<a name="gSetColor"</a>[<a href="g.html#gSetColor">Doc</a>]
     "set on color for a view"
     if color != None:
        view.color = color

# File opening and saving using tk open and save dialogs

def gOpenFileUserPick (view, **args):                   #<a name="gOpenFileUserPick"</a>[<a href="g.html#gOpenFileUserPick">Doc</a>]
    "call up tk's file open dialog - args are title=, initialdir=, and initialfile="
    global GDEVICE
    if view == None:
        view = GDEVICE
    return tkinter.filedialog.Open(view).show(**args)

def gSaveFileUserPick (view, **args):                   #<a name="gSaveFileUserPick"</a>[<a href="g.html#gSaveFileUserPick">Doc</a>]
    "call up tk's file save dialog - args are title=, initialdir=, and initialfile="
    global GDEVICE
    if view == None:
        view = GDEVICE
    return tkinter.filedialog.SaveAs(view).show(**args)


### gdGRAPHICS

def canvasPoint(view, x1, y1):
    return x1, y1

def gdDrawPoint (view, dx, dy, colorcode=None):     #<a name="gdDrawPoint"</a>[<a href="g.html#gdDrawPoint">Doc</a>]
    "Draws a point on view, using device coordinates"
    dx, dy = canvasPoint(view, dx, dy)
    color, pattern, mode, (xsize, ysize) = getColor(view, colorcode)
    #return view.create_line(dx, dy, dx+1, dy, fill=color, width=xsize)
    return view.create_oval(dx, dy, dx+xsize, dy+ysize, width=0, outline= color, fill=color)

                                                              #<a name="gdDrawLine"</a>[<a href="g.html#gdDrawLine">Doc</a>]
def gdDrawLine (view, dx1, dy1, dx2, dy2, colorcode=None):
    "Draws a line on view, using device coordinates"
    dx1, dy1 = canvasPoint(view, dx1, dy1)
    dx2, dy2 = canvasPoint(view, dx2, dy2)
    color, pattern, mode, (xsize, ysize) = getColor(view, colorcode)
    return view.create_line(dx1, dy1, dx2, dy2, fill=color, width=xsize)
    

                                                              #<a name="gdDrawLineR"</a>[<a href="g.html#gdDrawLineR">Doc</a>]
def gdDrawLineR (view, dx, dy, deltax, deltay, colorcode=None):
    """Draws a line on view, using device coordinates for the first point and
       the relative distance to determine the second point"""
    return gdDrawLine(view, dx, dy, dx+deltax, dy+deltay, colorcode)

                                                              #<a name="gdOutlineRect"</a>[<a href="g.html#gdOutlineRect">Doc</a>]
def gdOutlineRect (view, dx1, dy1, dx2, dy2, colorcode=None):
    "Draws a rectangle outline on view, using device coordinates"
    return gdOutlineRectR(view, dx1, dy1, dx2-dx1, dy2-dy1, colorcode)

                                                              #<a name="gdOutlineRectR"</a>[<a href="g.html#gdOutlineRectR">Doc</a>]
def gdOutlineRectR (view, dx, dy, deltax, deltay, colorcode=None):
    """Draws a rectangle outline on view, using device coordinates for the first corner and
       the relative distance to determine the second corner"""
    deltax += dx
    deltay += dy
    dx, dy = canvasPoint(view, dx, dy)
    deltax, deltay = canvasPoint(view, deltax, deltay)
    color, pattern, mode, (xsize, ysize) = getColor(view, colorcode)
    return view.create_rectangle(dx, dy, deltax+1, deltay+1,outline=color, width=xsize)
        
                                                              #<a name="gdFillRect"</a>[<a href="g.html#gdFillRect">Doc</a>]
def gdFillRect (view, dx1, dy1, dx2, dy2, colorcode=None):
    "Draws a solid rectangle on view, using device coordinates"
    return gdFillRectR(view, dx1, dy1, dx2-dx1, dy2-dy1, colorcode)

                                                              #<a name="gdFillRectR"</a>[<a href="g.html#gdFillRectR">Doc</a>]
def gdFillRectR (view, dx, dy, deltax, deltay, colorcode=None):
    """Draws a solid rectangle on view, using device coordinates for the first corner and
       the relative distance to determine the second corner"""
    deltax += dx
    deltay += dy
    dx, dy = canvasPoint(view, dx, dy)
    deltax, deltay = canvasPoint(view, deltax, deltay)
    color, pattern, mode, (xsize, ysize) = getColor(view, colorcode)
    return view.create_rectangle(dx, dy, deltax+1, deltay+1, fill=color, outline=color, stipple=pattern)
    

                                                              #<a name="gdDrawCircle"</a>[<a href="g.html#gdDrawCircle">Doc</a>]
def gdDrawCircle (view, dx, dy, dradius, colorcode=None):
    "Draws a circle outline on view, using device coordinates"
    dx, dy = canvasPoint(view, dx, dy)
    color, pattern, mode, (xsize, ysize) = getColor(view, colorcode)
    return view.create_oval(dx - dradius, dy - dradius, dx + dradius, dy + dradius, outline=color, width=xsize)

                                                              #<a name="gdDrawArc"</a>[<a href="g.html#gdDrawArc">Doc</a>]
def gdDrawArc (view, dx, dy, dradius, startangle, angle, colorcode=None):
    "Draws the outline of a wedge on view, using device coordinates. For startangle, 0 is east."
    dx, dy = canvasPoint(view, dx, dy)
    color, pattern, mode, (xsize, ysize) = getColor(view, colorcode)
    return view.create_arc(dx - dradius, dy - dradius, dx + dradius, dy + dradius, start=startangle, extent=angle, \
        outline=color, width=xsize)

def gdDrawWedge (view, dx, dy , dradius, startangle, angle, colorcode=None):
    "Draws a solid wedge on view, using device coordinates. For startangle, 0 is east"
    dx, dy = canvasPoint(view, dx, dy)
    color, pattern, mode, (xsize, ysize) = getColor(view, colorcode)
    return view.create_arc(dx - dradius, dy - dradius, dx + dradius, dy + dradius, start=startangle, extent=angle, \
        fill=color, outline=color)

                                                              #<a name="gdDrawDisk"</a>[<a href="g.html#gdDrawDisk">Doc</a>]
def gdDrawDisk (view, dx, dy, dradius, colorcode=None):
    "Draws a solid circle on view, using device coordinates"
    dx, dy = canvasPoint(view, dx, dy)
    color, pattern, mode, (xsize, ysize) = getColor(view, colorcode)
    return view.create_oval(dx - dradius, dy - dradius, dx + dradius, dy + dradius, \
                            fill=color, outline=color, stipple=pattern)

                                                              #<a name="gdFillPolygon"</a>[<a href="g.html#gdFillPolygon">Doc</a>]
def gdFillPolygon (view, colorcode=None, *pts):
    "Draws a solid polygon on view, using pairs of device coordinates"
    color, pattern, mode, (xsize, ysize) = getColor(view, colorcode)
    arglist = {'fill':color, 'outline':color, 'stipple':pattern}
    return view.create_polygon(*pts, **arglist)

                                                              #<a name="gdDrawText"</a>[<a href="g.html#gdDrawText">Doc</a>]
def gdDrawText (view, string, font, dx, dy, colorcode=None):
    """Draws text on view, using device coordinates. font eg ("Geneva", 12, 'italic bold') """
    dx, dy = canvasPoint(view, dx, dy)
    color, pattern, mode, (xsize, ysize) = getColor(view, colorcode)
    if font == None:
        return view.create_text(dx, dy, text=string, anchor=tkinter.W, fill=color)  # use default font
    else:
        return view.create_text(dx, dy, text=string, anchor=tkinter.W, fill=color, font=font)


                                                              #<a name="gdDrawTextCentered"</a>[<a href="g.html#gdDrawTextCentered">Doc</a>]
def gdDrawTextCentered (view, string, font, dx, dy, colorcode=None):
    """Draws text centered at the point specified on view, using device coordinates"""
    dx, dy = canvasPoint(view, dx, dy)
    color, pattern, mode, (xsize, ysize) = getColor(view, colorcode)
    if font == None:
        return view.create_text(dx, dy, text=string, anchor=tkinter.CENTER, fill=color) # use default font
    else:
        return view.create_text(dx, dy, text=string, anchor=tkinter.CENTER, fill=color, font=font)


# Need a better way to calculate this

def gdTextWidth (Viewignore, string, characterstyle):    #<a name="gdTextWidth"</a>[<a href="g.html#gdTextWidth">Doc</a>]
    return len(string) * characterstyle[1]

                                                              #<a name="GdTextHeight"</a>[<a href="g.html#GdTextHeight">Doc</a>]
def gdTextHeight (Viewignore, Textignore, characterstyle):
        return characterstyle[1]

                                                              #<a name="gdGetCursorPosition"</a>[<a href="g.html#gdGetCursorPosition">Doc</a>]
def gdGetCursorPosition (view):
    "Returns the current Cursor Position in appropriate Coordinates"
    point = view.winfo_pointerxy()
    dx = point[0]
    dy = point[1]
    if dx != -1 and dy != -1:
        if gdWithinCS(view, dx, dy):
            return dx, dy
        else:
            return None
    else:
        return None

### gGRAPHICS

                                                              #<a name="gClear"</a>[<a href="g.html#gClear">Doc</a>]
def gClear (view, color=None):
    "Draws a solid rectangle in color that covers the whole view"
    if color == None:
        if view.backcolor != None:
            color = view.backcolor
        else: 
            color = gColorOff(view)
    minx, miny ,maxx, maxy, corner = gdGetCoordinateSystem(view)
    view.backcolor = color
    return gdFillRect(view, minx, miny, maxx, maxy, color)


def gMakeVisible (view):                                  #<a name="gMakeVisible"</a>[<a href="g.html#gMakeVisible">Doc</a>]
    "Make the window and changes to it show up"
    if isinstance(view, Gwindow):
        view.update_idletasks()
    else:
        gMakeVisible(view.gGetParent())

def gDrawPoint (view, x, y , colorcode=None):               #<a name="gDrawPoint"</a>[<a href="g.html#gDrawPoint">Doc</a>]
    dx = gdCoordx(view, x)
    dy = gdCoordy(view, y)
    return gdDrawPoint(view, dx, dy, colorcode)

def gDrawLine (view, x1, y1, x2, y2, colorcode=None):        #<a name="gDrawline"</a>[<a href="g.html#gDrawline">Doc</a>]
    dx1 = gdCoordx(view, x1)
    dy1 = gdCoordy(view, y1)
    dx2 = gdCoordx(view, x2)
    dy2 = gdCoordy(view, y2)
    return gdDrawLine(view, dx1, dy1, dx2, dy2, colorcode)
                                                              #<a name="gDrawLineR"</a>[<a href="g.html#gDrawLineR">Doc</a>]
def gDrawLineR (view, x, y, deltax, deltay, colorcode=None):
    return gDrawLine(view, x, y,  x + deltax, y + deltay, colorcode)

def gOutlineRect (view, x1, y1, x2, y2, colorcode=None):      #<a name="gOutlineRect"</a>[<a href="g.html#gOutlineRect">Doc</a>]
    dx1 = gdCoordx(view, x1)
    dy1 = gdCoordy(view, y1)
    dx2 = gdCoordx(view, x2)
    dy2 = gdCoordy(view, y2)
    return gdOutlineRect(view, dx1, dy1, dx2, dy2, colorcode)
                                                              #<a name="gOutlineRectR"</a>[<a href="g.html#gOutlineRectR">Doc</a>]
def gOutlineRectR (view, x, y ,deltax, deltay, colorcode=None):
    dx1 = gdCoordx(view, x)
    dy1 = gdCoordy(view, y)
    dx2 = gdCoordx(view, x + deltax)
    dy2 = gdCoordy(view , y + deltay)
    return gdOutlineRect(view, dx1, dy1, dx2, dy2, colorcode)

def gFillRect (view, x1, y1, x2, y2, colorcode=None):       #<a name="gFillRect"</a>[<a href="g.html#gFillRect">Doc</a>]
    dx1 = gdCoordx(view, x1)
    dy1 = gdCoordy(view, y1)
    dx2 = gdCoordx(view, x2)
    dy2 = gdCoordy(view, y2)
    return gdFillRect(view, dx1, dy1, dx2, dy2, colorcode)
                                                              #<a name="gFillRectR"</a>[<a href="g.html#gFillRectR">Doc</a>]
def gFillRectR (view, x, y, deltax, deltay, colorcode=None):
    dx1 = gdCoordx(view, x)
    dy1 = gdCoordy(view, y)
    dx2 = gdCoordx(view, x + deltax)
    dy2 = gdCoordy(view,  y + deltay)
    return gdFillRect(view, dx1, dy1, dx2, dy2, colorcode)

def gDrawCircle (view, x, y, radius, colorcode=None):       #<a name="gDrawCircle"</a>[<a href="g.html#gDrawCircle">Doc</a>]
    dx = gdCoordx(view, x)
    dy = gdCoordy(view, y)
    dradius  = gdOffsetx(view, radius)
    return gdDrawCircle(view, dx, dy, dradius, colorcode)

def gDrawDisk (view, x, y, radius, colorcode=None):       #<a name="gDrawDisk"</a>[<a href="g.html#gDrawDisk">Doc</a>]
    dx = gdCoordx(view, x)
    dy = gdCoordy(view, y)
    dradius = gdOffsetx(view, radius)
    return gdDrawDisk(view, dx, dy, dradius, colorcode)

def gFillPolygon (view, colorcode=None, *pts):       #<a name="gFillPolygon"</a>[<a href="g.html#gFillPolygon">Doc</a>]
    newpts = []
    for i in range(0, len(pts), 2): 
        x = pts[i]
        y = pts[i+1]
        dx = gdCoordx(view, x)
        dy = gdCoordy(view, y)
        newpts.extend([dx,dy])
    return gdFillPolygon(view, colorcode, *newpts)
                                                              #<a name="gDrawArc"</a>[<a href="g.html#gDrawArc">Doc</a>]
def gDrawArc (view, x, y, radius, startangle, angle, colorcode=None):
    dx = gdCoordx(view, x)
    dy = gdCoordy(view, y)
    dradius = gdOffsetx(view, radius)
    return gdDrawArc(view, dx, dy, dradius, startangle, angle, colorcode)

def gDrawWedge (view, x, y, radius, startangle, angle, colorcode=None):
    dx = gdCoordx(view, x)
    dy = gdCoordy(view, y)
    dradius = gdOffsetx(view, radius)
    return gdDrawWedge(view, dx, dy, dradius, startangle, angle, colorcode)

def gDrawText (view, string, font, x, y, colorcode=None):    #<a name="gDrawText"</a>[<a href="g.html#gDrawText">Doc</a>]
    dx = gdCoordx(view, x)
    dy = gdCoordy(view, y)
    return gdDrawText(view, string, font, dx, dy, colorcode)
                                                              #<a name="gDrawTextCentered"</a>[<a href="g.html#gDrawTextCentered">Doc</a>]
def gDrawTextCentered (view, string, font, x, y, colorcode=None):
    dx = gdCoordx(view, x)
    dy = gdCoordy(view, y)
    return gdDrawTextCentered(view, string, font, dx, dy, colorcode)

                                                              #<a name="gTextWidth"</a>[<a href="g.html#gTextWidth">Doc</a>]
def gTextWidth (view, string, characterstyle):
    return abs(gOffsetx(view, gdTextWidth(view, string, characterstyle)))

def gTextHeight (view, text, characterstyle):             #<a name="gTextHeight"</a>[<a href="g.html#gTextHeight">Doc</a>]
    return abs(gOffsety(view, gdTextHeight(view, text, characterstyle)))

                                                              #<a name="gGetCursorPosition"</a>[<a href="g.html#gGetCursorPosition">Doc</a>]
def gGetCursorPosition (view):
    "Returns the current Cursor Position in appropriate Coordinates"
    dx, dy = gdGetCursorPosition(view)
    if dx !=None:
        return gCoords(view, dx, dy)
    else:
        return None

### ADDITIONAL

                                                              #<a name="gdDrawArrow"</a>[<a href="g.html#gdDrawArrow">Doc</a>]
def gdDrawArrow (view, dx1, dy1, dx2, dy2, colorcode=None):
    "Draws an arrow starting at dx1,dy1 and ending at dx2,dy2 of color"
    return gdDrawArrowhead(view, dx1, dy1, dx2, dy2, 1.0, 0.25, colorcode)
                                                              #<a name="gdDrawArrowR"</a>[<a href="g.html#gdDrawArrowR">Doc</a>]
def gdDrawArrowR (view, dx, dy, deltax, deltay, colorcode=None):
    "Draws an arrow starting at dx,dy and ending at dx+deltax,dy+deltay of color"
    return gdDrawArrowhead(view, dx, dy, dx + deltax, dy + deltay, 1.0, 0.25, colorcode)

angleTangent = 0.7
#   angleTangent is the tangent of the angle between the base  main
#  part of the arrow and one of the two parts of the arrowhead.  I don't
#  know what happens if you Make this parameter negative.  The default
#  value is 0.7.
                                                              #<a name="gdDrawArrowhead"</a>[<a href="g.html#gdDrawArrowhead">Doc</a>]
def gdDrawArrowhead (view, dx1, dy1, dx2, dy2, bodySize, headSize, colorcode=None):
    "Draws an arrowhead dx2,dy2 from dx1,dy1 of color and Sizes"
    deltax = ( dx2 - dx1) * headSize
    deltay =  ( dy2 - dy1) * headSize
    l = []
    if bodySize!= 0:                            #Draw arrow body
        l.append(gdDrawLineR(view, dx2, dy2, \
                             int(round(bodySize * ( dx1 - dx2))), \
                             int(round(bodySize * ( dy1 - dy2))), \
                             colorcode))
    l.append(gdDrawLineR(view, dx2, dy2, \
                         int(round((-deltay * angleTangent) - deltax)), \
                         int(round((deltax * angleTangent) - deltay)), \
                         colorcode))
    l.append(gdDrawLineR(view, dx2, dy2, \
                         int(round((deltay * angleTangent) - deltax)), \
                         int(round((-deltax * angleTangent) - deltay)), \
                         colorcode))
    return l
                                                              #<a name="gdDrawArrowheadR"</a>[<a href="g.html#gdDrawArrowheadR">Doc</a>]
def gdDrawArrowheadR (view, dx, dy, deltax, deltay, bodySize, headSize, colorcode=None):
    "Draws an arrowhead starting at dx,dy and ending at dx+deltax,dy+deltay of color and sizes"
    gdDrawArrowhead(view, dx, dy, dx+deltax, dy+deltay, bodySize, headSize, colorcode)

def gDrawArrow (view, x1, y1, x2, y2, colorcode=None):    #<a name="gDrawArrow"</a>[<a href="g.html#gDrawArrow">Doc</a>]
    dx1 = gdCoordx(view, x1)
    dy1 = gdCoordy(view, y1)
    dx2 = gdCoordx(view, x2)
    dy2 = gdCoordy(view, y2)
    return gdDrawArrowhead(view, dx1, dy1, dx2, dy2, 1.0, 0.25, colorcode)

                                                              #<a name="gDrawArrowR"</a>[<a href="g.html#gDrawArrowR">Doc</a>]
def gDrawArrowR (view, x, y, deltax, deltay, colorcode=None):
    return gDrawArrow(view, x, y , x+deltax, y+deltay, colorcode)

                                                              #<a name="gDrawArrowhead"</a>[<a href="g.html#gDrawArrowhead">Doc</a>]
def gDrawArrowhead (view, x1, y1, x2, y2, bodySize, headSize, colorcode=None):
    dx1 = gdCoordx(view, x1)
    dy1 = gdCoordy(view, y1)
    dx2 = gdCoordx(view, x2)
    dy2 = gdCoordy(view, y2)
    return gdDrawArrowhead(view, dx1, dy1, dx2, dy2, bodySize, headSize, colorcode)

                                                              #<a name="gDrawArrowheadR"</a>[<a href="g.html#gDrawArrowheadR">Doc</a>]
def gDrawArrowheadR (view, x, y, deltax, deltay, bodySize, headSize, colorcode=None):
    return gDrawArrowhead(view, x, y, x+deltax, y+deltay, bodySize, headSize, colorcode)

# Checks to see if within viewports
# Do we need these anymore?

def gdWithinViewport (view, dx, dy):
    "Is dx,dy Within Viewport of view, in the Coordinate System of the parent of view?"
    x1, y1, x2, y2 = gdGetViewport( view)
    return (x1 <= dx <= x2) and (y1 <= dy <= y2)
   
def gWithinViewport (view, x, y):
    "Is x,y Within Viewport of view, in the Coordinate System of the parent of view?"
    x1, y1, x2, y2 = gGetViewport( view)
    return (x1 <= dx <= x2) and (y1 <= dy <= y2)
 
def gdWithinCS (view, dx, dy):
    "Is dx,dy Within CS of view?"
    x1, y1, x2, y2, corner = gdGetCS(view)
    return  (x1 <= dx <= x2) and (y1 <= dy <= y2)

def gWithinCS (view, x, y):
    "Is x,y Within CS of view?"
    x1, y1, x2, y2, corner = gGetCS(view)
    return (x1 <= x <= x2) and (y1 <= y <= y2)
    
# G Control stuff

def gStartEventLoop():                 #<a name="gStartEventLoop"</a>[<a href="g.html#gStartEventLoop">Doc</a>]
    "Starts up the main event loop"
    global GDEVICE
    GDEVICE.mainloop()

gMainloop = gMainLoop = gStartEventLoop  # alternate names for gStartEventLoop

def gQuit():             #<a name="gQuit"</a>[<a href="g.html#gQuit">Doc</a>]
    "destroys all gwindows and exits the event loop"
    global GDEVICE
    for w in GDEVICE.childwindows[:]:
        w.gCloseView()
    GDEVICE.update()
    GDEVICE.quit()

    
def gDelete (view, object):      #<a name="gDelete"</a>[<a href="g.html#gDelete">Doc</a>]
    "Deletes object (an item or list of items created by the gDraw or gdDraw routines) from view"
    if isinstance(object, (tuple, list)):
        for i in object:
            gDelete(view, i)
    else:
        view.delete(object)

def gSetTitle(windoworbutton, newtitle):         #<a name="gSetTitle"</a>[<a href="g.html#gSetTitle">Doc</a>]
    "sets the title or label for a window or a button"
    if isinstance(windoworbutton, tkinter.Button):
        windoworbutton.config(text=newtitle)
    else:
        windoworbutton.parent.title(newtitle)

def gSetCursor(view, cursorname='arrow'):        #<a name="gSetCursor"</a>[<a href="g.html#gSetCursor">Doc</a>]
    """Sets the cursor for view (or button) to be the one specified by cursorname.
       Some cursors are 'sizing', 'cross', 'crosshair', 'plus', 'xterm', 'pencil', 'double_arrow',
       'watch', 'sb_up_arrow', 'sb_down_arrow', sb_left_arrow', 'sb_right_arrow', 'watch', 'fleur'  """
    view.config(cursor=cursorname)
    
# Note: no provision for the color of the button itself because the mac won't use it 
def gdAddButton(view, btext, bcommand, xpos, ypos, background=None):
    """Adds a button to view with text btext, command bcommand, 
        at position xpos, ypos, background of view is background
        e.g. gAddButton(w, "run", runcommand, .5, .5, 'blue')"""
    if background == None:
        b = tkinter.Button(view, text=btext, command=bcommand)
    else:
        b = tkinter.Button(view, text=btext, command=bcommand, highlightbackground=background)
    b.place(x=xpos, y=ypos)
    return b
    
def gAddButton(view, btext, bcommand, xpos, ypos, background=None):      #<a name="gAddButton"</a>[<a href="g.html#gAddButton">Doc</a>]
    """Adds a button to view with text btext, command bcommand, 
        at position xpos, ypos, background of view is background
        e.g. gAddButton(w, "run", runcommand, 100, 100, 'blue')"""
    return gdAddButton(view, btext, bcommand, gdCoordx(view,xpos), gdCoordy(view,ypos), background)

def gButtonEnable(button):           #<a name="gButtonEnable"</a>[<a href="g.html#gButtonEnable">Doc</a>]
    "Enables a button and makes it visible and active"
    button.config(state=tkinter.NORMAL)

def gButtonDisable(button):          #<a name="gButtonDisable"</a>[<a href="g.html#gButtonDisable">Doc</a>]
    "Disables a button - greys it out and makes it inactive"
    button.config(state=tkinter.DISABLED)

class gIntVar(tkinter.IntVar):
    "Pass through for tk integer variable. Use set and get methods to set and get values"
    pass
    
class gStringVar(tkinter.StringVar):
    "Pass through for tk string variable. Use set and get methods to set and get values"
    pass
    
def gAddMenu (parent, menuname, menuitems=None):         #<a name="gAddMenu"</a>[<a href="g.html#gAddMenu">Doc</a>]
    """Adds a menu (or submenu). Menuitems should be a list consisting of the following patterns:
        [text, command]         Adds menuitem text which when selected calls command
        'separator'  or   '---'  Adds a separator line
        ['button', label, variable, on, off, command]  Adds a menu checkbutton attached to variable
                          variable, which must be a gIntVar or a gStringVar
        If parent is a window, the menu is added to the menubar for that window. If it is a menu, it
           is added as a submenu"""
    global GMENU
    if not isinstance(parent, (Gwindow, tkinter.Menu)) and not parent == GMENU:
        print("Cannot add menu to anything except a Gwindow or another menu")
    else:
        if isinstance(parent, Gwindow):
            if parent.menu == None:
                mm = tkinter.Menu(parent)
                parent.parent.config(menu=mm)
                parent.menu = mm
            else:
                mm = parent.menu
            parent = mm
        m = tkinter.Menu(parent, tearoff=0)
        for i in menuitems:
            if i == 'separator' or i == '---':
                m.add_separator()
            elif not isinstance(i, (tuple, list)):
                print(i, "is not a legal menu item")
            elif i[0] == 'button':
                # form is ['button', 'label', gVarname, onvalue, offvalue, command]
                bcom, l, v, on, off, c= i
                m.add_checkbutton(label=l, variable=v, onvalue=on, offvalue=off, command=c)
            else:
                # form is ['label', command]
                l, c = i
                m.add_command(label=l, command=c)
        parent.add_cascade(label=menuname, menu=m)
        return m

def gCheckEvents(view, fn):
    """Pauses long enough to see if there are any other events waiting to be handled,
       then calls fn. Tk lets things run without interruption, so this makes it
       pause to check for events. To run something until interrupted, fn should do
       some processing, and then call gCheckEvents with itself as the fn"""
    view.after(1, fn)
        

GDEVICE = Gdevice()                     #<a name="GDEVICE"</a>[<a href="g.html#GDEVICE">Doc</a>]
GMENU = tkinter.Menu(GDEVICE)           #Application wide menu that all windows will inherit
GDEVICE["menu"] = GMENU                 

#</pre></body></html>

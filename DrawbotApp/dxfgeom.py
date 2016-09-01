import math

# Class definitions
class Entity:
    '''A base class for a DXF entities; lines and arcs.
    The class attribute delta contains the maximum distance in x and y
    direction between eindpoints that are considered coincident.'''

    delta = 0.005
    _anoent = "Argument is not an entity!"

    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        '''Creates an Entity from (x1, y1) to (x2, y2)..'''
        # Start- and enpoint
        self.x1 = float(x1)
        self.y1 = float(y1)
        self.x2 = float(x2)
        self.y2 = float(y2)
        # Bounding box
        self.xmin = min(x1, x2)
        self.ymin = min(y1, y2)
        self.xmax = max(x1, x2)
        self.ymax = max(y1, y2)
        # Endpoints swapped indicator
        self.sw = False

    def fits(self, index, other):
        '''Checks if another entity fits onto this one.

        index -- end of the entity to test, either 1 or 2.
        other -- Entity to test.

        Returns 0 if the other entity doesn't fit. Otherwise returns 1 or 2
        indicating the new free end of other.'''
        assert isinstance(other, Entity), Entity._anoent
        if index == 1:
            if (math.fabs(self.x1-other.x1) < Entity.delta and 
                math.fabs(self.y1-other.y1) < Entity.delta):
                # return free end of other
                return 2
            elif (math.fabs(self.x1-other.x2) < Entity.delta and 
                  math.fabs(self.y1-other.y2) < Entity.delta):
                return 1
        elif index == 2:
            if (math.fabs(self.x2-other.x1) < Entity.delta and 
                math.fabs(self.y2-other.y1) < Entity.delta):
                return 2
            elif (math.fabs(self.x2-other.x2) < Entity.delta and 
                  math.fabs(self.y2-other.y2) < Entity.delta):
                return 1
        return 0 # doesn't fit!

    def getbb(self):
        '''Returns a tuple containing the bounding box of an entity in the
        format (xmin, ymin, xmax, ymax).'''
        return (self.xmin, self.ymin, self.xmax, self.ymax)

    def move(self, dx, dy):
        self.x1 += dx
        self.x2 += dx
        self.y1 += dy
        self.y2 += dy

    def swap(self):
        '''Swap (x1, y1) and (x2, y2)'''
        (self.x1, self.x2) = (self.x2, self.x1)
        (self.y1, self.y2) = (self.y2, self.y1)
        self.sw = not self.sw

    def length(self):
        '''Returns the length of the entity.'''
        raise NotImplementedError

    def startpoint(self):
        '''Returns the (x1, y1).'''
        return (self.x1, self.y1)

    def endpoint(self):
        '''Returns the (x2, y2).'''
        return (self.x2, self.y2)

    def __lt__(self, other):
        '''The (xmin, ymin) corner of the bounding box will be used for
        sorting. Sort by ymin first, then xmin.'''
        assert isinstance(other, Entity), Entity._anoent
        if self.ymin == other.ymin:
            if self.xmin < other.xmin:
                return True
        else:
            return self.ymin < other.ymin

    def __gt__(self, other):
        assert isinstance(other, Entity), Entity._anoent
        if self.ymin == other.ymin:
            if self.xmin > other.xmin:
                return True
        else:
            return self.ymin > other.ymin

    def __eq__(self, other):
        assert isinstance(other, Entity), Entity._anoent
        return self.xmin == other.xmin and self.ymin == other.ymin


class Line(Entity):
    '''A class for a line entity, from point (x1, y1) to (x2, y2)'''
    def __init__(self, x1, y1, x2, y2):
        '''Creates a Line from (x1, y1) to (x2, y2).'''
        Entity.__init__(self, x1, y1, x2, y2)

    def __str__(self):
        fs = "#LINE from ({:.3f},{:.3f}) to ({:.3f},{:.3f})"
        fs =  fs.format(self.x1, self.y1, self.x2, self.y2)
        if self.sw:
            fs += " (swapped)"
        return fs

    def length(self):
        '''Returns the length of a Line.'''
        dx = self.x2-self.x1
        dy = self.y2-self.x1
        return math.sqrt(dx*dx+dy*dy)

    def points(self):
        return (self.startpoint,self.endpoint)

class Arc(Entity):
    '''A class for an arc entity, centering in (cx, cy) with radius R from
    angle a1 to a2.

    Class properties: 

        Arc.segmentsize -- Maximum length of the segment when an arc is rendered
                           as a list of connected line segments.
        Arc.as_segments -- Whether an arc should be output as a list of
                           connected line segments. True by default.'''
    segmentsize = 1
    as_segments = True

    def __init__(self, cx, cy, R, a1, a2):
        '''Creates a Arc centering in (cx, cy) with radius R and running from
        a1 degrees ccw to a2 degrees.'''
        if a2 < a1:
            a2 += 360
        assert a2 > a1, 'Arcs are defined CCW, so a2 must be greater than a1'
        self.cx = float(cx)
        self.cy = float(cy)
        self.R = float(R)
        self.a1 = float(a1)
        self.a2 = float(a2)
        self.segments = None
        x1 = cx+R*math.cos(math.radians(a1))
        y1 = cy+R*math.sin(math.radians(a1))
        x2 = cx+R*math.cos(math.radians(a2))
        y2 = cy+R*math.sin(math.radians(a2))
        Entity.__init__(self, x1, y1, x2, y2)
        # Refine bounding box
        A1 = int(a1)/90
        A2 = int(a2)/90
        for ang in range(A1, A2):
            (px, py) = (cx+R*math.cos(math.radians(90*ang)),
                        cy+R*math.sin(math.radians(90*ang)))
            if px > self.xmax:
                self.xmax = px
            elif px < self.xmin:
                self.xmin = px
            if py > self.ymax:
                self.ymax = py
            elif py < self.ymin:
                self.ymin = py

    def _gensegments(self):
        '''Subdivide the arc into a list of line segments of maximally
        Arc.segmentsize units length. Return the list of segments.'''
        fr = float(Arc.segmentsize)/self.R
        if fr > 1:
            step = self.a2-self.a1
        else:
            ang = math.asin(fr)/math.pi*180
            cnt = math.floor((self.a2-self.a1)/ang) + 1
            step = (self.a2-self.a1)/cnt
        sa = self.a1
        ea = self.a2
        if self.sw:
            sa = self.a2
            ea = self.a1
            step = -step
        angs = _frange(sa, ea, step)
        pnts = [(self.cx+self.R*math.cos(math.radians(a)), 
                 self.cy+self.R*math.sin(math.radians(a))) for a in angs]
        llist = []
        for j in range(1, len(pnts)):
            i = j-1
            llist.append(Line(pnts[i][0], pnts[i][1], pnts[j][0], pnts[j][1]))
        return llist

    def __str__(self):
        s = "#ARC from ({:.3f},{:.3f}) to ({:.3f},{:.3f}), radius {:.3f}"
        s =  s.format(self.x1, self.y1, self.x2, self.y2, self.R)
        if self.sw:
            s += " (swapped)"
        return s

    def move(self, dx, dy):
        Entity.move(self, dx, dy)
        self.cx += dx
        self.cy += dy
        if self.segments:
            for s in self.segments:
                s.move(dx, dy)

    def get_segments(self):
        if self.segments == None:
            self.segments = self._gensegments()
        return self.segments

    def length(self):
        '''Returns the length of an arc.'''
        angle = math.radians(self.a2-self.a1)
        return self.R*angle

class Contour(Entity):
    '''A class for a list of connected Entities'''

    def __init__(self, ent):
        '''Creates a contour from an initial entity.'''
        assert isinstance(ent, Entity), Entity._anoent
        Entity.__init__(self, ent.x1, ent.y1, ent.x2, ent.y2)
        self.ent = [ent]
        self.nument = 1

    def append(self, ent):
        '''Appends and entity to the contour, if one of the ends of entity
        matches the end of the last entity. Returns True if matched, otherwise
        False.'''
        assert isinstance(ent, Entity), Entity._anoent
        last = self.ent[-1]
        newfree = last.fits(2, ent)
        if newfree == 0:
            return False
        self.ent.append(ent)
        self.nument += 1
        (self.xmin, self.ymin, 
         self.xmax, self.ymax) = merge_bb(self.getbb(), ent.getbb())
        if newfree == 1:
            ent.swap()
        self.x2 = ent.x2
        self.y2 = ent.y2
        return True

    def prepend(self, ent):
        '''Prepends and entity to the contour, if one of the ends of entity
        matches the end of the first entity. Returns True if matched,
        otherwise False.'''
        assert isinstance(ent, Entity), Entity._anoent
        first = self.ent[0]
        newfree = first.fits(1, ent)
        if newfree == 0:
            return False
        self.ent.insert(0, ent)
        self.nument += 1
        (self.xmin, self.ymin, 
         self.xmax, self.ymax) = merge_bb(self.getbb(), ent.getbb())
        if newfree == 2:
            ent.swap()
        self.x1 = ent.x1
        self.y1 = ent.y1
        return True

    def __str__(self):
        outstr = "#Contour [boundingbox: {:.3f}, {:.3f}, {:.3f}, {:.3f}]\n"
        outstr = outstr.format(self.xmin, self.ymin, self.xmax, self.ymax)
        for e in self.ent:
            outstr += "#" + str(e) + "\n"
        return outstr[0:-1]

    def dxfdata(self):
        s = ""
        for e in self.ent:
            s += e.dxfdata()
        return s

    def pdfdata(self):
        rl = [self.ent[0].x1, self.ent[0].y1]
        for e in self.ent:
            rl.append(e.x2, e.y2)
        return rl

    def ncdata(self):
        (s1, s2) = self.ent[0].ncdata()
        for e in self.ent[1:]:
            (f1, f2) = e.ncdata()
            s2 += f2
        return (s1, s2)

    def length(self):
        '''Returns the length of a contour.'''
        il = [e.length() for e in self.ent]
        return sum(il)

# Function definitions.

def _frange(start, end, step):
    '''A range function for floats.
    
    start -- beginning of the range.
    end -- end of the range.
    step -- size of the step between numbers.

    Returns a list of floating point numbers. If the difference between start
    and end isn't a multiple of step, end will not be included in the list.'''

    assert start != end, "Start and end cannot have the same value!"
    assert step != 0.0, "Step cannot be 0!"
    if start < end:
        assert step > 0.0, "Step must be positive if start < end!"
    else:
        assert step < 0.0, "Step must negative if start > end!"
    rv = [start]
    a = start
    if step > 0.0:
        while a < end:
            a += step
            rv.append(a)
    else:
        while a > end:
            a += step
            rv.append(a)
    return rv    

def merge_bb(a, b):
    '''The bounding boxes a and b are tuples (xmin, ymin, xmax,
    ymax). Calculate and return a bounding box that contains a and b.'''
    xmin = min(a[0], b[0])
    ymin = min(a[1], b[1])
    xmax = max(a[2], b[2])
    ymax = max(a[3], b[3])
    return (xmin, ymin, xmax, ymax)

def find_contours(lol, loa):
    '''Find polylines in the list of lines and list of arcs. 

    lol -- list of lines
    loa -- list of arcs.

    Returns a list of contours and a list of remaining lines and a list of
    remaining arcs as a tuple.'''
    remlines = []
    remarcs = []
    elements = lol[:]+loa[:]
    loc = []
    while len(elements) > 0:
        first = elements.pop(0)
        cn = Contour(first)
        oldlen = cn.nument
        while True:
            n = 0
            while n < len(elements):
                if cn.append(elements[n]) or cn.prepend(elements[n]):
                    del elements[n]
                else:
                    n += 1
            if cn.nument == oldlen:
                break
            oldlen = cn.nument
        if cn.nument > 1:
            loc.append(cn)
        else:
            if isinstance(first, Line):
                remlines.append(first)
            elif isinstance(first, Arc):
                remarcs.append(first)
    return (loc, remlines, remarcs)

def gen_arc_other(origin,center,destination,direction):
    radius = twoPointDistance(origin,center)
    a1 = angle(origin,center)
    a2 = angle(destination,center)
    cx,cy = center
    return Arc(cx,cy,radius,a1,a2)

def angle(point,center):
    x1,y1 = point
    x2,y2 = center
    dx = x1-x2
    dy = y1-y2
    return math.degrees(math.atan2(dx,dy))

def twoPointDistance(start_point,center_point):
    x1,y1 = start_point
    x2,y2 = center_point
    dx = x1-x2
    dy = y1-y2
    return math.sqrt(dx ** 2 + dy ** 2)

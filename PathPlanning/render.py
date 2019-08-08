"""
render tools
"""
try:
    import pyglet
except ImportError as err:
    raise ImportError('''
    Unable to import pyglet.
    Please install pyglet via 'pip install pyglet'
    ''')

try:
    from pyglet.gl import *
except ImportError as err:
    raise ImportError('''
    Unable to import gl from pyglet.
    Please install OpenGL.
    ''')

import math

class Viewer(object):
    def __init__(self, width=640, height=480, caption="Robotics Notebook/Path Planning", icon_file="icon.png"):
        self.width = width
        self.height = height
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        # screen = display.get_default_screen()
        config = Config(double_buffer=True)
        self.window = pyglet.window.Window(width=width, height=height, display=display,
                                           config=config, caption=caption)
        icon = pyglet.image.load(icon_file)
        self.window.set_icon(icon)
        self.is_open = True
        self.window.on_close = self.close_viewer
        self.window.on_draw = self.draw

    def render(self):
        glClearColor(1,1,1,1)
        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()
        self.window.dispatch_event('on_draw')
        self.window.flip()

    def draw(self):
        self.draw_point(pos=(400, 300), color=(100, 0, 0), pointSize=3)
        self.draw_line(start=(200, 200), end=(400, 400), color=(0, 100, 0), lineWidth=3)
        self.draw_circle(pos=(100,350), radius=50, res=50, color=(100, 100, 0))
        self.draw_circle(pos=(100, 50), radius=30, res=10, filled=False, lineWidth=5)
        self.draw_polygon(points=((200, 50), (200, 250), (400, 250), (400, 50)), close=True, lineWidth=3, color=(0, 0, 100))
        self.draw_polygon(points=((500, 250), (500, 350), (600, 350), (600, 250)), filled=True, color=(0, 0, 100))

    def draw_point(self, pos, **attrs):
        point = Point(pos=pos)
        if 'color' in attrs:
            point.set_color(*attrs['color'])
        if 'pointSize' in attrs:
            point.set_pointSize(attrs['pointSize'])
        point.render()

    def draw_line(self, start, end, **attrs):
        line = Line(start=start, end=end)
        if 'color' in attrs:
            line.set_color(*attrs['color'])
        if 'lineWidth' in attrs:
            line.set_lineWidth(attrs['lineWidth'])
        line.render()

    def draw_circle(self, pos, radius, **attrs):
        circle = Circle(pos=pos, radius=radius)
        if 'color' in attrs:
            circle.set_color(*attrs['color'])
        if 'res' in attrs:
            circle.set_res(attrs['res'])
        if 'filled' in attrs:
            circle.set_filled(attrs['filled'])
        if 'lineWidth' in attrs:
            circle.set_lineWidth(attrs['lineWidth'])
        circle.render()

    def draw_polygon(self, points, **attrs):
        polygon = Polygon(points=points)
        if 'color' in attrs:
            polygon.set_color(*attrs['color'])
        if 'close' in attrs:
            polygon.set_close(attrs['close'])
        if 'filled' in attrs:
            polygon.set_filled(attrs['filled'])
        if 'lineWidth' in attrs:
            polygon.set_lineWidth(attrs['lineWidth'])
        polygon.render()

    def close_viewer(self):
        self.is_open = False


class Attr(object):
    def enable(self):
        raise NotImplementedError
    def disable(self):
        pass

class Color(Attr):
    def __init__(self, *color):
        self.color = color
    def enable(self):
        glColor3b(*self.color)

class LineWidth(Attr):
    def __init__(self, width):
        self.width = width
    def enable(self):
        glLineWidth(self.width)

class PointSize(Attr):
    def __init__(self, size):
        self.size = size
    def enable(self):
        glPointSize(self.size)

class Geom(object):
    def __init__(self):
        self._color = Color(0, 0, 0)
        self.attrs = [self._color]
    def render(self):
        for attr in self.attrs:
            attr.enable()
        self.render1()
        for attr in self.attrs:
            attr.disable()
    def render1(self):
        raise NotImplementedError
    def add_attr(self, attr):
        self.attrs.append(attr)
    def set_color(self, r, g, b):
        self._color.color = (r, g, b)

class Point(Geom):
    def __init__(self, pos=(0,0), size=3):
        Geom.__init__(self)
        self._pos = pos
        self._pointSize = PointSize(size=size)
        self.add_attr(self._pointSize)
    def render1(self):
        glBegin(GL_POINTS)
        glVertex2d(*self._pos)
        glEnd()
    def set_pointSize(self, size):
        self._pointSize.size = size

class Line(Geom):
    def __init__(self, start, end, width=3):
        Geom.__init__(self)
        self._start = start
        self._end = end
        self._lineWidth = LineWidth(width=width)
        self.add_attr(self._lineWidth)
    def render1(self):
        glBegin(GL_LINES)
        glVertex2d(*self._start)
        glVertex2d(*self._end)
        glEnd()
    def set_lineWidth(self, width):
        self._lineWidth.width = width

class Circle(Geom):
    def __init__(self, pos, radius, res=30, filled=True, width=3):
        Geom.__init__(self)
        self._pos = pos
        self._radius = radius
        self._res = res
        self._filled = filled
        self._lineWidth = LineWidth(width=width)
    def render1(self):
        if self._filled:
            glBegin(GL_POLYGON)
        else:
            glBegin(GL_LINE_LOOP)
        for i in range(max(self._res, 5)):
            angle = 2*math.pi/self._res*i
            glVertex2d(self._pos[0] + self._radius * math.cos(angle), self._pos[1] + self._radius * math.sin(angle))
        glEnd()
    def set_pos(self, pos):
        self._pos = pos
    def set_radius(self, radius):
        self._radius = radius
    def set_res(self, res):
        self._res = res
    def set_filled(self, filled):
        self._filled = filled
    def set_lineWidth(self, width):
        self._lineWidth.width = width

class Polygon(Geom):
    def __init__(self, points, close=True, filled=False, width=3):
        Geom.__init__(self)
        self._points = points
        self._close = close
        self._filled = filled
        self._lineWidth = LineWidth(width=width)
        self.add_attr(self._lineWidth)
    def render1(self):
        if self._filled:
            if len(self._points) > 4:
                glBegin(GL_POLYGON)
            elif len(self._points) == 4:
                glBegin(GL_QUADS)
            else:
                glBegin(GL_TRIANGLES)
        else:
            glBegin(GL_LINE_LOOP if self._close else GL_LINE_STRIP)
        for point in self._points:
            glVertex2d(*point)
        glEnd()
    def set_close(self, close):
        self._close = close
    def set_filled(self, filled):
        self._filled = filled
    def set_lineWidth(self, width):
        self._lineWidth.width = width


if __name__ == '__main__':
    viewer = Viewer()
    while viewer.is_open:
        viewer.render()
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
        # self.draw_line()
        # self.draw_circle()
        # self.draw_polygon()

    def draw_point(self, pos, **attrs):
        point = Point(pos=pos)
        if 'color' in attrs:
            point.set_color(*attrs['color'])
        if 'pointSize' in attrs:
            point.set_pointSize(attrs['pointSize'])
        point.render()

    def draw_line(self):
        glLineWidth(3)
        pyglet.graphics.draw(2, GL_LINES, ('v2i', (100, 100, 200, 200)), ('c3B', (0, 0, 0) * 2))

    def draw_circle(self):
        pass

    def draw_polygon(self):
        pass

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


class Line(object):
    def __init__(self):
        pass




if __name__ == '__main__':
    viewer = Viewer()
    while viewer.is_open:
        viewer.render()
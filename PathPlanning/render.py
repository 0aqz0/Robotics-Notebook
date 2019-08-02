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
        self.draw_point()
        self.draw_line()
        self.draw_circle()
        self.draw_polygon()

    def draw_point(self):
        glPointSize(3)
        pyglet.graphics.draw(1, GL_POINTS, ('v2i', (100, 100)), ('c3B', (255, 0, 0)))

    def draw_line(self):
        glLineWidth(1)
        pyglet.graphics.draw(2, GL_LINES, ('v2i', (100, 100, 200, 200)))

    def draw_circle(self):
        pass

    def draw_polygon(self):
        pass

    def close_viewer(self):
        self.is_open = False


if __name__ == '__main__':
    viewer = Viewer()
    while viewer.is_open:
        viewer.render()
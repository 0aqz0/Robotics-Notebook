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
    import pyglet.gl as gl
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
        config = gl.Config(double_buffer=True)
        self.window = pyglet.window.Window(width=width, height=height, display=display,
                                           config=config, caption=caption)
        icon = pyglet.image.load(icon_file)
        self.window.set_icon(icon)

    def close(self):
        self.window.close()

    def render(self):
        self.window.switch_to()
        self.window.dispatch_events()
        self.window.dispatch_event('on_draw')
        self.window.flip()

    def draw_circle(self):
        pass

    def draw_polygon(self):
        pass

    def draw_line(self):
        pass

    def draw_obstacle(self):
        pass


if __name__ == '__main__':
    viewer = Viewer()
    # pyglet.app.run()
    pyglet.clock.tick()
    while True:
        viewer.render()
        # viewer.window.switch_to()
        # viewer.window.dispatch_events()
        # viewer.window.dispatch_event('on_draw')
        # viewer.window.flip()
class window_starter():
    def __init__(self, world, **kwargs):
        self.world = world
        self.window = kwargs.get('turtle_screen')
        self.title = kwargs.get('title')
        self.bgcolor = kwargs.get('bgcolor')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')


    def set_window(self):
        self.window.title(self.title)
        self.window.bgcolor(self.bgcolor)
        self.window.setup(width=self.width, height=self.height)
        self.window.tracer(0)
        self.window.listen()


from random import choice, randint, sample

from fixtures import Parameter, RGB, RGBMatrix

class OneHot:
    def __init__(self, items, name = 'OneHot'):
        for item in items:
            if type(item) not in (Parameter, RGB, RGBMatrix) :
                raise 'OneHot cant handle'

        self.items = items
        self.hot = None

    def next(self):
        if self.hot:
            self.hot.enabled = False

        self.hot = choice(self.items)
        self.hot.enabled = True

class Rainbow:
    def __init__(self, items, name = 'Rainbow', mode = max):
        for item in items:
            if type(item) != RGB :
                raise 'Rainbow cant handle'

        self.mode = mode
        self.name = name
        self.items = items
        self.counter = 0

    def next(self):
        for i, item in enumerate(self.items):
            item.set_hsv(((self.counter + i) % 360) / 360, 1, 1, self.mode, self.name)

        self.counter += 1

class RandomRGB:
    def __init__(self, items, amount, name = 'RandomRGB', mode = max):
        for item in items:
            if type(item) != RGB :
                raise 'Rainbow cant handle'

        self.mode = mode
        self.name = name

        self.items = items
        self.amount = amount
        self.selection = []

    def next(self):
        for item in self.selection:
            item.remove_layer(self.name)

        self.selection = sample(self.items, self.amount)

        for item in self.selection:
            item.set_rgb(randint(0, 255), randint(0, 255), randint(0, 255), self.mode, self.name)


class Patric:
    def __init__(self, items, name = 'Patric', mode = max):
        for item in items:
            if type(item) != RGB :
                raise 'Rainbow cant handle'

        self.mode = mode
        self.name = name
        self.items = items
        self.counter = 0

    def next(self):
        self.switch = True;
        for i, item in enumerate(self.items):
            if self.switch:
                if i%2 == 0:
                    item.set_rgb(255, 0, 255, self.mode, self.name)
                else:
                    item.set_rgb(255, 0, 0, self.mode, self.name)
            else:
                if i%2 == 0:
                    item.set_rgb(255, 0, 0, self.mode, self.name)
                else:
                    item.set_rgb(255, 0, 255, self.mode, self.name)

        if self.counter % 5 == 0:
            self.switch = not self.switch
        self.counter += 1

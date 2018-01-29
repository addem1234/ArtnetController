from random import choice, randint, sample

from curio import spawn, sleep

from fixtures import Parameter, RGB, RGBMatrix

class Speed:
    def __init__(self, bpm):
        self.bpm = bpm

    @property
    def delay(self):
        return 60 / self.bpm

    @property
    def hertz(self):
        return self.bpm / 60


class Effect:
    def __init__(self, items, name, speed):
        self.items = items
        self.name = name

        self.speed = speed

    async def start(self):
        self.running = True
        await self.loop()

    def stop(self):
        self.running = False

    async def loop(self):
        while self.running:
            self.next()
            await sleep(self.speed.delay)


class OneHot(Effect):
    def __init__(self, items, speed, name = 'OneHot'):
        super().__init__(items, name, speed)

        self.hot = None

    def next(self):
        if self.hot:
            self.hot.enabled = False

        self.hot = choice(self.items)
        self.hot.enabled = True

class Rainbow(Effect):
    def __init__(self, items, speed, name = 'Rainbow', mode = max):
        super().__init__(items, name, speed)

        self.mode = mode
        self.counter = 0

    def next(self):
        for i, item in enumerate(self.items):
            item.set_hsv(((self.counter + i) % 360) / 360, 1, 1, self.mode, self.name)

        self.counter += 1

class RandomRGB(Effect):
    def __init__(self, items, speed, amount, name = 'RandomRGB', mode = max):
        super().__init__(items, name, speed)

        self.mode = mode
        self.amount = amount
        self.selection = []

    def next(self):
        for item in self.selection:
            item.remove_layer(self.name)

        self.selection = sample(self.items, self.amount)

        for item in self.selection:
            item.set_rgb(randint(0, 255), randint(0, 255), randint(0, 255), self.mode, self.name)


class Patric(Effect):
    def __init__(self, items, speed, name = 'Patric', mode = max):
        super().__init__(items, name, speed)

        self.mode = mode
        self.counter = 0

    def next(self):
        for i, item in enumerate(self.items):
            if self.counter % 2 == 0:
                if i % 2 == 0:
                    item.set_rgb(255, 0, 255, self.mode, self.name)
                else:
                    item.set_rgb(255, 0, 0, self.mode, self.name)
            else:
                if i % 2 == 0:
                    item.set_rgb(255, 0, 0, self.mode, self.name)
                else:

                    item.set_rgb(255, 0, 255, self.mode, self.name)
        self.counter += 1

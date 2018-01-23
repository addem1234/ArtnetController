from collections import namedtuple
from colorsys import hsv_to_rgb

from artnet import ArtNet

class Parameter:
    def __init__(self, name, default = None):
        self.name = name
        self.default = default
        self.enabled = True
        self.children = []

    def set_layer(self, mode, value, name):
        if self.__class__ != Parameter:
            for child in self.children:
                child.set_layer(mode, value, name)
        else:
            for layer in self.children:
                if layer[2] == name:
                    layer[0] = mode
                    layer[1] = value

                    break
            else:
                self.children.append([mode, value, name])

    def remove_layer(self, name):
        if self.__class__ != Parameter:
            for child in self.children:
                child.remove_layer(name)
        else:
            for i, layer in enumerate(self.children):
                if layer[2] == name:
                    self.children.pop(i)
                    break

    @property
    def value(self):
        if self.__class__ != Parameter:
            return [ c.value for c in self.children ]

        elif not self.enabled:
            return self.default

        else:
            result = self.default
            for mode, value, _ in self.children:
                result = mode(result, value)
            return int(result)

class RGB(Parameter):
    def __init__(self, name):
        super().__init__(name)

        self.children = [
            Parameter('red', 0),
            Parameter('green', 0),
            Parameter('blue', 0),
        ]

    def set_rgb(self, red, green, blue, mode = max, name = None):
        self.children[0].set_layer(mode, red, name)
        self.children[1].set_layer(mode, green, name)
        self.children[2].set_layer(mode, blue, name)

    def set_hsv(self, hue, saturation, value, mode = max, name = None):
        red, green, blue = hsv_to_rgb(hue, saturation, value)
        self.set_rgb(red * 255, green * 255, blue * 255, mode, name)


class RGBRow(Parameter):
    def __init__(self, name, cols):
        super().__init__(name)

        self.children = [ RGB('RGBRow') for _ in range(cols) ]

    @property
    def rgb(self):
        return self.children


class RGBMatrix(Parameter):
    def __init__(self, name, rows, cols):
        super().__init__(name)

        self.children = [ RGBRow('RGBMatrix', cols) for _ in range(rows) ]

    @property
    def rgb(self):
        return [ rgb for child in self.children for rgb in child.rgb ]

class SnakeRGBMatrix(RGBMatrix):
    @property
    def value(self):
        return [ (row.value if not i % 2 else reversed(row.value)) for i, row in enumerate(self.children) ]

class LEDStrip(ArtNet, RGBRow):
    def __init__(self, node):
        super().__init__(node)
        RGBRow.__init__(self, 'LEDStrip', 480)

class LEDCube(ArtNet):
    def __init__(self, node):
        super().__init__(node)

        self.panels = [ SnakeRGBMatrix('LEDCube', 10, 10) for _ in range(6) ]

    @property
    def value(self):
        return [ panel.value for panel in self.panels ]

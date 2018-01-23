from time import sleep
from collections import namedtuple

from fixtures import LEDStrip
from effects import Rainbow, RandomRGB, Patric

Node = namedtuple('Node', 'ip')
l = LEDStrip(Node('192.168.1.101'))
r = Rainbow(l.rgb)
rr = RandomRGB(l.rgb, 10, mode = max)
p = Patric(l.rgb)

for item in l.rgb:
    item.set_rgb(10, 10, 10, name = 'constant')

while True:
    r.next()
    rr.next()
    p.next()
    l.update()

    sleep(1/10)

from collections import namedtuple
from curio import run, spawn, sleep

from fixtures import LEDStrip
from effects import Speed, Rainbow, RandomRGB, Patric


async def main():
    Node = namedtuple('Node', 'ip')
    l = LEDStrip(Node('192.168.1.106'))

    s = Speed(200)

    #r = Rainbow(l.rgb, s)
    #r.start()
    #rr = RandomRGB(l.rgb, s, 10, mode = max)
    #await spawn(rr.start())
    p = Patric(l.rgb, s)
    await spawn(p.start())

    # for item in l.rgb:
    #     item.set_rgb(10, 10, 10, name = 'constant')

    while True:
        lupdate = await spawn(l.update())

        await lupdate.join()
        await sleep(1/10)

if __name__ == '__main__':
    run(main)

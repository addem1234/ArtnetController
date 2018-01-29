import bitstring

#from curio import run
from curio.socket import *

from constants import ARTNET_POLL, ARTNET_DMX, ARTNET_PORT

class ArtNet:
    def __init__(self, node):
        self.node = node
        #run(self.init)

        self.sock = socket(AF_INET, SOCK_DGRAM)

        self.sequence = 0

    async def update(self):
        rest = list(flatten(self.value))
        universes = []
        while len(rest):
            universe, rest = rest[:512], rest[512:]
            universes.append(universe)

        for i, data in enumerate(universes):
            packet = dmx_frame(data, i, self.sequence)
            await send_packet(self.sock, self.node.ip, packet)

        self.sequence = (self.sequence + 1) % 255

def flatten(items):
    for item in items:
        if not isinstance(item, int):
            yield from flatten(item)
        else:
            yield item

def dmx_frame(data, universe, sequence = 0):
    packet_format = ', '.join([
        'bytes:8=header',
        'uintle:16=opcode',
        'uintle:16=protocol_version',
        'uint:8=sequence',
        'uint:8=physical',
        'uintle:16=universe',
        'uintbe:16=length',
        'bytes=framedata'
    ])

    return bitstring.pack(packet_format,
        header='Art-Net\0'.encode('utf-8'),
        opcode=ARTNET_DMX,
        protocol_version=0,
        sequence=sequence,
        physical=0,
        universe=universe,
        length=len(data),
        framedata=data).tobytes()

def poll_request(ttm=True):
    packet_format = ', '.join([
        'bytes:8=header',
        'uintle:16=opcode',
        'uintle:16=protocol_version',
        'uint:8=ttm',
        'uint:8=pad'
    ])
    return bitstring.pack(packet_format,
        header='Art-Net\0'.encode('utf-8'),
        opcode=ARTNET_POLL,
        protocol_version=0,
        ttm=ttm,
        pad=0)

async def search_nodes(sock, interface):
    packet = poll_request()
    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    await send_packet(sock, interface['broadcast'], packet)

    while True:
        with move_on_after(30) as cancel_scope:
            packet, addr = await sock.recvfrom(1024)
            print(addr, packet)
            yield Node(addr, packet)

        if cancel_scope.cancel_called:
            break

async def send_packet(sock, addr, packet):
    await sock.sendto(packet, (addr, ARTNET_PORT))

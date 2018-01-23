import netifaces
from trio import run, socket, open_nursery

from artnet import search_nodes
from constants import ARTNET_PORT

class Controller:
    def __init__(self, interface):
        self.interface = interface

    async def main_loop(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        await self.sock.bind((interface['addr'], ARTNET_PORT))

        #nodes = [ node async for node in search_nodes(self.sock, self.interface) ]
        #print(nodes)

        while True:
            #I DONT KNOW WHAT TO DO UNTIL I HAVE A FRAMEWORK TO FRAME MY WORK AROUND
            pass



if __name__ == '__main__':
    print(netifaces.interfaces())
    interface = netifaces.ifaddresses('wlp58s0')[netifaces.AF_INET][0] # first ipv4 interface, AF_INET6 for ipv6

    controller = Controller(interface)

    run(controller.main_loop)


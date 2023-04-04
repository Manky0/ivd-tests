from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
import os
import sys

def int_to_mac(macint):
    if type(macint) != int:
        raise ValueError('invalid integer')
    return ':'.join(['{}{}'.format(a, b)
                     for a, b
                     in zip(*[iter('{:012x}'.format(macint))]*2)])

class testTopo(Topo):
    def build(self):
        self.switch = []
        self.host = []

        for i in range (0, 7):
            self.switch.append(self.addSwitch('s%d' % (i + 1), stp=True))
        
        for i in range (0, 4):
            host_name = 'h%d' % (i + 1)
            host_ip = '127.0.0.%d' % (i + 1)
            host_mac = int_to_mac(i + 1)
            self.host.append(self.addHost(host_name, ip=host_ip, mac=host_mac))

        # Server (Host 4) -> Router 7
        self.addLink(self.host[3], self.switch[6])

        # Router -> Router
        self.addLink(self.switch[0], self.switch[1])
        self.addLink(self.switch[0], self.switch[2])
        self.addLink(self.switch[0], self.switch[3])
        
        self.addLink(self.switch[1], self.switch[2])
        self.addLink(self.switch[1], self.switch[3])
        self.addLink(self.switch[1], self.switch[6])

        self.addLink(self.switch[2], self.switch[3])
        self.addLink(self.switch[2], self.switch[4])
        self.addLink(self.switch[2], self.switch[5])

        self.addLink(self.switch[3], self.switch[4])
        self.addLink(self.switch[3], self.switch[5])
        self.addLink(self.switch[3], self.switch[6])

        self.addLink(self.switch[4], self.switch[5])

        self.addLink(self.switch[5], self.switch[6])

        # Router -> User
        self.addLink(self.host[0], self.switch[0])
        self.addLink(self.host[1], self.switch[2])
        self.addLink(self.host[2], self.switch[4])


topos = { 'testTopo': ( lambda: testTopo() )} 

def perfTest():
    "Create network and run simple performance test"
    topo = testTopo()
    net = Mininet( topo=topo, link=TCLink)
    net.start()
    print( "Dumping host connections" )
    dumpNodeConnections( net.hosts )
    dumpNodeConnections (net.switches)
    print( "Testing network connectivity" )
    net.pingAll()
    print( "Testing bandwidth between h1 and h4" )
    h1, h4 = net.get( 'h1', 'h4' )
    net.iperf( (h1, h4) )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    # perfTest()

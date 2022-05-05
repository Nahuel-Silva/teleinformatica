#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s1_wan = net.addSwitch('s1_wan', cls=OVSKernelSwitch, failMode='standalone')
    s2_wan = net.addSwitch('s2_wan', cls=OVSKernelSwitch, failMode='standalone')
    s3_wan = net.addSwitch('s3_wan', cls=OVSKernelSwitch, failMode='standalone')
    s4_wan = net.addSwitch('s4_wan', cls=OVSKernelSwitch, failMode='standalone')
    s5_wan = net.addSwitch('s5_wan', cls=OVSKernelSwitch, failMode='standalone')
    s6_wan = net.addSwitch('s6_wan', cls=OVSKernelSwitch, failMode='standalone')
    s7_lan = net.addSwitch('s7_lan', cls=OVSKernelSwitch, failMode='standalone')
    s8_lan = net.addSwitch('s8_lan', cls=OVSKernelSwitch, failMode='standalone')
    s9_lan = net.addSwitch('s9_lan', cls=OVSKernelSwitch, failMode='standalone')
    s10_lan = net.addSwitch('s10_lan', cls=OVSKernelSwitch, failMode='standalone')
    s11_lan = net.addSwitch('s11_lan', cls=OVSKernelSwitch, failMode='standalone')
    s12_lan = net.addSwitch('s12_lan', cls=OVSKernelSwitch, failMode='standalone')

    r_central = net.addHost('r_central', cls=Node, ip='192.168.100.6/29')
    r_central.cmd('sysctl -w net.ipv4.ip_forward=1')

    r14 = net.addHost('r14', cls=Node, ip='192.168.100.1/29')
    r14.cmd('sysctl -w net.ipv4.ip_forward=1')
    r15 = net.addHost('r15', cls=Node, ip='192.168.100.9/29')
    r15.cmd('sysctl -w net.ipv4.ip_forward=1')
    r16 = net.addHost('r16', cls=Node, ip='192.168.100.17/29')
    r16.cmd('sysctl -w net.ipv4.ip_forward=1')
    r17 = net.addHost('r17', cls=Node, ip='192.168.100.25/29')
    r17.cmd('sysctl -w net.ipv4.ip_forward=1')
    r18 = net.addHost('r18', cls=Node, ip='192.168.100.33/29')
    r18.cmd('sysctl -w net.ipv4.ip_forward=1')
    r19 = net.addHost('r19', cls=Node, ip='192.168.100.41/29')
    r19.cmd('sysctl -w net.ipv4.ip_forward=1')
    

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.254/24', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.2.254/24', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.3.254/24', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.4.254/24', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.5.254/24', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.6.254/24', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(r_central, s1_wan, intfName='r_central-eth0', params1={'ip' : '192.168.100.6/29'})
    net.addLink(r14, s1_wan, intfName='r14-eth0', params1={'ip' : '192.168.100.1/29'})
    net.addLink(r14, s7_lan, intfName='r14-eth1', params1={'ip' : '10.0.1.1/24'})
    net.addLink(h1, s7_lan)
    net.addLink(r_central, s2_wan, intfName='r_central-eth1', params1={'ip' : '192.168.100.14/29'})
    net.addLink(r15,s2_wan, intfName='r15-eth0', params1={'ip' : '192.168.100.9/29'})
    net.addLink(r15, s8_lan, intfName='r15-eth1', params1={'ip' : '10.0.2.1/24'})
    net.addLink( h2, s8_lan)
    net.addLink(r_central, s3_wan, intfName='r_central-eth2', params1={'ip' : '192.168.100.22/29'})
    net.addLink(r16, s3_wan, intfName='r16-eth0', params1={'ip' : '192.168.100.17/29'})
    net.addLink(r16, s9_lan, intfName='r16-eth1', params1={'ip' : '10.0.3.1/24'})
    net.addLink(h3, s9_lan)
    net.addLink(r_central, s4_wan, intfName='r_central-eth3', params1={'ip' : '192.168.100.30/29'})
    net.addLink(r17, s4_wan, intfName='r17-eth0', params1={'ip' : '192.168.100.25/29'})
    net.addLink(r17, s10_lan, intfName='r17-eth1', params1={'ip' : '10.0.4.1/24'})
    net.addLink(h4, s10_lan)
    net.addLink(r_central, s5_wan, intfName='r_central-eth4', params1={'ip' : '192.168.100.38/29'})
    net.addLink(r18, s5_wan, intfName='r18-eth0', params1={'ip' : '192.168.100.33/29'})
    net.addLink(r18, s11_lan, intfName='r18-eth1', params1={'ip' : '10.0.5.1/24'})
    net.addLink(h5, s11_lan)
    net.addLink(r_central, s6_wan, intfName='r_central-eth5', params1={'ip' : '192.168.100.46/29'})
    net.addLink(r19, s6_wan, intfName='r19-eth0', params1={'ip' : '192.168.100.41/29'})
    net.addLink(r19, s12_lan, intfName='r19-eth1', params1={'ip' : '10.0.6.1/24'})
    net.addLink(h6, s12_lan)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1_wan').start([])
    net.get('s8_lan').start([])
    net.get('s4_wan').start([])
    net.get('s6_wan').start([])
    net.get('s5_wan').start([])
    net.get('s3_wan').start([])
    net.get('s11_lan').start([])
    net.get('s2_wan').start([])
    net.get('s10_lan').start([])
    net.get('s12_lan').start([])
    net.get('s7_lan').start([])
    net.get('s9_lan').start([])

    info( '*** Post configure switches and hosts\n')
    net['r_central'].cmd('ip route add 10.0.1.0/24 via 192.168.100.1')
    net['r_central'].cmd('ip route add 10.0.2.0/24 via 192.168.100.9')
    net['r_central'].cmd('ip route add 10.0.3.0/24 via 192.168.100.17')
    net['r_central'].cmd('ip route add 10.0.4.0/24 via 192.168.100.25')
    net['r_central'].cmd('ip route add 10.0.5.0/24 via 192.168.100.33')
    net['r_central'].cmd('ip route add 10.0.6.0/24 via 192.168.100.41')

    net['r14'].cmd('ip route add 192.168.100.0/24 via 192.168.100.6')
    net['r14'].cmd('ip route add 10.0.0.0/21 via 192.168.100.6') 
    
    net['r15'].cmd('ip route add 192.168.100.0/24 via 192.168.100.14')
    net['r15'].cmd('ip route add 10.0.0.0/21 via 192.168.100.14') 

    net['r16'].cmd('ip route add 192.168.100.0/24 via 192.168.100.22')
    net['r16'].cmd('ip route add 10.0.0.0/21 via 192.168.100.22') 

    net['r17'].cmd('ip route add 192.168.100.0/24 via 192.168.100.30')
    net['r17'].cmd('ip route add 10.0.0.0/21 via 192.168.100.30') 

    net['r18'].cmd('ip route add 192.168.100.0/24 via 192.168.100.38')
    net['r18'].cmd('ip route add 10.0.0.0/21 via 192.168.100.38') 

    net['r19'].cmd('ip route add 192.168.100.0/24 via 192.168.100.46')
    net['r19'].cmd('ip route add 10.0.0.0/21 via 192.168.100.46') 

    net['h1'].cmd('ip route add 192.168.100.0/24 via 10.0.1.1')
    net['h1'].cmd('ip route add 10.0.0.0/21 via 10.0.1.1') 

    net['h2'].cmd('ip route add 192.168.100.0/24 via 10.0.2.1')
    net['h2'].cmd('ip route add 10.0.0.0/21 via 10.0.2.1') 

    net['h3'].cmd('ip route add 192.168.100.0/24 via 10.0.3.1')
    net['h3'].cmd('ip route add 10.0.0.0/21 via 10.0.3.1') 

    net['h4'].cmd('ip route add 192.168.100.0/24 via 10.0.4.1')
    net['h4'].cmd('ip route add 10.0.0.0/21 via 10.0.4.1') 

    net['h5'].cmd('ip route add 192.168.100.0/24 via 10.0.5.1')
    net['h5'].cmd('ip route add 10.0.0.0/21 via 10.0.5.1') 

    net['h6'].cmd('ip route add 192.168.100.0/24 via 10.0.6.1')
    net['h6'].cmd('ip route add 10.0.0.0/21 via 10.0.6.1') 

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()


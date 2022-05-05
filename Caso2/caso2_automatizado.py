#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import Host, Node
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class Red:

    def __init__(self, cant_redes):
        self.cant_redes = cant_redes
        self.net = Mininet(topo=None, build=False, ipBase='10.0.0.0/8')
        self.r_central = None

    def redes(self):
        IPs = 8
        pre_ip = '192.168.100'
        list_redes = []
        for red in range(self.cant_redes):
            list_redes.append(pre_ip + '.' + str(int(IPs * red)))
        return list_redes
    
    def generarSwitch(self):
        info('*Add switches\n')
        for i in range(0, self.cant_redes):
            name_wan = "s_wan" + str(i + 1)
            name_lan = "s_lan" + str(i + 1)
            self.net.addSwitch(name_wan, cls=OVSKernelSwitch, failMode='standalone')
            self.net.addSwitch(name_lan, cls=OVSKernelSwitch, failMode='standalone')

    def generarRouter(self):
        info('*Add routers\n')
        self.r_central = self.net.addHost('r_central', cls=Node, defaultRoute=None)
        self.r_central.cmd('sysctl -w net.ipv4.ip_forward=1')
        for i in range(0, self.cant_redes):
            name = 'r' + str(i + 1)
            r = self.net.addHost(name, cls=Node)
            r.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    def generarHost(self):
        info('*Add hosts\n')
        for i in range(0, self.cant_redes):
            pre = '10.0.' + str(i + 1)
            pos = pre + '.254/24'
            name = 'h' + str(i + 1)
            self.net.addHost(name, cls=Host, ip=pos, defaultRoute=None)
    
    def generarLinks(self):
        info('*Add links\n')
        for i in range(0, self.cant_redes):
            s_wan = self.net.get('s_wan' + str(i + 1))
            r = self.net.get('r' + str(i + 1))
            s_lan = self.net.get('s_lan' + str(i + 1))
            h = self.net.get('h' + str(i + 1))
            self.net.addLink(self.r_central, s_wan)
            self.net.addLink(s_wan, r)
            self.net.addLink(r, s_lan)
            self.net.addLink(s_lan, h)
    
    def start(self):
        info('* Starting network\n')
        self.net.build()
        info( '*** Starting controllers\n')
        for controller in self.net.controllers:
            controller.start()
        info('* Starting switches\n')
        for switch in self.net.switches:
            switch.start([])
    
    def generarConf(self, list_redes):
        info( '*** Post configure switches and hosts\n')
        for i in range(0, self.cant_redes):
            r = self.net.get('r' + str(i + 1))
            h = self.net.get('h' + str(i + 1))
            red = list_redes[i].rsplit('.', 1)
            ip = red[0] + '.' + str(int(red[1]) + 6)   
            nodo_eth = 'r_central-eth' + str(i)
            self.r_central.setIP(ip, prefixLen=29, intf=nodo_eth)
            ip2 = red[0] + '.' + str(int(red[1]) + 1)
            eth0 = 'r' + str(i + 1) + '-eth0'
            ip_interna = '10.0.' + str(i + 1) + '.1'
            ip_redHost = '10.0.' + str(i + 1) + '.0/24'
            eth1 = 'r' + str(i + 1) + '-eth1'
            r.setIP(ip2, prefixLen=29, intf=eth0)
            r.setIP(ip_interna, prefixLen=24, intf=eth1)
            cmd = 'ip route add ' + ip_redHost + ' via ' + ip2
            self.r_central.cmd(cmd)
            cmd1 = 'ip route add 10.0.0.0/21 via ' + ip
            r.cmd(cmd1)
            cmd2 = 'ip route add 192.168.100.0/24 via ' + ip
            r.cmd(cmd2)
            cmd3 = 'ip route add 10.0.0.0/21 via ' + ip_interna
            h.cmd(cmd3)
            cmd4 = 'ip route add 192.168.100.0/24 via ' + ip_interna
            h.cmd(cmd4)



    def generarRed(self):
        list_redes = self.redes()
        self.generarSwitch()
        self.generarRouter()
        self.generarHost()
        self.generarLinks()
        self.start()
        self.generarConf(list_redes)
        CLI(self.net)
        self.net.stop()


def main():
    while True:
        while True:
            cant_redes = int(input('Cuantas redes queres crear (menor a 32 o 32)? '))
            break
        if cant_redes > 0 and cant_redes < 33:
            break
        else:
            print("---->NUMERO ENTRE 1 A 32<----")
    caso2 = Red(cant_redes)
    caso2.generarRed()


if __name__ == '__main__':
    setLogLevel('info')
    main()
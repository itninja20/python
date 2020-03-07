
import ipaddress
from ipaddress import *


from time import sleep
import subprocess as sp

from threader import thready
from ping import ping


class Check:
    def __init__(self, interface):
        self.ilist = []
        self.threads = list()
        
        #self.results.setdefault('ssh')
        self.interface = interface
        self.get_ip_list()
        self.ping()

    def get_ip_list(self):
        c = IPv4Network(self.interface, strict=False)
        for i in c:
            self.ilist.append(str(i))

    def ping(self):
        results = {'ping':{}}
        for ip in  self.ilist:
            if '1' in ip[-1] or '0' in ip[-1] or '255' in ip:
                pass
            else:
                x = thready(ping, ip, 'ping')
                self.threads.append(x[0])

                #results['ping'].setdefault(stat[0][0], stat[0][1])
                #print(results['ping'])

                for thread in self.threads:
                    thread.join(timeout=0.05)
                    res = x[1].get()
                    state = str(res).rsplit(':')
                    #p.append([state[0], state[1]])
                    print(state)



    def ssh(self):
        pass

Check('192.168.0.104/24')

def ping_check(): 
    #host_list = get_host_list('192.168.0.104/24')
    #status = threader(host_list,'ping')
    pass


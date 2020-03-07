import ipaddress
from ipaddress import *
import subprocess as sp

import threading
from threading import Lock
from time import sleep
from threading import Thread
import queue

from ssh import client, commander, close_conn
import socket, json


interface = IPv4Interface('192.168.0.104/24')
ip = interface.ip
host_alive = []
stat = {}
stat.setdefault('check', {})
stat['check'].setdefault('ssh', {})
stat['check'].setdefault('ping', {})
stat['check']['ping'].setdefault('alive', {})
stat['check']['ping'].setdefault('dead', {})

def threader(alist, opt):
    
    q = queue.Queue()
    threads = list()
    state = []
    x = None
    for n in range(0,len(alist)):
        print('cheking: ' +  opt)
        host = str(alist[n])
        if '1' in host[-1] or '255' in host:
            pass
        else:
            if 'ping' in opt:
                x = Thread(target=ping, args=(host, q))
            elif 'ssh' in opt:
                x = Thread(target=ssh_check, args=(host, q))
            x.start()
            threads.append(x)
    for thread in threads:
        thread.join(timeout=0.05)
        res = q.get()
        
        if 'ssh' in opt:
            print(res)
            return res
        state.append(res)
    return state

def ping_check(): 
    host_list = get_host_list()
    status = threader(host_list,'ping')
    for i in status:
        c = i.rsplit(' ')
        if 'up' in c[2]:
            stat['check']['ping']['alive'].setdefault(c[0], c[2])
        else:
            stat['check']['ping']['dead'].setdefault(c[0], c[2])
    return stat

def ping(ip, q):
    status, result = sp.getstatusoutput("ping -c1 -W1 " + ip)
    sleep(1)
    if status == 0:
        q.put(ip + ' is up')
    else:
        q.put(ip + ' is down')

def get_host_list():
    ilist = []
    c = IPv4Network(interface, strict=False)
    for i in c:
        ilist.append(i)
    return ilist

def init_ssh_check(host_list):
    status = threader(host_list, 'ssh')
    c = str(status).rsplit(' ')
    if 'OK' in c[-1]:
        stat['check']['ssh'].setdefault(c[0], c[-1])
    return stat

def ssh_port_check(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((host,22))
    r = False
    if result == 0:
        return True

def ssh_check(host,q):
    ok = []
    if ssh_port_check(host):
        ok.append(host)
    else:
        #pass
        print('[ '+host+' ]'+'> port 22 is CLOSED')
    for h in ok:
        p = client(h, 22, 'usr', 'pwd')
        stdout = commander(p, 'whoami')
        close_conn(p)
        q.put(h +' '+ stdout.decode() + '> OK')

def pretty_print(adict):
    ajson = json.dumps(adict, indent=2, sort_keys=True)
    return ajson

if __name__ == "__main__":
    results = ping_check()
    host_up = []
    for item in results['check']['ping'].items():
        if 'up' in item[1]:
            host_up.append(item[0])
    
    ssh_state = init_ssh_check(host_up)

    print(pretty_print(stat['check']['ssh']))



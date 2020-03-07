from collections import deque
import queue
import csv
import datetime
import os
import re
import subprocess as sp
#subprocess
import multiprocessing as mp
import ipaddress
from ipaddress import *
import time

# devicelist.csv = HOSTNAME,IP

def loadDevices():
    with open('devicelist.csv', 'rb') as csvfile:
        devices = csv.reader(csvfile, delimiter=',', quotechar='"')
        dev = [(dev,ip) for dev,ip in devices]
    return dev

def loadIPs():
    loadDevices()
    IPs = [i[1] for i in loadDevices()]
    print (IPs)
    return IPs

def load_ip_list(interface):
    ilist = []
    c = IPv4Network(interface, strict=False)
    for i in c:
        if '0' in str(i)[-1] or '1' in str(i)[-1] or '255' in str(i):
            pass
        else:
            #print(i)
            ilist.append(str(i))
    return ilist

def check(ip):
    """ test an IP address to see if it's up with one ping"""
    """ will feed this an array with mp.Pool.map() """
    IPup = []
    IPdown = []
    #with open(os.devnull, "w") as fnull:
    #status, result = sp.getstatusoutput("ping -c1 -W1 " + ip)
    #print('checking ' + ip)
    state, check = sp.getstatusoutput('ping -c1 -W2' + ip)#,stdout=fnull, stderr=fnull)#==0
    if state == 0:
        print(ip + ' is up')
        return ip
    else:
        #print(ip + ' is down')
        return None
    #print(sp.getstatusoutput("ping -c1 -W1 " + ip))
        # if subprocess.call(['ping','-c 1 -W 1',IP,],stdout=fnull, stderr=fnull)==0:
        #     print ('host %s is UP' % IP)
        #     return IP
        # else:
        #     print ('host %s is DOWN' % IP)
        #     return None

numThreads = 20
ip_list = load_ip_list('192.168.0.104/24')

#for  i in ip_list:  
#    check(i)
#    time.sleep(0.5)

p = mp.Pool(numThreads)

""" IPout is a list of the devices that are UP """
IPout = p.map(check, ip_list)
print(IPout)
p.close()
p.join()


import subprocess as sp

def ping(ip, q):
    status, result = sp.getstatusoutput("ping -c1 -W1 " + ip)
    if status == 0:
        q.put(ip + ':up')
    else:
        q.put(ip + ':down')

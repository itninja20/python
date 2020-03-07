
import threading
from threading import Lock
from time import sleep
from threading import Thread
import queue

def thready(func, ip, opt):
    q = queue.Queue()
    x = Thread(target=func, args=(ip, q))
    x.start()
    return [x,q]


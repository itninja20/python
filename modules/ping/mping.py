
from multiprocessing import Lock, Process, Queue, current_process
import time
import queue
import ipaddress
from ipaddress import *
import subprocess as sp



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

def do_job(tasks_to_accomplish, tasks_that_are_done, ip_list):
    host = None
    while True:
        try:
            '''
                try to get task from the queue. get_nowait() function will 
                raise queue.Empty exception if the queue is empty. 
                queue(False) function would do the same task also.
            '''
            task = tasks_to_accomplish.get_nowait()
        except queue.Empty:

            break
        else:
            '''
                if no exception has been raised, add the task completion 
                message to task_that_are_done queue
            '''
            
            for ip in ip_list:
                print(task)
                
                state, check = sp.getstatusoutput('ping -c1 -W0.5' + ip)
                if state == 0:
                    host = 'alive'
                else:
                    host = 'dead'

                tasks_that_are_done.put(task + ' is done by ' + current_process().name)
                time.sleep(1)
    return True




def main():
    cnt  = 0
    load_ips = load_ip_list('192.168.0.104/24')
    number_of_task = len(load_ips)
    number_of_processes = 10
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    processes = []
    

    for i in range(0, number_of_task):
        tasks_to_accomplish.put("[ "+str(i)+" ] "+"Checking host: " + load_ips[cnt])

    # creating processes
    for w in range(number_of_processes):
        p = Process(target=do_job, args=(tasks_to_accomplish, tasks_that_are_done, load_ips))
        processes.append(p)
        p.start()

    # completing process
    for p in processes:
        p.join()

    # print the output
    while not tasks_that_are_done.empty():
        print(tasks_that_are_done.get())
        cnt+=1

    return True


if __name__ == '__main__':
    main()
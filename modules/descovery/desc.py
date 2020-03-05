
import csv



def reader():
    host_list = [] 
    with open('test.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        line_cnt = 0
        for row in reader:
            if line_cnt is 0:
                line_cnt += 1
            else:
                line_cnt += 1
                char_cnt = len(row[0])
                host_list.append(row[0])
    return host_list

def get_px(host_list):
    for h in host_list:
        if 'p' in h[len(h)-2:len(h)-1]:
            print(h)

def get_qa(host_list):
    for h in host_list:
        if 'v' in h[len(h)-2:len(h)-1]:
            print(h)

def get_ft(host_list):
    for h in host_list:
        if 't' in h[len(h)-2:len(h)-1]:
            print(h)

host_list =  reader()
get_px(host_list)
print('-------------------')
get_qa(host_list)
print('-------------------')
get_ft(host_list)
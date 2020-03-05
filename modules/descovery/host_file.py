

def pxwriter(host):
    with open('inventory/px.ini', 'a+') as px:
        px.write(host)
        px.close()

def qawriter(host):
    with open('inventory/qa.ini', 'a+') as px:
        px.write(host)
        px.close()

def ftwriter(host):
    with open('inventory/ft.ini', 'a+') as px:
        px.write(host)
        px.close()

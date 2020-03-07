
import paramiko

def client(host,port,user,passwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=user, password=passwd, timeout=2)
    return client

def commander(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.read()

def close_conn(client):
    client.close()

# con = client('192.168.0.109',22,'jan','kee5daij')
# out = commander(con, 'whoami')
# print(out)
# close_conn(con)

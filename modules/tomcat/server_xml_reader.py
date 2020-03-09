#!/usr/bin/env python
'''
Parses a Tomcat configuration and will output various helpful 
settings to aide in the review/assessment of the service. 

Copyright (c)2014 Mike Duncan <mike.duncan@waitwha.com>.
'''
import os, sys
import xml.etree.ElementTree as et

path = "."
verbose = False

class bcolors:
    HEADER = '\033[97m'
    BOLD = HEADER
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    YELLOW = WARNING
    FAIL = '\033[91m'
    RED = FAIL
    ENDC = '\033[0m'
    CLEAR = ENDC

class Listener:
  def __init__(self, element):
    self.classname = element.get("className")
    
  def getClassName(self):
    return self.classname

class Resource:
  name = ""
  type = ""
  
  def __init__(self, element):
    self.name = element.get("name")
    self.type = element.get("type")
    
  def getName(self):
    return self.name
    
  def getType(self):
    return self.type

class GlobalNamingResources:
  resources = []
  
  def __init__(self, element):
    for e in element.findall('.//*'):
      if "Resource" in e.tag:
        self.resources.append(Resource(e))
        
  def getResources(self):
    return self.resources

class Connector:
  address = "*"
  port = 8080
  protocol = "HTTP/1.1"
  
  def __init__(self, element):
    self.address = element.get("address")
    if self.address is None:
      print (">> " + bcolors.YELLOW + "Warning"+ bcolors.CLEAR +", Connector element does not have a 'address' attribute. This effectively means that this connector will run on all interfaces.")
      self.address = "*"
    
    self.port = int(element.get("port"))
    self.protocol = element.get("protocol")
  
  def getAddress(self):
    return self.address
    
  def getPort(self):
    return self.port
    
  def getProtocol(self):
    return self.protocol

class Realm:
  classname = ""
  resourceName = ""
  digest = ""
  
  def __init__(self, element):
    self.classname = element.get("className")
    self.resourceName = element.get("resourceName")
    self.digest = element.get("digest")
    
    if self.digest is None and self.resourceName is not None and "UserDatabase" in self.resourceName:
      print (">> " + bcolors.YELLOW + "Warning" + bcolors.CLEAR +", no 'digest' attribute found in UserDatabase Realm (tomcat-users.xml). This means this file could contain plain-text passwords.") 
  
  def getClassName(self):
    return self.classname
    
  def getResourceName(self):
    return self.resourceName
    
  def getDigest(self):
    return self.digest

class Valve:
  className = ""
  
  def __init__(self, element):
    self.className = element.get("className")
    
  def getClassName(self):
    return self.className

class Host:
  name = ""
  appBase = ""
  unpackWARs = False
  autoDeploy = False
  valves = []
  
  def __init__(self, element):
    self.name = element.get("name")
    self.appBase = element.get("appBase")
    self.unpackWARs = (element.get("unpackWARs") == 'true')
    self.autoDeploy = (element.get("autoDeploy") == 'true')
    
    for child in element.findall('.//*'):
      if "Valve" in child.tag:
        self.valves.append(Valve(child))
        
  def getName(self):
    return self.name
    
  def getAppBase(self):
    return self.appBase
    
  def getUnpackWARs(self):
    return self.unpackWARs
    
  def getAutoDeploy(self):
    return self.autoDeploy
    
  def getValves(self):
    return self.valves

class Engine:
  name = ""
  defaultHost = "localhost"
  host = None
  realms = []
  
  def __init__(self, element):
    self.name = element.get("name")
    self.defaultHost = element.get("defaultHost")
    
    for child in element.findall('.//*'):
      if "Host" in child.tag:
        self.host = Host(child)
      elif "Realm" in child.tag:
        self.realms.append(Realm(child))
  
  def getName(self):
    return self.name
    
  def getDefaultHost(self):
    return self.defaultHost
    
  def getHost(self):
    return self.host

class Service:
  connectors = []
  engine = None
  
  def __init__(self, element):
    for child in element.findall('.//*'):
      if "Connector" in child.tag:
        self.connectors.append(Connector(child))
      elif "Engine" in child.tag:
        self.engine = Engine(child)
        
    #print ">> Successfully parsed service: %d connector(s)." % len(self.connectors)
    
  def getConnectors(self):
    return self.connectors
    
  def getEngine(self):
    return self.engine

class Server:
  port = 8005
  shutdown = "SHUTDOWN"
  listeners = []
  globalNamingResources = None
  service = None

  def __init__(self, element):
    port = int(element.get("port"))
    shutdown = element.get("shutdown")
    
    for child in element.findall('.//*'):
      if "Listener" in child.tag:
        self.listeners.append(Listener(child))
      elif "GlobalNamingResources" in child.tag:
        self.globalNamingResources = GlobalNamingResources(child)
      elif "Service" in child.tag:
        self.service = Service(child)
    
    #print ">> Successfully parsed server: %d listener(s)." % len(self.listeners)
    
  def getPort(self):
    return self.port
  
  def getShutdown(self):
    return self.shutdown
  
  def getListeners(self):
    return self.listeners
  
  def getGlobalNamingResources(self):
    return self.globalNamingResources
    
  def getService(self):
    return self.service

class ServerConfParser:
  server = None

  def __init__(self, path):
    print (">> Parsing file %s, please wait..." % path)
    self.dom = et.parse(path)
    
    #print ">> Parsing complete. Finding Server element..."
    root = self.dom.getroot()
    self.server = Server(root)
  
  def getServer(self):
    return self.server

class Role:
  rolename = ""
  
  def __init__(self, element):
    self.rolename = element.get("rolename")
    
  def getRoleName(self):
    return self.rolename

class User:
  username = ""
  password = ""
  roles = []
  
  def __init__(self, element):
    self.username = element.get("username")
    self.password = element.get("password")
    self.roles = element.get("roles").split(",")
    
    if "manager-gui" in self.roles:
      print (">> "+ bcolors.YELLOW +"Warning"+ bcolors.CLEAR +", user '"+ self.username +"' has the 'manager-gui' role. This means this user may administrate Tomcat remotely.")
    
  def getUsername(self):
    return self.username
  
  def getPassword(self):
    return self.password
    
  def getRoles(self):
    return self.roles
    
class TomcatUsersConfParser:

  roles = []
  users = []

  def __init__(self, path):
    dom = et.parse(path)
    root = dom.getroot()
    for element in root.findall('.//*'):
      if "role" in element.tag:
        self.roles.append(Role(element))
      elif "user" in element.tag:
        self.users.append(User(element))
        
  def getUsers(self):
    return self.users
    
  def getRoles(self):
    return self.roles

def main():
  confPath = "%s/%s" % (path, "conf/server.xml")
  print('CONF: ' + confPath)
  if os.path.isfile(confPath):
    parser = ServerConfParser(confPath)
    server = parser.getServer()
    
    print (bcolors.BLUE)
    print ("--[ Tomcat (port tcp/%d) ]-----------------------------------------" % server.getPort())
  
    print (bcolors.BLUE + "Listeners: " + bcolors.CLEAR)
    for listener in server.getListeners():
      print ("\t%s" % listener.getClassName())
    
    print (bcolors.BLUE + "Global Naming Resources: " + bcolors.CLEAR)
    for resource in server.getGlobalNamingResources().getResources():
      print ("\t%s - %s" % (resource.name, resource.type))
    
    print (bcolors.BLUE + "Service Connectors: (* = runs on all interfaces/addresses)" + bcolors.CLEAR)
    for connector in server.getService().getConnectors():
      print ("\t%s:%s (%s)" % (connector.address, connector.port, connector.protocol))

    print (bcolors.BLUE + "Service Engine: " + bcolors.CLEAR)
    print ("\tDefault Host: %s" % server.getService().getEngine().getDefaultHost())
    print ("\tHost: %s " % server.getService().getEngine().getHost().getName())
    print ()
  else:
    print (">> "+ bcolors.RED +"Error"+ bcolors.CLEAR +", could not find the conf/server.xml file in "+ path)
  
  confPath = "%s/%s" % (path, "conf/tomcat-users.xml")
  if os.path.isfile(confPath):
    parser = TomcatUsersConfParser(confPath)
    print (bcolors.BLUE + "--[ Tomcat Users Database ]-----------------------------------------" + bcolors.CLEAR)
    
    if len(parser.getRoles()) > 0:
      print (bcolors.BLUE + "Role(s):" + bcolors.CLEAR)
      for role in parser.getRoles():
        print ("\t%s" % role.getRoleName())
    
      print (bcolors.BLUE + "User(s):" + bcolors.CLEAR)
      for user in parser.getUsers():
        print ("\t%s (%s)" % (user.getUsername(), ",".join(user.getRoles())))
    else:
      print ("(No users/roles were defined in tomcat-users.xml)")
    
    print ()
  else:
    print (">> "+ bcolors.RED +"Error"+ bcolors.CLEAR +", could not find the conf/tomcat-users.xml file in "+ path)
    
  webApps = "%s/%s" % (path, "webapps")
  if os.path.exists(webApps):
    print (bcolors.BLUE + "--[ Web Applications Deployed ]------------------------------------" + bcolors.CLEAR)
    for entry in os.listdir(webApps):
      if "." in entry:
        continue
        
      print ("\t%s" % entry)
      
    print()

if __name__=='__main__':
  if len(sys.argv) == 2:
    path = sys.argv[1]
  
  main()
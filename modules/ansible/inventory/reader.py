import ConfigParser

config = ConfigParser.RawConfigParser()

config.read('hosts.ini')

print config.get('servers')
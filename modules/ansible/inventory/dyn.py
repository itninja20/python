import ConfigParser

try:
    import json
except ImportError:
    import simplejson as json





def httpd():
    dyn = dict()
    config = ConfigParser.RawConfigParser()
    config.read('hosts.ini')
    for section in config.sections():
        for option in config.options(section):
            test = [section, option, config.get(section, option)]
            dyn.setdefault(section,{})
            dyn[section].setdefault('hosts',[])
            dyn[section].setdefault('host_vars',{})
            dyn[section].setdefault('group_vars',{})
            #print(test)
            #print('------------')
            print(dyn[section])
            dyn[section]['hosts']
            dyn[section]['host_vars']
            dyn[section]['group_vars']

httpd()
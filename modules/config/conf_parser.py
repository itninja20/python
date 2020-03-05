import ConfigParser

config = ConfigParser.RawConfigParser()


def httpd():
    config.read('httpd.ini')
    print (config.get('main', 'conf.d'))

def tomcat():
    config.read('tomcat.ini')
    print (config.get('main', 'app_dir'))

httpd()
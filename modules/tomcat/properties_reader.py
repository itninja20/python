
#import ConfigParser

#config = ConfigParser.RawConfigParser()

path = '.'


class Catalina:

    def __init__(self, path):
        self.path = path

    def reader(self):
        ci = {}
        with open(self.path) as f:
            cont = f.readlines()
            for l in cont:
                if '#' not in l:
                    if '=' in l:
                        if '\\' not in l:
                            if len(l.rsplit('=')[1]) > 1:
                                ci.setdefault(l.rsplit('=')[0], l.rsplit('=')[1])
                                print(l.rsplit('=')[0])
                        if 'jarsToSkip' in l:
                            ci.setdefault(l.rsplit('=')[0], [])
                        if 'jarsToScan' in l:
                            ci.setdefault(l.rsplit('=')[0], [])
                    elif '$' not in l:
                        if len(l) > 2 and ',org' not in l:
                            if ',' in l and 'jarsToScan' not in l:
                                #print(l)
                                pass
                            elif 'jarsToScan' in l:
                                break
                            else:
                                #print(l)
                                pass
                                #input('ENTER')
                        elif 'jarsToScan' in l:
                            break
        print(ci.keys())


def main():
    p = Catalina('./conf/catalina.properties')
    p.reader()


if __name__=='__main__':
    main()
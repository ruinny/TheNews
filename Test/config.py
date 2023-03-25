from configparser import ConfigParser


def readconfig():
    file = 'config.ini'
    config = ConfigParser()
    config.read(file, encoding='utf-8')
    return config

config=readconfig()
print(config.sections())




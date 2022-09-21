from ast import parse
import configparser
import os

#################
## DATI FISSI ###
#################
INIFolder = os.getcwd() + '\\INI\\'
ResourceFolder = os.getcwd() + '\\RES\\'
CFGFile = INIFolder + 'Configuration.ini'
fileHELP = INIFolder + 'help.ini'

#---------------------------
def INIREAD(param):
    parser = configparser.ConfigParser(strict=False)
    parser.read_file(open(CFGFile,encoding='utf-8'))  # leggo il file di configurazione

    for section_name in parser.sections():
        # print ('Section:', section_name)
        # print ('  Options:', parser.options(section_name))
    
        parserDict = dict(parser.items(section_name)) # trasformo in dizionario

    return parserDict[param]
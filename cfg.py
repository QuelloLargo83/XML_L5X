#from ast import Str
from argparse import HelpFormatter
import os,sys
import configparser
from os import listdir
from os.path import isfile, join

#########################################
## check del sistema su cui sta girando #
#########################################
SYSTEM: str
if "linux" in sys.platform: SYSTEM = "Linux"
elif "win32" in sys.platform: SYSTEM = "Windows"
else: SYSTEM = "Other"

match SYSTEM:    
    case "Linux":
        bars = '/'
    case "Windows":
        bars = '\\'

INIFolder = os.getcwd() + bars + 'INI' + bars          # Cartella dei file INI
ResourceFolder = os.getcwd() + bars + 'RES'+ bars      # Cartella con le risorse
CFGFile = INIFolder + 'Configuration.ini'    # File di configurazione
fileHELP = INIFolder + 'help.ini'            # File di Help

#################
## DATI FISSI ###
#################
fileControllerTags = 'ControllerTags.txt'
fileIOMESSAGE_Pre = 'IOMESSAGES_PLXXXX.ENG'         # OUT:
fileIOMESSAGE = 'IOMESSAGES_PLXXXX'                 # OUT:

Sep = '..'                                          # separatore per parti della stringa IOMESSAGE
IntouchEncoding = 'utf-16-le'                       # codifica della maggior parte dei file ini 
NomeCartellaOUT = 'IO_OUT'                          # cartella appoggio per coppie di file IOMESSAGE in cwd
NomeCartellaFINALE = 'IO_OUTFINALE'                 # cartella con risultato finale in cwd per IOMESSAGE
NomeCartPhasesOUT = 'PHASES_out'                    # cartella in cui mettere i file PHASES

##########
# COLORS #
##########
# Raccolta colori per i significati delle scritte
#
ColorInfo = 'cyan' # infomsg

def INIREAD(param):
    """Legge il valore di un parametro dal file Configuration.ini

    Args:
        param (any): parameter in INIFILE

    Returns:
        str: value of the parameter requested
    """
    parser = configparser.ConfigParser(strict=False)
    parser.read_file(open(CFGFile,encoding='utf-8'))  # leggo il file di configurazione

    # # QUESTO LEGGE TUTTE LE SEZIONI
    # for section_name in parser.sections():
    #     parserDict = dict(parser.items(section_name)) # trasformo in dizionario

    # LEGGO SOLO LA SEZIONE SETUP
    parserDict = dict(parser.items('SETUP')) # trasformo in dizionario

    return parserDict[param]






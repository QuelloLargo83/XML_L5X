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

#####################################
## DATI CFG INTERNA DEL PROGRAMMA ###
#####################################

INIFolder = os.getcwd() + bars + 'INI' + bars          # Cartella dei file INI
ResourceFolder = os.getcwd() + bars + 'RES'+ bars      # Cartella con le risorse
CFGFile = INIFolder + 'Configuration.ini'              # File di configurazione
fileHELP = INIFolder + 'help.ini'                      # File di Help
PhaseINI = INIFolder + 'CyclesPhMsg.ini'               # File associazione Ciclo -> Struttura PhaseMSG

#################
## DATI FISSI ###
#################
fileControllerTags = 'ControllerTags.txt'
fileIOMESSAGE_Pre = 'IOMESSAGES_PLXXXX.ENG'         # OUT:
fileIOMESSAGE = 'IOMESSAGES_PLXXXX'                 # OUT:

Sep = '..'                                          # separatore per parti della stringa IOMESSAGE
IntouchEncoding = 'utf-16-le'                       # codifica della maggior parte dei file ini 
NomeCartellaOUT = 'IO_OUT_APP'                          # cartella appoggio per coppie di file IOMESSAGE in cwd
NomeCartellaFINALE = 'IO_OUT'                 # cartella con risultato finale in cwd per IOMESSAGE
NomeCartPhasesOUT = 'PHASES_OUT'                    # cartella in cui mettere i file PHASES

##########
# COLORS #
##########
# Raccolta colori per i significati delle scritte
#
ColorInfo = 'cyan' # infomsg


############
## CLASSI ##
############
class MyParser(configparser.ConfigParser):
    """Decoratore della classe configparser
       aggiunge il metodo per trasformare l'oggetto in dizionario
    """
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


##############
## FUNZIONI ##
##############

def INIREAD(param):
    """Legge il valore di un parametro dal file Configuration.ini

    Args:
        param (any): parameter in INIFILE

    Returns:
        str: value of the parameter requested
    """
    parser = configparser.ConfigParser(strict=False)
    parser.read_file(open(CFGFile,encoding='utf-8'))  # leggo il file di configurazione

    # LEGGO SOLO LA SEZIONE SETUP
    parserDict = dict(parser.items('SETUP')) # trasformo in dizionario

    return parserDict[param]


## RIVEDERE EXCEPT! bisogna che indichi sia la sezione che il parametro
def INIREAD_G(IniFile, SectionName, Param):
    """Restituisce il valore di un parametro da un file INI

    Args:
        IniFile (str): percorso completo del file ini
        SectionName (str): nome della sezione in cui cercare all'interno del file ini
        Param (str): parametro di cui si intende sapere il valore 

    Returns:
        any: valore del parametro cercato o stringa con non trovato
    """
    parserNew = MyParser(strict=False)
    parserNew.read_file(open(IniFile,encoding='utf-8'))  # leggo il file di configurazione

    #parserNew.as_dict() # mi un dizionario con tutto l'INI le cui chiavi di primo livello sono le sezioni
    try:
        SectionLevel = parserNew.as_dict()[SectionName] 
        valore = SectionLevel[Param]
    except(KeyError):
        valore = SectionName + ' or ' + Param + ' not Found '
    return valore
    

def INIREAD_COPPIE(IniFile):
    """Recupera un file ini e lo trasoforma in un dizionario mantendo il case

    Args:
        IniFile (str): percorso completo del file INI

    Returns:
        dict: rappresentazione in dizionario del file INI
    """
    parser = MyParser(strict=False)
    parser.optionxform = str # mantiene il case delle chiavi!!!
    parser.read_file(open(IniFile,encoding='utf-8')) # leggo il file di cfg

    ret = parser.as_dict()

    return ret


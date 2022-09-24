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


# INIFolder = os.getcwd() + '\\INI\\'          # Cartella dei file INI
# ResourceFolder = os.getcwd() + '\\RES\\'     # Cartella con le risorse
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

######################
## DATI da cfg.ini ###
######################

# LETTURA FILE CONFIGURAZIONE 
# CFGParser = configparser.ConfigParser(strict= False)
# CFGParser.read_file(open(CFGFile,encoding='utf-8')) 
# CFGlista_sezioni = CFGParser.sections()
# CFGlista = CFGParser.items(CFGlista_sezioni[0])    
# CFGlistaDICT = dict(CFGlista)    # metto tutto dentro un dizionario per comodita di accesso

# DATI ESTRATTI DAL FILE DI CONFIGURAZIONE
#filePLC = CFGlistaDICT['fileplc']                         # IN: file L5X sorgente dal PLC
#fileCFG_PAGE = CFGlistaDICT['filecfgpage']                # IN: file contenente lista macchine esterne
#Fx_Cx = CFGlistaDICT['fx_cx']                             # IN: tipo di macchina
# PLCProdCycleVAR = CFGlistaDICT['plcprodcyclevar']         # Area Memoria PLC per cicli Produzione
# PLCSanCycleVar = CFGlistaDICT['plcsancyclevar']           # Area Memoria PLC per cicli Sanificazione
# CFG_IOMAC = int(CFGlistaDICT['cfg_iomac'])                # Numero sezione CFG_IOMAC 
# fileCicliProd =  CFGlistaDICT['filecicliprod']            
# fileCicliSan = CFGlistaDICT['fileciclisan']           
###########################################################




#from ast import Str
from argparse import HelpFormatter
import os
import configparser
from os import listdir
from os.path import isfile, join


INIFolder = os.getcwd() + '\\INI\\'
ResourceFolder = os.getcwd() + '\\RES\\'
CFGFile = INIFolder + 'Configuration.ini'    
fileHELP = INIFolder + 'help.ini'

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
    """_summary_

    Args:
        param (any): parameter in INIFILE

    Returns:
        str: value of the parameter requested
    """
    parser = configparser.ConfigParser(strict=False)
    parser.read_file(open(CFGFile,encoding='utf-8'))  # leggo il file di configurazione

    for section_name in parser.sections():
        parserDict = dict(parser.items(section_name)) # trasformo in dizionario

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




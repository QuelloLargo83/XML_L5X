#from ast import Str
from argparse import HelpFormatter
import cmd
import os
import sys
import l5x
import configparser
import utils
import HelpMNG
from os import listdir
from os.path import isfile, join


#################
## DATI FISSI ###
#################

CFGFile = os.getcwd() + '\Configuration.ini'
fileHELP = 'help.ini'
ResourceFolder = os.getcwd() + '\\RES\\'

PLCProdCycleVAR = 'D40_00'
PLCSanCycleVar = 'D60_00'

fileCicliProd = 'NomiCicliProd.txt'                 # OUT
fileCicliSan = 'NomiCicliSan.txt'           
fileControllerTags = 'ControllerTags.txt'
fileIOMESSAGE_Pre = 'IOMESSAGES_PLXXXX.ENG'         # OUT:
fileIOMESSAGE = 'IOMESSAGES_PLXXXX'                 # OUT:

Sep = '..'                                          # separatore per parti della stringa IOMESSAGE
IntouchEncoding = 'utf-16-le'                       # codifica della maggior parte dei file ini 
NomeCartellaOUT = 'IO_OUT'                             # cartella appoggio per coppie di file IOMESSAGE in cwd
NomeCartellaFINALE = 'IO_OUTFINALE'                    # cartella con risultato finale in cwd per IOMESSAGE


######################
## DATI da cfg.ini ###
######################

# LETTURA FILE CONFIGURAZIONE 
CFGParser = configparser.ConfigParser(strict= False)
CFGParser.read_file(open(CFGFile,encoding='utf-8')) 
CFGlista_sezioni = CFGParser.sections()
CFGlista = CFGParser.items(CFGlista_sezioni[0])    
CFGlistaDICT = dict(CFGlista)    # metto tutto dentro un dizionario per comodita di accesso
#print(CFGlista)

# DATI ESTRATTI DAL FILE DI CONFIGURAZIONE
filePLC = CFGlistaDICT['fileplc']                               # IN: file L5X sorgente dal PLC
fileCFG_PAGE = CFGlistaDICT['filecfgpage']                # IN: file contenente lista macchine esterne
Fx_Cx = CFGlistaDICT['fx_cx']                             # IN: tipo di macchina
#PLCProdCycleVAR = eval(CFGlistaDICT['plcprodcyclevar'])  # Area Memoria PLC per cicli Produzione
#PLCSanCycleVar = eval(CFGlistaDICT['plcsancyclevar'])    # Area Memoria PLC per cicli Sanificazione
CFG_IOMAC = int(CFGlistaDICT['cfg_iomac'])               # Numero sezione CFG_IOMAC 

###########################################################
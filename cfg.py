#from ast import Str
from argparse import HelpFormatter
import os,sys
import configparser
from os import listdir
from os.path import isfile, join
import utils



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

INIFolder = os.getcwd() + bars + 'INI' + bars                   # Cartella dei file INI
ResourceFolder = os.getcwd() + bars + 'RES'+ bars               # Cartella con le risorse
HMIFolder = INIFolder  + 'HMI' + bars
SETUPfile = HMIFolder + 'SETUP_HMI.ini'                         # file SETUP_HMI.ini
PLCFilFolder = INIFolder  + 'PLC' + bars + 'FILLER' + bars
PLCProFolder = INIFolder  + 'PLC' + bars + 'PROCESSO' + bars
CFGFile = INIFolder + 'Configuration.ini'                       # File di configurazione
fileHELP = INIFolder + 'help.ini'                               # File di Help
PhaseINI = INIFolder + 'CyclesPhMsg.ini'                        # File associazione Ciclo -> Struttura PhaseMSG

#################
## DATI FISSI ###
#################
fileControllerTags = 'ControllerTags.txt'
fileIOMESSAGE_Pre = 'IOMESSAGES_PLXXXX.ENG'         # OUT:
fileIOMESSAGE = 'IOMESSAGES_PLXXXX'                 # OUT:

Sep = '..'                                          # separatore per parti della stringa IOMESSAGE
DisablingChar = '_'
TagChar = '~'                                       # carattere usato nei phase message per evidenziare le tag (~CA1)
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
ColorAlarm = 'red' # alarmmsg


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

def INIREAD2(IniFile,Section,param,Encoding):
    """legge un parametro all'interno di una sezione di un file ini

    Args:
        IniFile (str): percorso completo del file ini
        Section (str): nome sezione (senza parentesi quadre)
        param (str): parametro (o chiave) 
        Encoding (str): encoding del file ini (es: utf-8)

    Returns:
        dict: valore del parametro richiesto (ogni chiave rappresenta un carattere)
    """
    parser = configparser.ConfigParser(strict=False)
    parser.read_file(open(IniFile,encoding=Encoding))  # leggo il file di configurazione

    parserDict = dict(parser.items(Section)) # trasformo in dizionario
    return parserDict[param]

def INIREADKeys(IniFile,Section,Encoding):
    """Restituisce l'elenco delle chiavi di una sezione di un ini file

    Args:
        IniFile (str): percorso completo del file ini
        Section (str): sezione all'interno del file ini (senza parentesi quadre)
        Encoding (str): encoding del file ini (es: utf-8)

    Returns:
        list: lista delle chiavi della sezione 
    """
    parser = configparser.ConfigParser(strict=False)
    parser.read_file(open(IniFile,encoding=Encoding))  # leggo il file di configurazione

    # LEGGO SOLO LA SEZIONE SETUP
    parserDict = dict(parser.items(Section)) # trasformo in dizionario
    return list(parserDict.keys())

def INIGETMacCodes():
    """Ricava la lista dei nomi commerciali delle macchine configurate nel file SETUP_HMI.ini (es: CA1, CI1,..)

    Returns:
        list: lista senza duplicati dei nomi commerciali
    """
    AppoFile = 'trashINI.ini'
    CodeList =[]

    # leggo il file SETUP_HMI.ini e copio in un file di appoggio
    # solo la parte che mi serve
    with open(SETUPfile,'r',encoding=IntouchEncoding) as setupFILE:
        content = setupFILE.readlines()

        count = 0
        for line in content:
            if utils.left(line,5) == '[CFG]':
                with open(AppoFile,'w',encoding='utf-8') as out:
                    for l in content[count:]:
                        if utils.left(l,1) != '{':  # rimuovo commenti che non sono INI approved
                            out.write(l)
            count +=1

    # leggo la lista delle macchine presenti nel SETUP_HMI
    listParam = INIREADKeys(AppoFile,'CFG','utf-8')
        
    for par in listParam:
        code = INIREAD2(AppoFile,'CFG',str(par),'utf-8').split(';')[3].strip()  # il codice commerciale è il terzo campo
        if code != '0' and code != 'XXX': # filtro il global e le non configuate
            CodeList.append(code)

    # cancello il file di appoggio
    if os.path.exists(AppoFile):
        os.remove(AppoFile)
    
    CodeList = list(set(CodeList)) # rimuovo eventuali duplicati

    return CodeList
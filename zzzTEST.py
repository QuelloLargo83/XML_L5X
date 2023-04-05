import cfg
import os
import utils
import configparser
import sys

class MyParser(configparser.ConfigParser):
    """Decoratore della classe configparser
       aggiunge il metodo per trasformare l'oggetto in dizionario
    """
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)


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
        

#-----------------------------
INIFolder = os.getcwd() + cfg.bars + 'INI' + cfg.bars
HMIFolder = INIFolder  + 'HMI' + cfg.bars

SETUPfile = HMIFolder + 'SETUP_HMI.ini'


AppoFile = 'trashINI.ini'

# leggo il file SETUP_HMI.ini e copio in un file di appoggio
# solo la parte che mi serve
with open(SETUPfile,'r',encoding=cfg.IntouchEncoding) as setupFILE:
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
    code = INIREAD2(AppoFile,'CFG',str(par),'utf-8').split(';')[3]
    print (code.strip())

# cancello il file di appoggio
if os.path.exists(AppoFile):
    os.remove(AppoFile)
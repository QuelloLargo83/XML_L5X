import os
import cfg
import shutil
from termcolor import colored
import json

# IntouchEncoding = 'utf-16-le'                       # codifica della maggior parte dei file ini

def left(s, amount):
    """Restituisce la parte sinistra di una stringa

    Args:
        s (str): stringa in cui cercare
        amount (int): quantita di caratteri

    Returns:
        str: parte sinistra
    """
    return s[:amount]

def right(s, amount):
    """Restituisce la parte destra di una stringa

    Args:
        s (str): stringa in cui cercare
        amount (int): quantita di caratteri

    Returns:
        str: parte destra
    """
    return s[-amount:]

def mid(s, offset, amount):
    """Restituisce una perte delimitata di una stringa

    Args:
        s (str): stringa in cui cercare
        offset (int): indice di partenza
        amount (int): quantita di caratteri

    Returns:
        str: substring
    """
    return s[offset:offset+amount]

def OutFileUTF16(fileOut,Input):
    """Crea un file di output in utf-16-le e scrive la stringa passata
       Se il file non esiste lo crea
       le stringhe vengono aggiunte al file

    Args:
        fileOut (str): Nome File OutPut
        Input (str): stringa da stampare
    """
    with open(fileOut,'a',encoding=cfg.IntouchEncoding) as f:
        f.write(Input + '\n')

def OutFileUCS2LeBom(fileOut,Input):
    """Crea un file di output in utf-16-le e scrive la stringa passata
       Se il file non esiste lo crea
       le stringhe vengono aggiunte al file

    Args:
        fileOut (str): Nome File OutPut
        Input (str): stringa da stampare
    """
    with open(fileOut,'a',encoding='utf-16') as f:
        f.write(Input + '\n')



def DeleteFilesInFolder(folder):
    """Cancella tutti i files presenti in una cartella

    Args:
        folder (str): percorso della cartella da cui rimuovere i files
    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(colored('INFO > ',cfg.ColorInfo)+' DeleteFilesInFolder: Failed to delete %s. Reason: %s' % (file_path, e))

def DeleteFolder(path):
    """cancella una cartella

    Args:
        path (_type_): percorso completo della cartella
    """
    try:
        shutil.rmtree(path)
    except Exception as e:
        print(colored('INFO > ', cfg.ColorInfo) + str(e))

def indices(lst, element):
    """restituisce un array con gli indici delle occorrenze di elemnt in list

    Args:
        lst (list): lista da scorrere
        element (any): elemento 

    Returns:
        list: lista degli indici
    """
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
        except ValueError:
            return result
        result.append(offset)

def find_between( s, first, last ):
    """estrae una sottostringa tra due caratteri o stringhe all'interno di un'altra stringa

    Args:
        s (string): stringa completa
        first (str): carattere o stringa iniziale 
        last (str): carattere o stringa finale

    Returns:
        str: sottostringa cercata
    """
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ''

def JsonPrettify(Dict: dict):
    """stampa un dizionario in modo leggibile su terminale

    Args:
        Dict (dict): un dizionario da stampare
    """
    pretty = json.dumps(Dict,indent=4)
    print (pretty)
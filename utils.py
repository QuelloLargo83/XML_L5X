import os
import cfg
import shutil
from termcolor import colored

# IntouchEncoding = 'utf-16-le'                       # codifica della maggior parte dei file ini

def left(s, amount):
    """Restituisce la parte sinistra di una stringa

    Args:
        s (str): _description_
        amount (int): _description_

    Returns:
        _type_: _description_
    """
    return s[:amount]

def right(s, amount):
    """Restituisce la parte destra di una stringa

    Args:
        s (str): _description_
        amount (int): _description_

    Returns:
        _type_: _description_
    """
    return s[-amount:]

def mid(s, offset, amount):
    """Restituisce una perte delimitata di una stringa

    Args:
        s (str): _description_
        offset (int): _description_
        amount (int): _description_

    Returns:
        _type_: _description_
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
    try:
        shutil.rmtree(path)
    except Exception as e:
        print(colored('INFO > ', cfg.ColorInfo) + str(e))
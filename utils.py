IntouchEncoding = 'utf-16-le'                       # codifica della maggior parte dei file ini

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
    with open(fileOut,'a',encoding=IntouchEncoding) as f:
        f.write(Input + '\n')
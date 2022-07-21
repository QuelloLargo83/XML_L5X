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
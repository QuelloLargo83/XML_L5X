import configparser

def GetHelp(HelpFile,cmdswitch):
    """Gestione Help

    Args:
        HelpFile (str): Percorso completo del file ini di Help
        cmdswitch (str): nome dello swith di cui si vuole conoscere la funzione
    Return:
        stampa la descrizione del cmdswitch
    """
    helpParser = configparser.ConfigParser(strict= False)
    helpParser.read_file(open(HelpFile,encoding='utf-8')) 

    HELPlista_sezioni = helpParser.sections()               # lista con le sezioni
    HELPlista_cmd = helpParser.items(HELPlista_sezioni[0])    
    HELPlista_cmdDICT = dict(HELPlista_cmd)    
    
    # Se non specifico alcun command switch restituisco tutto il file di help
    if cmdswitch is None:
        print ('** SWITCH HELP **')
        for k,v in HELPlista_cmdDICT.items():
            print ('--' + k + ' : ' + v)
    # altrimenti recupero la descrizione dello switch
    else:
        for k,v in HELPlista_cmdDICT.items():
            if k == cmdswitch:
                print ('HELP for switch: --' + cmdswitch + '\n')
                print ('--'+cmdswitch + ' : ' + v)
            # else:
            #     print ('Help not FOUND for --'+ cmdswitch)
import l5x
import utils
import os

l5xFile = 'F:\SCRIPTING\XML_L5X\INI\PLC\STERILCAP\P16378_PLC_00P.L5X'
fileTagName = 'F:\SCRIPTING\XML_L5X\TagNameListLang_PLxxxx.ENG'

# ricavo la struttura delle variabili
prj = l5x.Project(l5xFile)
tags = prj.controller.tags





def ExportTagsComments(tags,outfile):
    """crea un file di testo con i commenti delle tags (TagNameListLang)

    Args:
        tags (ElementDict): variabili da cui ricavare i commenti dal plc
        outfile (str): percorso completo del file di output
    """
   
    # lista di tutti le possibili iniziali delle variabili con commento
    deviceCodes = ['CONC','DGTA','DGTL','DGTH','FLWL','FLWN','FLWV','LVLM','MMOD','MOTR','PRSM','PRSP','TEMP','VALV','VMOD','VOLU','WGTG']

    # lista con le variabili a livello controllore
    nomi_variabili = tags.names
    
    # cancello il file di output se già esiste
    if os.path.exists(outfile):
        os.remove(outfile)

    utils.OutFileUCS2LeBom(outfile,'[TAGNAMELISTLANG]')

    for n in nomi_variabili:
        # la lunghezza delle variabili è 17 (esempio MOTR_SH1_D61PPX01)
        if utils.left(n,4) in deviceCodes and len(n)==17:
            line = n +' = ' + tags[n].description.replace('\n',' ')
            utils.OutFileUCS2LeBom(outfile,line)

ExportTagsComments(tags,fileTagName)
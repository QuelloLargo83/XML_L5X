import l5x
import cfg

FilL5X = 'F:\SCRIPTING\XML_L5X\INI\PLC\FILLER\P16255_PLC_02C_M18.L5X'
prj = l5x.Project(FilL5X)
programs = prj.programs




def line_num_for_phrase_in_file(phrase, filename):
    """ricava il numero della riga in cui compare una frase
    """
    with open(filename,encoding='utf8') as f:
        for (i, line) in enumerate(f):
            if phrase in line:
                return i
    return -1

def GetPhCommentList(textToSearch,l5xFile):
    """Ricava la parte relativa al testo cercato fino a </Comment>\n nel CDATA del file l5x

    Args:
        textToSearch (str): es: ## D40_00.Production.Phase - MESSAGE FOR HMI ##
        l5xFile (str): percorso in cui cercare la stringa
    """

    # ricavo il numero della linea all'interno del file in inizia la struttura dei commenti
    lnum = line_num_for_phrase_in_file(textToSearch,l5xFile)

    with open(l5xFile,encoding='utf8') as f:
        # prendo un area dopo la parola in cui ragionevolmente ci sono tutte le fasi
        lineList = f.readlines()[lnum:lnum+100]
        
        # ricavo l'indice di dove finisce l'area dei commenti del rung
        commentIdx = lnum+100 #inizializzo per evitare errore quando non esiste il commento
        if '</Comment>\n' in lineList:
            commentIdx = lineList.index('</Comment>\n')

        return(lineList[0:commentIdx])



def GetPhaseComments(FileL5X,StructCicli,DesinenzaStruct,NomePOSPlc):
    """Ricava un dizionario le cui chiavi sono i cicli (es: D40_00.Production.Phase) e i valori sono i commenti
       dal file l5x prendendo dai commenti dei rung
       ATTENZIONE: ad agosto 2023 nei commenti ci sono solo i .Phase

    Args:
        FileL5X (str): percorso completo del file l5x in cui cercare i commenti delle fasi
        StructCicli (str): es: D40_00
        DesinenzaStruct (str): es: Phase, CycleMSG, PhaseMSG
        NomePOSPlc (str): es FILLER, STERILCAP

    Returns:
        dict: key: nomeCiclo, value: commenti
    """

########## RECUPERO I NOMI DEI CICLI NEL FILE L5X
    # definisco un dizionario vuoto in cui mettere le variabili che mi interessano
    cicli = {}
    cicli = programs[NomePOSPlc].tags[StructCicli].value
    
    # le chiavi sono i nomi del livello figlio della struttura
    nomi_cicli = cicli.keys()

    CycList =  list(nomi_cicli)

#######   
    # scorro i nomi dei cicli e li certo nel file l5x
    comments = {}
    for cycle in CycList:
        nomeCiclo =  cycle.replace('\n','')
        # text ='## D40_00.' + nomeCiclo + '.Phase - MESSAGE FOR HMI ##'
        text ='## '+ StructCicli +'.' + nomeCiclo + '.'+ DesinenzaStruct +' - MESSAGE FOR HMI ##'
        CommentStruct = GetPhCommentList(text,FileL5X)
        if CommentStruct: # se manca la stringa nel posto in cui me lo aspetto, la struttura è vuota e quindi non la cago
            comments[StructCicli +'.'+ nomeCiclo +'.'+ DesinenzaStruct] = CommentStruct[1:] #ogni chiave è il nome del ciclo piu caratteri per riconoscerla 
        
    return comments
  





ProdPhase = GetPhaseComments (FilL5X,cfg.INIREAD('plcprodcyclevar'),'Phase','FILLER')


print(ProdPhase)
import os
import l5x
###########
## DATI ###
###########

file = 'P16164_PLC_20220609_00C.L5X'                # file L5X sorgente dal PLC
fileCicliProd = 'NomiCicliProd.txt'
fileControllerTags = 'ControllerTags.txt'
fileIOMESSAGE = 'IOMESSAGES_PLXXXX.ENG'
PLCProdCycleVAR = 'D40_00'
Sep = '..'                                          # separatore per parti della stringa IOMESSAGE

###########################################################








#####

def OutFileUTF16(fileOut,Input):
    """Crea un file di output in utf-16-le e scrive la stringa passata
       Se il file non esiste lo crea
       le stringhe vengono aggiunte al file

    Args:
        fileOut (str): Nome File OutPut
        Input (str): stringa da stampare
    """
    with open(fileOut,'a',encoding='utf-16-le') as f:
        f.write(Input + '\n')

def SignalExc (NomeSegnale,AccessName):
    """_summary_

    Args:
        NomeSegnale (_type_): _description_
    """
    # cancello il file di output se esiste
    if os.path.exists(fileIOMESSAGE):
            os.remove(fileIOMESSAGE)

    # ricavo la prima parte (SX o DX in base al nome del segnale FROM or TO)
    FromTo = NomeSegnale[9:11] # puo essere Fr o To
    match FromTo.lower():
        case 'fr':
            FirstCol = 'SX'
        case 'to':
            FirstCol = 'DX'


    # scambio è un dizionario le cui chiavi rappresentano i nomi dei segnali di scambio
    scambio = ctl_tags[NomeSegnale].value

    #le chiavi rappresentano i campi dei segnali di scambio
    # for s in scambio.keys():
    #     print(s)
    comment = [] # bisogna ricavarlo dalle chiavi
    lev2str = [] # coverto poi l'oggetto in stringa (lista di char)
    n = 1        # incrementale della prima colonna S01, SX02, ecc

    for s in scambio.keys():
        lev2 = ctl_tags[NomeSegnale][s] # oggetto EnumDict che contiene l'informazione sul tipo di dato
        lev2str = str(lev2) #converto l'oggetto in stringa
        type = lev2str[9:13] # recupero il tipo di dato con un mid dell'oggetto
        #print (lev2str[9:13], ':',s) 

        comment = s #per ora commento = variabile l'idea sarebbe di guardare dove ci sono i caratteri maiuscoli e poi inserire uno spazio
        

        # dal tipo ricavo la lettera (D : digital, A: analog)
        match type:
            case 'BOOL':
                PRE = 'D'
            case 'INT':
                PRE = 'A'
            case 'DINT':
                PRE = 'A'
            case 'SINT':
                PRE = 'A'
        
        if n in range(1,10):
            n = '0' + str(n)

        #compongo l'uscita
        Out = FirstCol + str(n) + " = " + PRE + Sep + AccessName +'.' + NomeSegnale + '.' + s + Sep + comment
        OutFileUTF16(fileIOMESSAGE,Out)
        n = int(n) + 1 

##########
## MAIN ##
##########

# carico il file L5X in memoria
prj = l5x.Project(file)

# ctl_tags è un ElementDict contenente le tag a livello controllore
ctl_tags = prj.controller.tags
# lista tag name livello controllore
tag_names = ctl_tags.names

# lista nomi programmi
programs_names = prj.programs.names

# ELEMENTDICT 
programs = prj.programs

# definisco un dizionario vuoto in cui mettere le variabili che mi interessano
struttura = {}
struttura = programs['FILLER'].tags[PLCProdCycleVAR].value

# le chiavi sono i nomi del livello figlio della struttura
nomi_cicli = struttura.keys()


#### FILE CON I NOMI DEI CICLI
with open(fileCicliProd,'w',encoding='utf-16-le') as f:
    for n in nomi_cicli:
        f.write(n + '\n')

#### FILE CON LE TAGS LIVELLO CONTROLLORE
#stampa lista tag a livello controllore
with open(fileControllerTags,'w',encoding='utf-16-le') as f:
    for tag in tag_names:
        f.write(tag + '\n')



# creo il fiel IOMESSAGE
SignalExc('SignalFILFromBSI','ABFIL1')

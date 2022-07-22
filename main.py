import os
import sys
import l5x
import configparser
import utils
from os import listdir
from os.path import isfile, join

###########
## DATI ###
###########

file = 'P16164_PLC_20220609_00C.L5X'                # file L5X sorgente dal PLC
fileCicliProd = 'NomiCicliProd.txt'
fileControllerTags = 'ControllerTags.txt'
fileIOMESSAGE_Pre = 'IOMESSAGES_PLXXXX.ENG'
PLCProdCycleVAR = 'D40_00'
Sep = '..'                                          # separatore per parti della stringa IOMESSAGE
IntouchEncoding = 'utf-16-le'                       # codifica della maggior parte dei file ini 

###########################################################


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

def MergeFiles(dir,mac):
    """Unisce i file dei segnali

    Args:
        dir (str): Directory da cui leggere i file singoli
        mac (str): Codice Macchina (ES: BSI)
    """
    # ricavo la lista dei file nella cartella
    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    
    coppie = filter(lambda f: mac in f,files) # in list(coppie) ho la coppia FromTo
        
    #print (list(coppie))

    # scrivo un file solo
    with open('OUIT_'+ mac +'.ENG','w', encoding=IntouchEncoding) as outfile:
        for c in list(coppie):
            # Open each file in read mode
                with open(os.getcwd() +'\OUT\\' + c,encoding=IntouchEncoding) as infile:
                    outfile.write(infile.read())

def SignalExc(NomeSegnale,AccessName,Mac,OutDirFile):
    """Stampa su File un gruppo di segnali di scambio

    Args:
        NomeSegnale (str): nome della struttura del segnale di scambio (ES: SignalFILFromBSI)
        AccessName (str): access name del plc da cui proviene la struttura
        Mac (str): Nome Macchina (es: BSI)
    """
    startPos = 2 #posizione iniziale dell'incrementale per SXxx e DXxx

    # ricavo la prima parte (SX o DX in base al nome del segnale FROM or TO)
    FromTo = NomeSegnale[9:11] # puo essere Fr o To
    match FromTo.lower():
        case 'fr':
            FirstCol = 'SX'
            FromTo = 'From' #poi viene usato nel nome File
        case 'to':
            FirstCol = 'DX'
            FromTo = 'To'   #poi viene usato nel nome File

    # cancello il file di output se esiste
    if os.path.exists(OutDirFile + fileIOMESSAGE_Pre + '_' + FromTo + Mac):
        os.remove(OutDirFile + fileIOMESSAGE_Pre + '_' + FromTo + Mac)

    scambio = {}
    PRE = ''

    # scambio è un dizionario le cui chiavi rappresentano i nomi dei segnali di scambio
    try: 
        scambio = ctl_tags[NomeSegnale].value
    except KeyError:   # interecetto l'assenza del sengnale nel PLCs
        print('INFO> ' + NomeSegnale + ' NOT PRESENT')

  
    #le chiavi rappresentano i campi dei segnali di scambio
    # for s in scambio.keys():
    #     print(s)
    comment = [] # bisogna ricavarlo dalle chiavi
    lev2str = [] # coverto poi l'oggetto in stringa (lista di char)
    n = startPos        # incrementale della prima colonna S01, SX02, ecc

    # scorro la struttura per ricavare tutti i dati dei segnali di scambio
    for s in scambio.keys():
        lev2 = ctl_tags[NomeSegnale][s] # oggetto EnumDict che contiene l'informazione sul tipo di dato
        lev2str = str(lev2) 
        type = lev2str[9:13]            # recupero il TIPO di dato con un mid dell'oggetto
       # print (lev2str[9:13], ':',s) 

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
            case _:         #default
                PRE = 'D'

        
        #separo in blocchi da 28
        if int(n) > 28:
            n = startPos

        # aggiungo lo zero all'incrementale se sono entro la decina 
        if n in range(1,10):
            n = '0' + str(n)

        # gestione nome sezione
        Header = ''
        if FirstCol == 'SX' and int(n) == startPos:
            Header = '\n' + '['+ Mac + ']'
        else:
            Header = ''

        # gestione prima riga di SX o DX
        if FirstCol == 'DX' and int(n) == startPos:
            Nome01 = '\n' + FirstCol +'01 = B..FILLER\n'
        else:
            Nome01 = '\n' + FirstCol +'01 = B..\n'

        #compongo l'uscita
        if int(n) == startPos:
            #Out = Header + FirstCol +'01 = B..\n'+ FirstCol + str(n) + " = " + PRE + Sep + AccessName +'.' + NomeSegnale + '.' + s + Sep + comment
            Out = Header + Nome01 + FirstCol + str(n) + " = " + PRE + Sep + AccessName +'.' + NomeSegnale + '.' + s + Sep + comment
        else:
            Out =  FirstCol + str(n) + " = " + PRE + Sep + AccessName +'.' + NomeSegnale + '.' + s + Sep + comment
        
        OutFileUTF16(os.getcwd() +'\OUT\\' +fileIOMESSAGE_Pre + '_' + FromTo + Mac,Out) # stampo il file
        n = int(n) + 1

   
##########
## MAIN ##
##########

#################################
##### PREPARAZIONE STRUTTURE ####
#################################

# carico il file L5X in memoria
prj = l5x.Project(file)

# ctl_tags è un ElementDict contenente le tag a livello controllore
ctl_tags = prj.controller.tags
# lista tag name livello controllore
tag_names = ctl_tags.names

# ELEMENTDICT con i programmi
programs = prj.programs

# lista nomi programmi
programs_names = programs.names

#################################


###########################################
#  ricavo la lista della macchine esterne #
###########################################

config = configparser.ConfigParser(strict= False)
fileCFG_PAGE = 'CFG_PAGE.INI'

config.read_file(open(fileCFG_PAGE,encoding='utf-8')) 

lista_sezioni = config.sections()               # lista con le sezioni
lista_item = config.items(lista_sezioni[4])     # lista della prima sezione CFG_IOMAC
lista_itemDICT = dict(lista_item)               

lista_macc = []     # lista delle macchine 

# leggo la lista delle macchine di cui leggere i segnali di scambio
for k in range(1,len(lista_itemDICT.keys())):
    if (lista_itemDICT.get(str(k)) is not None):      # salto eventuali buchi
        lista_macc.append(lista_itemDICT.get(str(k))) # prendo le prime tre lettere che indicano la macchina 
#print(lista_macc)


# TO DO: trovare il modo di leggere ACCESSNAME
#      : Unire a modo le coppie di files
#      : 

# creo la cartella temporanea di uscita se non esiste
OutDir = os.getcwd() +'\OUT\\'
if not os.path.exists (OutDir):
    os.makedirs(OutDir)

# creo i file IOMESSAGE singoli
for a in lista_macc:
    SignalExc('SignalFILFrom'+a,'ABFIL1',a,OutDir)
    SignalExc('SignalFILTo'+a,'ABFIL1',a,OutDir)

# unisco i file corrispondenti
for m in lista_macc:
    MergeFiles(OutDir,m)

# MergeFiles(OutDir,'BHE')
sys.exit(0)




#######################################
######## PREPARAZIONE PER ALTRO  ######
#######################################


# definisco un dizionario vuoto in cui mettere le variabili che mi interessano
struttura = {}
struttura = programs['FILLER'].tags[PLCProdCycleVAR].value

# le chiavi sono i nomi del livello figlio della struttura
nomi_cicli = struttura.keys()


#### FILE CON I NOMI DEI CICLI
with open(fileCicliProd,'w',encoding=IntouchEncoding) as f:
    for n in nomi_cicli:
        f.write(n + '\n')

#### FILE CON LE TAGS LIVELLO CONTROLLORE
#stampa lista tag a livello controllore
with open(fileControllerTags,'w',encoding=IntouchEncoding) as f:
    for tag in tag_names:
        f.write(tag + '\n')



  #### PROVE ####
    
    #va in ordine alfabetico
    # for i in range(0, len(ctl_tags.names)):
    #     if ctl_tags.names[i] == 'SignalFILFromBSI':
    #         print(ctl_tags.names[i])
    #         print(ctl_tags[ctl_tags.names[i]].names)
    #         print(ctl_tags[ctl_tags.names[i]].value)
    #         print(ctl_tags[ctl_tags.names[i]].description)

    # sys.exit(0)
    ######




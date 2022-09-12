#from ast import Str
from argparse import HelpFormatter
import cmd
import os
import sys
import l5x
import configparser
import utils
import HelpMNG
from os import listdir
from os.path import isfile, join

CFGFile = os.getcwd() + '\Configuration.ini'
fileHELP = 'help.ini'
ResourceFolder = os.getcwd() + '\\RES\\'

###########
## DATI ###
###########
# LETTURA FILE CONFIGURAZIONE 
CFGParser = configparser.ConfigParser(strict= False)
CFGParser.read_file(open(CFGFile,encoding='utf-8')) 
CFGlista_sezioni = CFGParser.sections()
CFGlista = CFGParser.items(CFGlista_sezioni[0])    
CFGlistaDICT = dict(CFGlista)    # metto tutto dentro un dizionario per comodita di accesso
#print(CFGlista)

# DATI ESTRATTI DAL FILE DI CONFIGURAZIONE
file = CFGlistaDICT['file']                               # IN: file L5X sorgente dal PLC
fileCFG_PAGE = CFGlistaDICT['filecfgpage']                # IN: file contenente lista macchine esterne
Fx_Cx = CFGlistaDICT['fx_cx']                             # IN: tipo di macchina
#PLCProdCycleVAR = eval(CFGlistaDICT['plcprodcyclevar'])  # Area Memoria PLC per cicli Produzione
#PLCSanCycleVar = eval(CFGlistaDICT['plcsancyclevar'])    # Area Memoria PLC per cicli Sanificazione
PLCProdCycleVAR = 'D40_00'
PLCSanCycleVar = 'D60_00'

CFG_IOMAC = int(CFGlistaDICT['cfg_iomac'])               # Numero sezione CFG_IOMAC 


fileCicliProd = 'NomiCicliProd.txt'                 # OUT
fileCicliSan = 'NomiCicliSan.txt'           
fileControllerTags = 'ControllerTags.txt'
fileIOMESSAGE_Pre = 'IOMESSAGES_PLXXXX.ENG'         # OUT:
fileIOMESSAGE = 'IOMESSAGES_PLXXXX'                 # OUT:

Sep = '..'                                          # separatore per parti della stringa IOMESSAGE
IntouchEncoding = 'utf-16-le'                       # codifica della maggior parte dei file ini 
NomeCartellaOUT = 'IO_OUT'                             # cartella appoggio per coppie di file IOMESSAGE in cwd
NomeCartellaFINALE = 'IO_OUTFINALE'                    # cartella con risultato finale in cwd per IOMESSAGE

###########################################################


def MergeFiles(dir,mac,outdir):
    """Unisce i file dei segnali

    Args:
        dir (str): Directory da cui leggere i file singoli
        mac (str): Codice Macchina (ES: BSI)
        outdir (str): destinazione file uniti
    """
    # ricavo la lista dei file nella cartella
    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    
    # in list(coppie) ho la coppia FromTo
    coppie = filter(lambda f: mac in f,files) 

    # scrivo un file solo per ogni categoria
    with open(outdir + fileIOMESSAGE + '_'+ mac +'.ENG','w', encoding=IntouchEncoding) as outfile: # apro il file di uscita
        for c in list(coppie):
            # Apro ogni coppia di file
                with open(dir + c,encoding=IntouchEncoding) as infile:
                    # leggo i file e li combino in un file per ogni macchina
                    outfile.write(infile.read())


def SignalExc(NomeSegnale,AccessName,Mac,OutDirFile):
    """Stampa su File un gruppo di segnali di scambio
       per ogni gruppo (es: BSI) stampa due files From e To

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
        
        utils.OutFileUTF16(os.getcwd() +'\\'+ NomeCartellaOUT +'\\'  +fileIOMESSAGE_Pre + '_' + FromTo + Mac,Out) # stampo il file
        n = int(n) + 1



def ListaCicli (StructCicli,FileOutput,NomePOSPlc):
    """Crea un file con i nomi dei cicli presi dal plc

    Args:
        StructCicli (str): nome struttura cicli (es: D40_00)
        FileOutput (str): Nome file uscita
    """
    # definisco un dizionario vuoto in cui mettere le variabili che mi interessano
    cicli = {}
    cicli = programs[NomePOSPlc].tags[StructCicli].value
   
    # le chiavi sono i nomi del livello figlio della struttura
    nomi_cicli = cicli.keys()

    
    #### FILE CON I NOMI DEI CICLI
    with open(FileOutput,'w',encoding=IntouchEncoding) as f:
        for n in nomi_cicli:
            if isinstance(cicli[n],dict):  # solo le strutture sono cicli!!
                f.write(n + '\n')
    print ('INFO -> Cycle List generation to file ' + FileOutput + '\n')
   




def CycleDesc(NomePrg,NomeStruct,NomeCiclo,NomeStructPhMsg,MacCyc,OutFile):
    """Stampa su file i tre blocco di commenti per un ciclo

    Args:
        NomePrg (str): Nome del programma PLC in cui riesiede il ciclo (ES: FILLER)
        NomeStruct (str): Nome della struttura PLC del ciclo (ES: D40_00)
        NomeCiclo (str): ES: Drainage
        NomeStructPhMsg (str): Nome struttura PhaseMsgInput (ed: D40_01)
        OutFile (str): File di uscita
    """
    ###########
    ## PHASE ##
    ###########
    PhaseDesc = programs[NomePrg].tags[NomeStruct][NomeCiclo]['Phase'].description
    # rimuovo header dal commento
    PhaseDesc = PhaseDesc.replace('## PHASE ##','') # tolgo ## PHASE ##
    PhaseDesc = PhaseDesc.strip('\n')
    # aggiungo =V;
    PhaseDesc = PhaseDesc.replace('=','= V;')

    ############
    # CYCLEMSG #
    ############
    CycleMsgDesc = ''
    for a in range(0,3):
        for i in range(0,31):
            if programs[NomePrg].tags[NomeStruct][NomeCiclo]['CycleMsgInput'][a][i].description is not None:
                nMSG = i+1 # il numero del messaggio è il bit + 1 nel PLC
                CycleMsgDescA = programs[NomePrg].tags[NomeStruct][NomeCiclo]['CycleMsgInput'][a][i].description + '\n'
                try:
                    # nel caso nei commenti le frasi siano separate da newline
                    CycleMsgDescSplit = CycleMsgDescA.split('\n')
                    msg = CycleMsgDescSplit[2].strip('\n') + '\n'
                except:
                    print('EXCEPT CycleMSG per ' + NomeCiclo)
                        # nel caso nei commenti le frasi abbiamo almeno message
                    try:
                        # casefold rende tutto minuscolo in modo piu aggressivo rispetto a lower
                        id = CycleMsgDescA.casefold().index('message') + len('message') + 3 # cerco MESSAGE
                        msg = utils.mid(CycleMsgDescA,id,len(CycleMsgDescA))
                    except:
                        print('EXCEPT ANNIDATO CycleMSG per ' + NomeCiclo)
                        msg = CycleMsgDescA #nel caso peggiore il messaggio è tutto il commento così come lo trovo
                #         print('INFO-> CYCLEMSG di '+ NomeCiclo +' Manca Message nei commenti PLC')
                #         id = 0
                        
                # else:
                #     print('INFO-> Else attivo per ' + NomeCiclo)
                    #msg = CycleMsgDescA #nel caso peggiore il messaggio è tutto il commento così come lo trovo
                CycleMsgDesc = CycleMsgDesc + str(nMSG) + '= V; - ' + msg.strip('\n') + ('\n')
             
    ############
    # PHASEMSG #
    ############
    PhaseMsgDesc = ''
    if NomeStructPhMsg is not None: # NON TUTTI I CICLI HANNO PHASE MESSAGE
        for a in range(0,2): 
            for i in range(0,31):                    
                if programs[NomePrg].tags[NomeStructPhMsg]['PhaseMessageInput'][a][i].description is not None:
                    nMSG = i+1
                    PhaseMsgDescA = programs[NomePrg].tags[NomeStructPhMsg]['PhaseMessageInput'][a][i].description + '\n'
                    try:
                        # nel caso nei commenti le frasi siano separate da newline
                        PhaseMsgDescSplit =  PhaseMsgDescA.split('\n')
                        msg = PhaseMsgDescSplit[2].strip('\n') + '\n'
                    except:
                        print('EXCEPT PhaseMsg per ' + NomeCiclo)
                        try:
                            # casefold rende tutto minuscolo in modo piu aggressivo rispetto a lower
                            id = PhaseMsgDescA.casefold().index('message') + len('message') + 3 # cerco MESSAGE
                            msg = utils.mid(PhaseMsgDescA,id,len(PhaseMsgDescA))
                        except:
                            print('EXCEPT ANNIDATO PhaseMSG per ' + NomeCiclo)
                            msg = PhaseMsgDescA #nel caso peggiore il messaggio è tutto il commento così come lo trovo

                    PhaseMsgDesc = PhaseMsgDesc + str(nMSG) + '= V;' + msg.strip('\n') + ('\n')
    else:
        PhaseMsgDesc = ''
            
    # pubblico su file
    with open(OutFile,'w',encoding=IntouchEncoding) as f:
        f.write('[CYCL_'+ MacCyc +'_'+ NomeCiclo +'_Phase]=Program:'+ NomePrg +'.'+ NomeStruct +'.'+ NomeCiclo +'.Phase\n') # Header
        f.write(PhaseDesc)
        f.write('\n')
        f.write('\n')
        f.write('[CYCL_'+ MacCyc +'_'+ NomeCiclo +'_MSG]=Program:'+ NomePrg +'.'+ NomeStruct +'.'+ NomeCiclo +'.CycleMsg\n') # Header
        f.write(CycleMsgDesc)
        f.write('\n')
        f.write('\n')
        f.write('[CYCL_'+ MacCyc +'_'+ NomeCiclo +'_PhaseMSG]=Program:'+ NomePrg +'.'+ NomeStruct +'.'+ NomeCiclo +'.PhaseMessage\n') # Header
        f.write(PhaseMsgDesc)
        f.write('\n')
        f.write('\n')




##########
## MAIN ##
##########

#  GESTIONE HELP #
HelpFile = ResourceFolder + fileHELP
#se non viene passato alcun argomento, la lista ha un solo elemento che è il percorso completo del sorgente
if len(sys.argv) == 1:
    HelpMNG.GetHelp(HelpFile,None)
elif utils.left(sys.argv[1],4).lower() == 'help':
    try:
        HelpMNG.GetHelp(HelpFile, sys.argv[2])  # si prevede di chiamare con help [nomeswitch]
    except:
        print('Switch not supplied')
else:
    
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

    ####################
    # LISTA NOMI CICLI #
    ####################
   
    if sys.argv[1].strip() == '--cycleslist':
        ListaCicli(PLCProdCycleVAR,fileCicliProd,'FILLER') # Cicli Prod
        ListaCicli(PLCSanCycleVar,fileCicliSan,'FILLER')   # Cicli San
   
    ##########
    # PHASES #
    ##########
    # SANIFICAZIONE #
    # with open (os.getcwd() + '\\' + fileCicliSan,'r',encoding=IntouchEncoding) as fcs:
    #     SanCycles = fcs.readlines()
    #     for sanc in SanCycles:
    #         CycleDesc('FILLER','D60_00',sanc.strip('\n'),20,'D60_01','FIL',os.getcwd() + '\Phase_'+ sanc.strip('\n') +'_TEST.ENG')
    if sys.argv[1].strip() == '--cycles':
        # SANIFICAZIONE #
        CycleDesc('FILLER','D60_00','Drainage','D60_01','FIL',os.getcwd() + '\Phase_Drainage_TEST.ENG')
        CycleDesc('FILLER','D60_00','COP','D60_02','FIL',os.getcwd() + '\Phase_COP_TEST.ENG')
        CycleDesc('FILLER','D60_00','DBLoad','D60_02','FIL',os.getcwd() + '\Phase_DBLoad_TEST.ENG')
        CycleDesc('FILLER','D60_00','CIP','D60_04','FIL',os.getcwd() + '\Phase_CIP_TEST.ENG')
        CycleDesc('FILLER','D60_00','SteamFilter','D60_05','FIL',os.getcwd() + '\Phase_SteamFilter_TEST.ENG')
        CycleDesc('FILLER','D60_00','SipFiller','D60_06_'+Fx_Cx,'FIL',os.getcwd() + '\Phase_SipFiller_TEST.ENG')
        CycleDesc('FILLER','D60_00','SteamBarrier','D60_09','FIL',os.getcwd() + '\Phase_SteamBarrier_TEST.ENG')
        CycleDesc('FILLER','D60_00','PAAExternal','D60_07','FIL',os.getcwd() + '\Phase_PAAExternal_TEST.ENG')
        CycleDesc('FILLER','D60_00','HEPA1','D60_08_SV1','FIL',os.getcwd() + '\Phase_HEPA1_TEST.ENG')       #occhio che qui c'è SV1!!
        CycleDesc('FILLER','D60_00','DBUnLoad',None,'FIL',os.getcwd() + '\Phase_DBUnLoad_TEST.ENG')
        CycleDesc('FILLER','D60_00','DBLoad_PSD',None,'FIL',os.getcwd() + '\Phase_DBLoad_PSD_TEST.ENG')
        CycleDesc('FILLER','D60_00','Rinse_PSD',None,'FIL',os.getcwd() + '\Phase_Rinse_PSD_TEST.ENG')
        CycleDesc('FILLER','D60_00','CIP_PSD',None,'FIL',os.getcwd() + '\Phase_CIP_PSD_TEST.ENG')
        CycleDesc('FILLER','D60_00','SIP_PSD',None,'FIL',os.getcwd() + '\Phase_SIP_PSD_TEST.ENG')
        CycleDesc('FILLER','D60_00','DBUnLoad_PSD',None,'FIL',os.getcwd() + '\Phase_DBUnLoad_PSD_TEST.ENG')
        CycleDesc('FILLER','D60_00','BellowsIntegrity_PSD',None,'FIL',os.getcwd() + '\Phase_BellowsIntegrity_PSD_TEST.ENG')
        CycleDesc('FILLER','D60_00','SteamBarrier_PSD',None,'FIL',os.getcwd() + '\Phase_BellowsIntegrity_SteamBarrier_PSD.ENG')
        CycleDesc('FILLER','D60_00','CXJackTest',None,'FIL',os.getcwd() + '\Phase_CXJackTest.ENG')
        # PRODUZIONE #
        CycleDesc('FILLER','D40_00','TankStartUp','D40_02','FIL',os.getcwd() + '\Phase_TankStartup_TEST.ENG')
    #sys.exit(0)

    #### PROVE ####
        
        #va in ordine alfabetico
    # for i in range(0, len(ctl_tags.names)):
    #     if ctl_tags.names[i] == 'D60_00':
    #         print(ctl_tags.names[i])
    #         print(ctl_tags[ctl_tags.names[i]].names)
    #         print(ctl_tags[ctl_tags.names[i]].value)
    #         print(ctl_tags[ctl_tags.names[i]].description)

    ###############
    # IO MESSAGES #
    ###############
    if sys.argv[1].strip() == '--iomsg':
        # TO DO: trovare il modo di leggere ACCESSNAME
        #      : Unire a modo le coppie di files
        #      : 

        #  ricavo la lista della macchine esterne #
        CFGPAGE = configparser.ConfigParser(strict= False)
        CFGPAGE.read_file(open(fileCFG_PAGE,encoding='utf-8')) 
        lista_sezioni = CFGPAGE.sections()               # lista con le sezioni
        lista_item = CFGPAGE.items(lista_sezioni[CFG_IOMAC])     # lista della prima sezione CFG_IOMAC
        lista_itemDICT = dict(lista_item)               
        lista_macc = []     # lista delle macchine 
        
        # leggo la lista delle macchine di cui leggere i segnali di scambio
        for k in range(1,len(lista_itemDICT.keys())):
            if (lista_itemDICT.get(str(k)) is not None):      # salto eventuali buchi
                lista_macc.append(lista_itemDICT.get(str(k))) # prendo le prime tre lettere che indicano la macchina 

        
        # creo la cartella temporanea di uscita se non esiste
        OutDir = os.getcwd() +'\\'+ NomeCartellaOUT +'\\'
        if not os.path.exists (OutDir):
            os.makedirs(OutDir)
        OutDirFIN = os.getcwd() +'\\'+ NomeCartellaFINALE +'\\'
        if not os.path.exists (OutDirFIN):
            os.makedirs(OutDirFIN)
        
        # creo i file IOMESSAGE
        for a in lista_macc:
            SignalExc('SignalFILFrom'+a,'ABFIL1',a,OutDir)
            SignalExc('SignalFILTo'+a,'ABFIL1',a,OutDir)
        
        # unisco i file corrispondenti
        for m in lista_macc:
            MergeFiles(OutDir,m,OutDirFIN)
        

        print('Files generated in : ' + OutDirFIN ) # avviso in quale cartella ho generato i file uniti



    ####################
    # TAG CONTROLLORE  #
    ####################

    #stampa lista tag a livello controllore
# with open(fileControllerTags,'w',encoding=IntouchEncoding) as f:
#     for tag in tag_names:
#         f.write(tag + '\n')








import os
import utils
from os import listdir
from os.path import isfile, join
import cfg
from termcolor import colored
import re


def MergeFiles(dir,mac,outdir):
    """Unisce i file dei segnali di SCAMBIO

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
    with open(outdir + cfg.fileIOMESSAGE + '_'+ mac +'.ENG','w', encoding=cfg.IntouchEncoding) as outfile: # apro il file di uscita
        for c in list(coppie):
            # Apro ogni coppia di file
                with open(dir + c,encoding=cfg.IntouchEncoding) as infile:
                    # leggo i file e li combino in un file per ogni macchina
                    outfile.write(infile.read())


def SignalExc(NomeSegnale,AccessName,Mac,OutDirFile,ctl_tags):
    """Stampa su File un gruppo di segnali di scambio
       per ogni gruppo (es: BSI) stampa due files From e To

    Args:
        NomeSegnale (str): nome della struttura del segnale di scambio (ES: SignalFILFromBSI)
        AccessName (str): access name del plc da cui proviene la struttura
        Mac (str): Nome Macchina (es: BSI)
        OutDirFile (str): Nome cartella di Output per i files
        ctl_tags (ElementDict): contenitore tags livello controllore
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
    if os.path.exists(OutDirFile + cfg.fileIOMESSAGE_Pre + '_' + FromTo + Mac):
        os.remove(OutDirFile + cfg.fileIOMESSAGE_Pre + '_' + FromTo + Mac)

    scambio = {}
    PRE = ''

    # scambio è un dizionario le cui chiavi rappresentano i nomi dei segnali di scambio
    try: 
        scambio = ctl_tags[NomeSegnale].value
    except KeyError:   # interecetto l'assenza del sengnale nel PLCs
        print(colored('INFO > ',cfg.ColorInfo) + NomeSegnale + ' NOT PRESENT')

  
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
        
        # # \\TEST per scrivere un commento piu significativo
        # sAppo = ''
        # for c in comment:
        #     if c.isupper() == True:
        #         idC = comment.index(c)  # indice della maiuscola
        #         sAppo = s.replace(c,)

        
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
            Out = Header + Nome01 + FirstCol + str(n) + " = " + PRE + cfg.Sep + AccessName +'.' + NomeSegnale + '.' + s + cfg.Sep + comment
        else:
            Out =  FirstCol + str(n) + " = " + PRE + cfg.Sep + AccessName +'.' + NomeSegnale + '.' + s + cfg.Sep + comment
        
        utils.OutFileUTF16(os.getcwd() + cfg.bars + cfg.NomeCartellaOUT + cfg.bars  + cfg.fileIOMESSAGE_Pre + '_' + FromTo + Mac,Out) # stampo il file
        n = int(n) + 1



def ListaCicli (StructCicli,FileOutput,NomePOSPlc,programs):
    """Crea un file con i nomi dei cicli presi dal plc

    Args:
        StructCicli (str): nome struttura cicli (es: D40_00)
        FileOutput (str): Nome file uscita
        NomePOSPlc (str): Nome del POS del plc (es: FILLER)
        programs (ElementDict): dizionari con l'elenco dei programmi del POS
    """
    # definisco un dizionario vuoto in cui mettere le variabili che mi interessano
    cicli = {}
    cicli = programs[NomePOSPlc].tags[StructCicli].value
   
    # le chiavi sono i nomi del livello figlio della struttura
    nomi_cicli = cicli.keys()

    
    #### FILE CON I NOMI DEI CICLI
    with open(FileOutput,'w',encoding=cfg.IntouchEncoding) as f:
        for n in nomi_cicli:
            if isinstance(cicli[n],dict):  # solo se le strutture sono cicli!!
                f.write(n + '\n')
    #print ('INFO -> Cycle List generation to file ' + FileOutput + '\n')
    print (colored('INFO > ',cfg.ColorInfo)+' Cycle List generation to file ' + FileOutput + '\n')





def CycleDesc(NomePrg,NomeStruct,NomeCiclo,NomeStructPhMsg,MacCyc,OutFile,programs,HmiVer=0):
    """Stampa su file i tre blocchi di commenti per un ciclo (PHASES.eng)

    Args:
        NomePrg (str): Nome del programma PLC in cui riesiede il ciclo (ES: FILLER)
        NomeStruct (str): Nome della struttura PLC del ciclo (ES: D40_00)
        NomeCiclo (str): ES: Drainage
        NomeStructPhMsg (str): Nome struttura PhaseMsgInput (ed: D40_01)
        MacCyc (str): nome macchina per header sezione (Es: FIL )
        OutFile (str): File di uscita
        programs (ElementDict): dizionari con l'elenco dei programmi del POS
        HmiVer (int): 0- mette la 'V;'
    """
    # folder di uscita viene creato se non esiste
    OutDir = os.getcwd() + cfg.bars + cfg.NomeCartPhasesOUT + cfg.bars
    if not os.path.exists (OutDir):
        os.makedirs(OutDir)
    
      # svuoto la cartella da eventuali files precedenti
    #utils.DeleteFilesInFolder(OutDir)


    ###########
    ## PHASE ##
    ###########
    PhaseDesc = programs[NomePrg].tags[NomeStruct][NomeCiclo]['Phase'].description # description indica il commento della tag

    if PhaseDesc is not None: # potrebbe mancare il commento nella tag a PLC
        # rimuovo header dal commento
        #PhaseDesc = PhaseDesc.replace('## PHASE ##','') # tolgo ## PHASE ##
        PhaseDesc = re.sub(r'(?:#+)(.*?)(?:#+)','',PhaseDesc) # tolgo qualsiasi cosa tra n# e n# (## PHASE ##)
        PhaseDesc = PhaseDesc.strip('\n')
        PhaseDesc = '0='+ '\n' + PhaseDesc # aggiungo lo zero alla prima riga
        PhaseDesc = re.sub(r'(\n)(?:\s+)','\n',PhaseDesc) # tolgo eventuali spazi all'inizio di ogni entry

        if HmiVer == 0:
            # aggiungo '=V;' (HMI blu)
            PhaseDesc = PhaseDesc.replace('=','= V;')
        else:               #(HMI Grigia)
            pass
            
    else:
        PhaseDesc = '!! NO_COMMENTS_IN_PLC TAGS !!' # se mancano i commenti nella tag a plc lo segnalo nel file

    ############
    # CYCLEMSG #
    ############

    CycleMsgDesc = ''

    # Ricavo la dimensione del CycleMsgInput
    CMIArrSize = programs[NomePrg].tags[NomeStruct][NomeCiclo]['CycleMsgInput'].shape[0]

    for a in range(0,CMIArrSize): # scorro .CycleMsgInput è un array 
        for i in range(0,31): # scorro ogni DINT di .CycleMsgInput

            if programs[NomePrg].tags[NomeStruct][NomeCiclo]['CycleMsgInput'][a][i].description is not None:
                nMSG = i+1 # il numero del messaggio è il bit + 1 nel PLC
                CycleMsgDescA = programs[NomePrg].tags[NomeStruct][NomeCiclo]['CycleMsgInput'][a][i].description + '\n'
                
                try:
                    # nel caso nei commenti le frasi siano separate da newline
                    CycleMsgDescSplit = CycleMsgDescA.split('\n')
                    msg = CycleMsgDescSplit[2].strip('\n') + '\n'
                except:
                        # nel caso nei commenti le frasi abbiamo almeno un message
                    try:
                        # casefold rende tutto minuscolo in modo piu aggressivo rispetto a lower
                        id = CycleMsgDescA.casefold().index('message') + len('message') + 3 # cerco MESSAGE
                        msg = utils.mid(CycleMsgDescA,id,len(CycleMsgDescA))
                    except:
                        # print('INFO-> EXCEPT ANNIDATO CycleMSG per ' + NomeCiclo)
                        msg = CycleMsgDescA #nel caso peggiore il messaggio è tutto il commento così come lo trovo
                
                # ALLA FINE    
                if HmiVer == 0:  #(HMI BLU)
                    CycleMsgDesc = CycleMsgDesc + str(nMSG) + '= V; - ' + msg.strip('\n') + ('\n')
                else:               #(HMI GRIGIA)
                    CycleMsgDesc = CycleMsgDesc + str(nMSG) + '= - ' + msg.strip('\n') + ('\n')

    # se non ho trovato neanche un commento nelle variabili lo segnalo nel file
    if CycleMsgDesc == '':
        CycleMsgDesc = '! NO COMMENTS IN PLC TAGS !'

    ############
    # PHASEMSG #
    ############
    PhaseMsgDesc = ''

    if NomeStructPhMsg is not None: # NON TUTTI I CICLI HANNO PHASE MESSAGE
        try: # potrebbe non essere presente nel software PLC in esame il PhaseMessageInput

            # Ricavo la dimensione dell'array PhaseMessageInput
            PMIArrSize = programs[NomePrg].tags[NomeStructPhMsg]['PhaseMessageInput'].shape[0]
            # for a in range(0,2): 

            for a in range(0,PMIArrSize): #scorro ogni array
                for i in range(0,31):   #scorro ogni bit dell array
                    try: # nel caso non ci sia la variabile di struttura Phase Msg
                        description = programs[NomePrg].tags[NomeStructPhMsg]['PhaseMessageInput'][a][i].description               
                        #if programs[NomePrg].tags[NomeStructPhMsg]['PhaseMessageInput'][a][i].description is not None:
                        if description is not None:
                            nMSG = i+1
                            PhaseMsgDescA = programs[NomePrg].tags[NomeStructPhMsg]['PhaseMessageInput'][a][i].description + '\n'
                            try:
                                # nel caso nei commenti le frasi siano separate da newline
                                PhaseMsgDescSplit =  PhaseMsgDescA.split('\n')
                                msg = PhaseMsgDescSplit[2].strip('\n') + '\n'
                            except:
                                #print('EXCEPT PhaseMsg per ' + NomeCiclo)
                                try:
                                    # casefold rende tutto minuscolo in modo piu aggressivo rispetto a lower
                                    id = PhaseMsgDescA.casefold().index('message') + len('message') + 3 # cerco MESSAGE
                                    msg = utils.mid(PhaseMsgDescA,id,len(PhaseMsgDescA))
                                except:
                                    #print('EXCEPT ANNIDATO PhaseMSG per ' + NomeCiclo)
                                    msg = PhaseMsgDescA #nel caso peggiore il messaggio è tutto il commento così come lo trovo
                            if HmiVer == 0:  #(HMI BLU):
                                PhaseMsgDesc = PhaseMsgDesc + str(nMSG) + '= V;' + msg.strip('\n') + ('\n')
                            else:               #(HMI GRIGIA)
                                PhaseMsgDesc = PhaseMsgDesc + str(nMSG) + '= ' + msg.strip('\n') + ('\n')
                    except(KeyError):
                        pass
        except(KeyError):
            pass
    else:
        PhaseMsgDesc = ''

    # se il file esiste lo cancello        
    try:
        os.remove(OutDir + OutFile)
    except OSError:
        pass
    
    # pubblico su file
    with open(OutDir + OutFile,'w',encoding=cfg.IntouchEncoding) as f:
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

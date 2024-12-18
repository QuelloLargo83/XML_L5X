from asyncio.windows_events import NULL
import os
from tkinter import N
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


def SignalExc(NomeSegnale,AccessName,Mac,OutDirFile,ctl_tags, DIR = '-1'):
    """Stampa su File un gruppo di segnali di scambio
       per ogni gruppo (es: BSI) stampa due files From e To

    Args:
        NomeSegnale (str): nome della struttura del segnale di scambio (ES: SignalFILFromBSI)
        AccessName (str): access name del plc da cui proviene la struttura
        Mac (str): Nome Macchina (es: BSI)
        OutDirFile (str): Nome cartella di Output per i files
        ctl_tags (ElementDict): contenitore tags livello controllore
        DIR (optional): indicare SX o DX se non si puo ricavare questa info dal nome segnale
    """

    startPos = 2 #posizione iniziale dell'incrementale per SXxx e DXxx
    MaxRow = int(cfg.INIREAD('sigmaxrow'))

    # se il parametro DIR non viene passato rimane a -1
    if DIR == '-1':  
        # ricavo la prima parte (SX o DX in base al nome del segnale FROM or TO)
        FromTo = NomeSegnale[9:11] # puo essere Fr o To
        match FromTo.lower():
            case 'fr':
                FirstCol = 'SX'
                FromTo = 'From' #poi viene usato nel nome File
            case 'to':
                FirstCol = 'DX'
                FromTo = 'To'   #poi viene usato nel nome File
    else:
        # nei casi in cui non è possibile ricavare l'info dal Nome del segnale
        FirstCol = DIR
        match DIR:
            case 'SX':
                FromTo = 'From'
            case 'DX':
                FromTo = 'To'

    # cancello il file di output se esiste
    if os.path.exists(OutDirFile + cfg.fileIOMESSAGE_Pre + '_' + FromTo + Mac):
        os.remove(OutDirFile + cfg.fileIOMESSAGE_Pre + '_' + FromTo + Mac)

    scambio = {}
    PRE = ''
    splitted = False

    # scambio è un dizionario le cui chiavi rappresentano i nomi dei segnali di scambio
    try: 
        posPunto = NomeSegnale.find('.')
        if posPunto != -1:         # se ce un punto (esempio SignalFILToPRO.UTH) devo splittare 
            splitted = True        # indico che la tag nomesegnale ha un punto in mezzo
            LS = utils.left(NomeSegnale,posPunto)
            RS = utils.mid(NomeSegnale,posPunto+1,len(NomeSegnale))
            scambio = ctl_tags[LS][RS].value
        else:
            scambio = ctl_tags[NomeSegnale].value
    # except KeyError:   # interecetto l'assenza del sengnale nel PLCs
    #     print(colored('INFO > ',cfg.ColorInfo) + NomeSegnale + ' NOT PRESENT')

  
        #le chiavi rappresentano i campi dei segnali di scambio
        comment = [] # bisogna ricavarlo dalle chiavi
        lev2str = [] # coverto poi l'oggetto in stringa (lista di char)
        n = startPos        # incrementale della prima colonna S01, SX02, ecc

        last = list(scambio.keys())[-1] #memorizzo l'ultimo elemento del gruppo di segnali

        # scorro la struttura per ricavare tutti i dati dei segnali di scambio
        for s in scambio.keys():
            if splitted == True:
                lev2 = ctl_tags[LS][RS][s]
            else:
                lev2 = ctl_tags[NomeSegnale][s] # oggetto EnumDict che contiene l'informazione sul tipo di dato
            
            lev2str = str(lev2) 
            type = lev2str[9:13]            # recupero il TIPO di dato con un mid dell'oggetto
        
            comment = s # rinomico in comment per chiarezza

            ##############################################################
            # ricavo commento separando il nome dove trovo una maiuscola #
            ##############################################################
            
            mem = [] # appoggio per le maiuscole

            for c in comment: # scorro ogni lettera di ogni commento
                
                if c in mem: continue # se ho gia visto questa lettera maiuscola vado avanti perche ho gia sistemato il commento

                if c.isupper() == True:   
    
                    lstIndex = utils.indices(comment,c) # lista delle posizioni in cui trova la lettera maiuscola (la stessa lettera puo essere in piu posizioni)
                    
                    for idC in lstIndex: # ci possono essere due lettere maiuscole uguali
                        
                        mem.append(comment[idC])
                        try:
                            if comment[idC-1].isupper() == True and comment[idC+1].isupper() == True :  # se anche la lettera precedente e consec sono maiuscole (es: PAA)
                                pass
                            else:
                                comment = ''.join((comment[:idC],' ', comment[idC:])) # aggiungo uno spazio dove trovo la maiuscola, aggiungendo anche uno spazio all'inizio
                                comment = comment.lstrip() # rimuovo lo spazio iniziale indesiderato
                        except(IndexError): # intercetto il fatto che la maiuscola sia alla fine del testo
                            pass
                                   
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
                case 'REAL':
                    PRE = 'A'
                case _:         #default
                    PRE = 'D'

            
            #separo in blocchi 
            if int(n) > MaxRow:
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

              ### TENTO DI INSERIRE ..[DIM]..[Kx]
            if PRE == 'A':
                K = 'K1' # lascio per ora la costante =1
                #print(colored(NomeSegnale,'yellow') + '.' + colored(s,'red'))
                if('flow' in s or 'Flow' in s):
                    Dim = 'FLWL'
                elif('speed' in s or 'Speed' in s):
                    Dim = 'SPDH'
                elif('weight' in s or 'Weight' in s):
                    Dim = 'SPDH..K1'
                elif('pressure' in s or 'Pressure' in s):
                    Dim = 'PRSM'
                elif('time' in s or 'Time' in s):
                    Dim = 'TIME'
                elif('level' in s or 'Level' in s):
                    Dim = 'LVLT'
                else:
                    Dim = 'NONE'
                
                comment = comment + cfg.Sep + Dim + cfg.Sep + K
            ###

            #compongo l'uscita
            if int(n) == startPos:
                Out = Header + Nome01 + FirstCol + str(n) + " = " + PRE + cfg.Sep + AccessName +'.' + NomeSegnale + '.' + s + cfg.Sep + comment
            else:
                Out =  FirstCol + str(n) + " = " + PRE + cfg.Sep + AccessName +'.' + NomeSegnale + '.' + s + cfg.Sep + comment
            

            # stampo l'uscita sul file
            utils.OutFileUTF16(os.getcwd() + cfg.bars + cfg.NomeCartellaOUT + cfg.bars  + cfg.fileIOMESSAGE_Pre + '_' + FromTo + Mac,Out) 
            
            # se sono in fondo ai segnali, completo il file fino all'ultimo numero utile 
            if s == last:
                #print('Siamo in fondo a ' + NomeSegnale + ' che contiene ' + str(n) + ' elementi')
                for d in range(int(n) + 1, MaxRow + 1):
                    if d in range(1,10):
                        d = '0' + str(d)
                    Out = FirstCol + str(d) + " = "
                    utils.OutFileUTF16(os.getcwd() + cfg.bars + cfg.NomeCartellaOUT + cfg.bars  + cfg.fileIOMESSAGE_Pre + '_' + FromTo + Mac,Out) 

            n = int(n) + 1 # avanti il prossimo
            
    except KeyError:   # interecetto l'assenza del sengnale nel PLC
        print(colored('INFO > ',cfg.ColorInfo) + NomeSegnale + ' NOT PRESENT')
    

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





def CycleDesc(NomePrg,NomeStruct,NomeCiclo,NomeStructPhMsg,MacCyc,OutFile,programs,MacCodeList,HmiVer=0,contr_tags = None):
    """Stampa su file i tre blocchi di commenti per un ciclo (PHASES.eng)

    Args:
        NomePrg (str): Nome del programma PLC in cui riesiede il ciclo (ES: FILLER)
        NomeStruct (str): Nome della struttura PLC del ciclo (ES: D40_00)
        NomeCiclo (str): ES: Drainage
        NomeStructPhMsg (str): Nome struttura PhaseMsgInput (ed: D40_01)
        MacCyc (str): nome macchina per header sezione (Es: FIL )
        OutFile (str): File di uscita
        programs (ElementDict): dizionari con l'elenco dei programmi del POS (es: PLC della filler, PLC del processo)
        MacCodeList (list): lista dei codici commerciali di macchina (CA1 etc , per mettere tilde) 
        HmiVer (int): 0- mette la 'V;'
        contr_tags : struttura tag controllore se necessario usarla (es: il phmsginput del ciclo dbload è nelle tag controllore)
    """
    # folder di uscita viene creato se non esiste
    OutDir = os.getcwd() + cfg.bars + cfg.NomeCartPhasesOUT + cfg.bars
    if not os.path.exists (OutDir):
        os.makedirs(OutDir)
    
      # svuoto la cartella da eventuali files precedenti
    #utils.DeleteFilesInFolder(OutDir)

    # Trappola per verificare che esista il ciclo nel PLC
    try:
        programs[NomePrg].tags[NomeStruct][NomeCiclo]
    except:
        print(colored('INFO -> Cycle ' + NomeStruct + '.' + NomeCiclo + ' Not Found in PLC program ' + NomePrg,cfg.ColorInfo))
        return False

    ###########
    ## PHASE ##
    ###########
    PhaseDesc = programs[NomePrg].tags[NomeStruct][NomeCiclo]['Phase'].description # description indica il commento della tag

    if PhaseDesc is not None: # potrebbe mancare il commento nella tag a PLC
        # rimuovo header dal commento
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
    MaxNCycleMsg = 32

    # Ricavo la dimensione del CycleMsgInput
    CMIArrSize = programs[NomePrg].tags[NomeStruct][NomeCiclo]['CycleMsgInput'].shape[0]

    for a in range(0,CMIArrSize): # scorro .CycleMsgInput è un array 
       
        for i in range(0,MaxNCycleMsg): # scorro ogni DINT di .CycleMsgInput
            if programs[NomePrg].tags[NomeStruct][NomeCiclo]['CycleMsgInput'][a][i].description is not None:
            
                nMSG = MaxNCycleMsg * a + i+1  # il numero del messaggio è il bit + 1 nel PLC e si va avanti
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
                else:            #(HMI GRIGIA)
                    CycleMsgDesc = CycleMsgDesc + str(nMSG) + '= - ' + msg.strip('\n') + ('\n')

    CycleMsgDesc = '0= \n' + CycleMsgDesc # aggiungo lo 0= all'inizio del blocco

    # se non ho trovato neanche un commento nelle variabili lo segnalo nel file
    if CycleMsgDesc == '':
        CycleMsgDesc = '! NO COMMENTS IN PLC TAGS !'

    ############
    # PHASEMSG #
    ############
    PhaseMsgDesc = ''
    MaxNMsg = 32
   

    
    if NomeStructPhMsg is not None: # NON TUTTI I CICLI HANNO PHASE MESSAGE
        
        ## Verifico se devo usare la tag a livello controllore 
        Flag_CTL = False
        if contr_tags != None:
            Flag_CTL = True
        else:
            Flag_CTL = False
        ##

        try: # potrebbe non essere presente nel software PLC in esame il PhaseMessageInput

            # Ricavo la dimensione dell'array PhaseMessageInput
            if Flag_CTL:
                PMIArrSize = contr_tags[NomeStructPhMsg]['PhaseMessageInput'].shape[0]
            else:
                PMIArrSize = programs[NomePrg].tags[NomeStructPhMsg]['PhaseMessageInput'].shape[0]
        
            for a in range(0,PMIArrSize): #scorro ogni array
                for i in range(0,MaxNMsg):   #scorro ogni bit dell array
                    try: # nel caso non ci sia la variabile di struttura Phase Msg
                        if Flag_CTL:
                            description = contr_tags[NomeStructPhMsg]['PhaseMessageInput'][a][i].description
                        else:
                            description = programs[NomePrg].tags[NomeStructPhMsg]['PhaseMessageInput'][a][i].description               
                        if description is not None:
                            # nMSG = i+1
                            nMSG = MaxNMsg * a + i + 1 # i msg nell'array successivo hanno numero incrementale
                            if Flag_CTL:
                                PhaseMsgDescA = contr_tags[NomeStructPhMsg]['PhaseMessageInput'][a][i].description + '\n'
                            else:
                                PhaseMsgDescA = programs[NomePrg].tags[NomeStructPhMsg]['PhaseMessageInput'][a][i].description + '\n'
                            try:
                                # nel caso nei commenti le frasi siano separate da newline
                                PhaseMsgDescSplit =  PhaseMsgDescA.split('\n')
                                msg = PhaseMsgDescSplit[2].strip('\n') + '\n'

                                 ### AGGIUNGE TILDE NEI TAG DISPOSITIVO
                                for tag in MacCodeList:
                                    idxTag = msg.find(tag) #cerco l'indice della tag
                                    if idxTag >= 0:
                                        msg = msg[:idxTag] + cfg.TagChar + msg[idxTag:]


                            except:
                                try:
                                    # casefold rende tutto minuscolo in modo piu aggressivo rispetto a lower
                                    id = PhaseMsgDescA.casefold().index('message') + len('message') + 3 # cerco MESSAGE
                                    msg = utils.mid(PhaseMsgDescA,id,len(PhaseMsgDescA))

                                     ### AGGIUNGE TILDE NEI TAG DISPOSITIVO
                                    for tag in MacCodeList:
                                        idxTag = msg.find(tag) #cerco l'indice della tag
                                        if idxTag >= 0:
                                            msg = msg[:idxTag] + cfg.TagChar + msg[idxTag:]
                                        

                                except:
                                    msg = PhaseMsgDescA #nel caso peggiore il messaggio è tutto il commento così come lo trovo

                                     ### AGGIUNGE TILDE NEI TAG DISPOSITIVO
                                    for tag in MacCodeList:
                                        idxTag = msg.find(tag) #cerco l'indice della tag
                                        if idxTag >= 0:
                                            msg = msg[:idxTag] + cfg.TagChar + msg[idxTag:]
                                       

                            if HmiVer == 0:  #(HMI BLU):
                                PhaseMsgDesc = PhaseMsgDesc + str(nMSG) + '= V;' + msg.strip('\n') + ('\n')
                            else:            #(HMI GRIGIA)
                                PhaseMsgDesc = PhaseMsgDesc + str(nMSG) + '= ' + msg.strip('\n') + ('\n')
                    except(KeyError):
                        pass
        except(KeyError):
            pass
    else:
        PhaseMsgDesc = ''

    if PhaseMsgDesc == '':
        PhaseMsgDesc = '! NO COMMENTS IN PLC TAGS !'

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


#######################
# TAGNAMELIST LANG ####
#######################

def ExportTagsComments(tags,outfile):
    """crea un file di testo con i commenti delle tags (TagNameListLang)

    Args:
        tags (ElementDict): variabili da cui ricavare i commenti dal plc
        outfile (str): percorso completo del file di output
    """
    if tags is not None:
        # lista di tutti le possibili iniziali delle variabili con commento
        deviceCodes = ['CONC','DGTA','DGTL','DGTH','DGTM','FLWL','FLWN','FLWV','LVLM','LVLT','MMOD','MOTR','PRSM','PRSP','TEMP','VALV','VMOD','VOLU','WGTG','SPDH']

        # lista con le variabili a livello controllore
        nomi_variabili = tags.names
        
        # cancello il file di output se già esiste
        if os.path.exists(outfile):
            os.remove(outfile)

        # scrivo nome della sezione nel file
        utils.OutFileUCS2LeBom(outfile,'[TAGNAMELISTLANG]')

        for n in nomi_variabili:
            # la lunghezza delle variabili è 17 (esempio MOTR_SH1_D61PPX01)
            if utils.left(n,4) in deviceCodes and len(n)==17:
                comment = tags[n].description.replace('\n',' ')
                # rimuovo le prime tre lettere e l'underscore (es SH1_) dal commento
                if comment[3] == '_':
                    comment = utils.mid(comment,4,100)
                line = n +' = ' + comment
                utils.OutFileUCS2LeBom(outfile,line)

        print(colored('Tags comment printed to file '+ outfile,cfg.ColorInfo))
    else:
        print(colored('ExportTagsComments: Tag structure is not present!',cfg.ColorAlarm))
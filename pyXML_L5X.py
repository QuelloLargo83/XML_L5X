
import argparse
import cmd
from distutils.command.config import config
import os
import sys
import l5x
import configparser
import utils
from os import listdir
from os.path import isfile, join
import fnz
import cfg
from version import __version__, __author__
from termcolor import colored



##########
## MAIN ##
##########


#####################
## HELP e ARGPARSE ##
#####################
args = argparse.ArgumentParser()
args.add_argument("-v", "--version",action="store_true", help = "show program version")
args.add_argument("--cycleslist",	action="store_true", help = "extract cycle list")
args.add_argument("--cycles",	    action="store_true", help = "extract PHASES")
args.add_argument("--iomsg",	    action="store_true", help = "extract IOMESSAGES")
stdargs = args.parse_args()


    # ###############################
    # ## STAMPO VERSIONE PROGRAMMA ##
    # ###############################
if stdargs.version:
    MainProgram = os.path.splitext(os.path.basename(__file__))[0] # leggo il nome del file che da il nome al programma
    print()
    print (colored(MainProgram,'yellow') + colored('  version: ','green') + colored(__version__,'yellow' ))
    print()

    raise SystemExit(0) # esci immediatamente dal programma

    
#  GESTIONE HELP #
#se non viene passato alcun argomento, la lista ha un solo elemento che è il percorso completo del sorgente
# in questo caso mostro gli switch disponibili
if len(sys.argv) == 1:
    MainProgram = os.path.splitext(os.path.basename(__file__))[0] # leggo il nome del file che da il nome al programma
    print()
    print (colored(MainProgram,'yellow') + colored('  version: ','green') + colored(__version__,'yellow' ))
    print()
    args.print_help() #stampa con argparse, l'help
   
else:
    
    #################################
    ##### PREPARAZIONE STRUTTURE ####
    #################################

    # RICAVO .L5X della filler
    FilL5X = None
    for file in os.listdir(cfg.PLCFilFolder):
        if file.endswith(".L5X"):
            FilL5X = cfg.PLCFilFolder + file

    # RICAVO .L5X della filler
    ProL5X = None
    for file in os.listdir(cfg.PLCProFolder):
        if file.endswith(".L5X"):
            ProL5X = cfg.PLCProFolder + file

    # RICAVO CFG_PAGE.ini
    CFGPAGEini = None
    for file in os.listdir(cfg.HMIFolder):
        if file.endswith(".INI"):
            CFGPAGEini = cfg.HMIFolder + file
    
    # RICAVO IOMESSAGES_PLxxxx.ENG
    IOMSGENG = None
    for file in os.listdir(cfg.HMIFolder):
        if file.endswith(".ENG"):
            IOMSGENG = cfg.HMIFolder + file


    #### PLC FILLER #####
    try:
        # carico il file L5X in memoria
        prj = l5x.Project(FilL5X)
        # ctl_tags è un ElementDict contenente le tag a livello controllore
        ctl_tags = prj.controller.tags
        # lista tag name livello controllore
        tag_names = ctl_tags.names
        # ELEMENTDICT con i programmi
        programs = prj.programs
        # lista nomi programmi
        programs_names = programs.names
    except:
        print(colored('FILLER L5X not supplied!',cfg.ColorAlarm))

    #### PLC PROCESSO #####
    try:
        PROC_prj = l5x.Project(ProL5X)
        PROC_ctl_tags = PROC_prj.controller.tags
        PROC_tag_names = PROC_ctl_tags.names
        PROC_programs = PROC_prj.programs
        PROC_programs_names = PROC_programs.names
    except:
        print(colored('PROCESS L5X not supplied!',cfg.ColorAlarm))

    ####################
    # LISTA NOMI CICLI #
    ####################
   
    if stdargs.cycleslist:
        fnz.ListaCicli(cfg.INIREAD('plcprodcyclevar'),cfg.INIREAD('filecicliprod'),'FILLER',programs) # Cicli Prod
        fnz.ListaCicli(cfg.INIREAD('plcsancyclevar'),cfg.INIREAD('fileciclisan'),'FILLER',programs)   # Cicli San
   

    ##########
    # PHASES #
    ##########
  
    if stdargs.cycles:

        if FilL5X != None and ProL5X != None:

            verHMI = int(cfg.INIREAD('verhmi'))

            # leggo i nomi delle aree di memoria corrispondenti ai cicli
            PLCProdCycleVar = cfg.INIREAD('plcprodcyclevar')
            PLCSanCycleVar = cfg.INIREAD('plcsancyclevar')

            #  svuota cartella di OUTPUT
            OutDir = os.getcwd() + cfg.bars + cfg.NomeCartPhasesOUT + cfg.bars
            if not os.path.exists (OutDir):
                os.makedirs(OutDir)
            utils.DeleteFilesInFolder(OutDir)
        
            # leggo Associazione tra Nome Ciclo e struttura del Phase Message
            Coppie = cfg.INIREAD_COPPIE(cfg.PhaseINI)

            # SANIFICAZIONE #
            ctl_tags_fake = None
            for item in Coppie['SANIFICAZIONE'].items(): 

                # INTERCETTO I CICLI CHE HANNO PHASE MESSAGE DIPENDENTE DAL SUFFISSO CX o FX CHE PESCO DA INI
                if item[0] == 'SipFiller' or item[0] == 'CIP' or item[0] == 'DBLoad':
                    item = list(item) # per modificare devo convertire in list (tupla non è modificabile)
                    item[1] = item[1] + '_'+ cfg.INIREAD('fx_cx')
                    #item = tuple(item)
                    if item[0] == 'DBLoad':  # condizione speciale perché il phasemsginput è nelle tag a livello controllore
                        ctl_tags_fake = ctl_tags
                    else:
                        ctl_tags_fake = None

                fnz.CycleDesc('FILLER',PLCSanCycleVar,item[0],item[1],'FIL','Phase_'+ item[0]+'.ENG',programs,verHMI,ctl_tags_fake) #item[0] = nomeCiclo, item[1] = struct PhMSG
            # /SANIFICAZIONE #

            # PRODUZIONE #
            for item in Coppie['PRODUZIONE'].items():
                fnz.CycleDesc('FILLER',PLCProdCycleVar,item[0],item[1],'FIL','Phase_'+ item[0]+'.ENG',programs,verHMI)
            # /PRODUZIONE #

            print ('INFO -> FILES GENERATED IN FOLDER ' + colored(os.getcwd() + cfg.bars + cfg.NomeCartPhasesOUT+ cfg.bars,cfg.ColorInfo))
        #sys.exit(0)
        else:
            print (colored('PLC L5x files not supplied!',cfg.ColorAlarm))


    ###############
    # IO MESSAGES #
    ###############
    
    if stdargs.iomsg:

        if IOMSGENG != None and CFGPAGEini != None and FilL5X != None and ProL5X != None:

            # TO DO: trovare il modo di leggere ACCESSNAME
            #      : Unire a modo le coppie di files
            #      : 

            #  ricavo la lista della macchine esterne #
            CFGPAGE = configparser.ConfigParser(strict= False)
            CFGPAGE.read_file(open(CFGPAGEini,encoding='utf-8'))
        
            lista_sezioni = CFGPAGE.sections()               # lista con le sezioni
            lista_item = CFGPAGE.items(lista_sezioni[int( cfg.INIREAD('cfg_iomac')) ])     # lista della sezione CFG_IOMAC
            lista_itemDICT = dict(lista_item)               
            lista_macc = []     # lista delle macchine 
            
            ## recupero le altre macchine da IOMESSAGE.eng e integro la lista
            IOMSG = configparser.ConfigParser(strict=False)
            IOMSG.read_file(open(IOMSGENG,encoding='utf-16'))
            IOMSG_listSec = IOMSG.sections()
            IOMSG_listIt = IOMSG.items(IOMSG_listSec[0]) # LIST è la prima sezione quindi 0
            IOMSG_listItDICT = dict(IOMSG_listIt)
            
            IOMSG_mac = list(IOMSG_listItDICT.values()) #prendo solo i valori e li metto in una lista
            
            for i in range(1, len(IOMSG_mac)):
                mac = utils.left(IOMSG_mac[i],3)
                if  (mac is not None) and (mac != '') and utils.left(mac,1) != cfg.DisablingChar:  # salto eventuali buchi e macchine disabilitate        
                    lista_macc.append(mac)                  # e le aggiungo alla lista

            ############


            # leggo la lista delle macchine di cui leggere i segnali di scambio
            for k in lista_itemDICT.keys():
                mac = lista_itemDICT.get(str(k))
            
                if (mac is not None) and (mac != '') and utils.left(mac,1) != cfg.DisablingChar :      # salto eventuali buchi e mac disabilitate
                    lista_macc.append(mac) # aggiungo alla lista macchine

            
            # creo la cartella temporanea di uscita se non esiste
            OutDir = os.getcwd() + cfg.bars + cfg.NomeCartellaOUT + cfg.bars
            if not os.path.exists (OutDir):
                os.makedirs(OutDir)
            #svuoto la cartella da eventuali files precedenti
            utils.DeleteFilesInFolder(OutDir)
            
            # creo la cartella finale con i file uniti
            OutDirFIN = os.getcwd() + cfg.bars + cfg.NomeCartellaFINALE + cfg.bars
            if not os.path.exists (OutDirFIN):
                os.makedirs(OutDirFIN)
            # svuoto la cartella da eventuali files precedenti
            utils.DeleteFilesInFolder(OutDirFIN)
            

            # creo i file IOMESSAGE facendo scorrere la lista delle macchine
            for a in lista_macc:
            
                match a:
                # casi speciali    
                    case 'UTH':    
                        ACNAME = 'ABUTH1'
                        SigFROM = 'SignalUTHToFIL'
                        SigTO = 'SignalFILToPRO.UTH'
                        
                        fnz.SignalExc(SigFROM,ACNAME,a,OutDir,PROC_ctl_tags,'SX')  
                        fnz.SignalExc(SigTO,'ABFIL1',a,OutDir,ctl_tags,'DX')   

                    case 'UDX':
                        ACNAME = 'ABUTH1'     
                        SigFROM= 'SignalUDXToFIL'    
                        SigTO = 'SignalFILToPRO.UDX' 

                        fnz.SignalExc(SigFROM,ACNAME,a,OutDir,PROC_ctl_tags,'SX')    
                        fnz.SignalExc(SigTO,'ABFIL1',a,OutDir,ctl_tags,'DX') 
                    

                    case 'CFT':
                        ACNAME = 'ABFIL1'     
                        SigFROM= 'SignalFILFromBFT'    
                        SigTO = 'SignalFILToBFT' 

                        fnz.SignalExc(SigFROM,ACNAME,a,OutDir,ctl_tags)
                        fnz.SignalExc(SigTO,ACNAME,a,OutDir,ctl_tags) 

                # casi standard
                    case _:

                        # variabili standard
                        ACNAME = 'ABFIL1'
                        SigFROM = 'SignalFILFrom'
                        SigTO = 'SignalFILTo'

                        
                        fnz.SignalExc(SigFROM + a,ACNAME,a,OutDir,ctl_tags)
                        fnz.SignalExc(SigTO + a,ACNAME,a,OutDir,ctl_tags)
            
            # unisco i file corrispondenti
            for m in lista_macc:
                fnz.MergeFiles(OutDir,m,OutDirFIN)
            
            # CANCELLO la cartella d'appoggio
            utils.DeleteFolder(OutDir)
        

            print('Files generated in : ' + colored(OutDirFIN,cfg.ColorInfo) ) # avviso in quale cartella ho generato i file uniti
        else:
            print(colored('HMI or PLC files not supplied!',cfg.ColorAlarm))


    ####################
    # TAG CONTROLLORE  #
    ####################

    #stampa lista tag a livello controllore
# with open(fileControllerTags,'w',encoding=IntouchEncoding) as f:
#     for tag in tag_names:
#         f.write(tag + '\n')

    #### PROVE ####
        
        #va in ordine alfabetico
    # for i in range(0, len(ctl_tags.names)):
    #     if ctl_tags.names[i] == 'D60_00':
    #         print(ctl_tags.names[i])
    #         print(ctl_tags[ctl_tags.names[i]].names)
    #         print(ctl_tags[ctl_tags.names[i]].value)
    #         print(ctl_tags[ctl_tags.names[i]].description)







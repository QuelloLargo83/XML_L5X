#from ast import Str
#from argparse import HelpFormatter
import argparse
import cmd
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
    args.print_help() #stampa con argparse, l'help
   
else:
    
    #################################
    ##### PREPARAZIONE STRUTTURE ####
    #################################
    # carico il file L5X in memoria
    prj = l5x.Project(cfg.INIREAD('fileplc'))
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
   
    if stdargs.cycleslist:
        fnz.ListaCicli(cfg.INIREAD('plcprodcyclevar'),cfg.INIREAD('filecicliprod'),'FILLER',programs) # Cicli Prod
        fnz.ListaCicli(cfg.INIREAD('plcsancyclevar'),cfg.INIREAD('fileciclisan'),'FILLER',programs)   # Cicli San
   

    ##########
    # PHASES #
    ##########
  
    if stdargs.cycles:

        verHMI = cfg.INIREAD('verhmi')
        verHMI = int(verHMI)

        # leggo i nomi delle aree di memoria corrispondenti ai cicli
        PLCProdCycleVar = cfg.INIREAD('plcprodcyclevar')
        PLCSanCycleVar = cfg.INIREAD('plcsancyclevar')

        #  svuota cartella
        OutDir = os.getcwd() + cfg.bars + cfg.NomeCartPhasesOUT + cfg.bars
        if not os.path.exists (OutDir):
            os.makedirs(OutDir)
        utils.DeleteFilesInFolder(OutDir)
    
        # leggo Associazione tra Nome Ciclo e struttura del Phase Message
        Coppie = cfg.INIREAD_COPPIE(cfg.PhaseINI)

        # SANIFICAZIONE #
        for item in Coppie['SANIFICAZIONE'].items(): 
            fnz.CycleDesc('FILLER',PLCSanCycleVar,item[0],item[1],'FIL','Phase_'+ item[0]+'.ENG',programs,verHMI) #item[0] = nomeCiclo, item[1] = struct PhMSG
        
            ## QUESTI RIMANGONO FUORI PERCHE HANNO IL PHASEMSG dipende da FX o CX
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'DBLoad','D28_60_'+ cfg.INIREAD('fx_cx'),'FIL','Phase_DBLoad.ENG',programs,verHMI)
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'SipFiller','D60_06_'+ cfg.INIREAD('fx_cx'),'FIL','Phase_SipFiller.ENG',programs,verHMI)
        # /SANIFICAZIONE #

        # PRODUZIONE #
        for item in Coppie['PRODUZIONE'].items():
            fnz.CycleDesc('FILLER',PLCProdCycleVar,item[0],item[1],'FIL','Phase_'+ item[0]+'.ENG',programs,verHMI)
        # /PRODUZIONE #
        

        # SANIFICAZIONE #
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'Drainage','D60_01','FIL','Phase_Drainage.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'COP','D60_02','FIL','Phase_COP.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'DBLoad','D28_60_'+ cfg.INIREAD('fx_cx'),'FIL','Phase_DBLoad.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'CIP','D60_04','FIL','Phase_CIP.ENG',programs) # occhio che questo ne ha due possibili di PhaseMessageInput
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'SteamFilter','D60_05','FIL','Phase_SteamFilter.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'SipFiller','D60_06_'+ cfg.INIREAD('fx_cx'),'FIL','Phase_SipFiller.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'SteamBarrier','D60_09','FIL','Phase_SteamBarrier.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'PAAExternal','D60_07','FIL','Phase_PAAExternal.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'HEPA1','D60_08_SV1','FIL','Phase_HEPA1.ENG',programs)       #occhio che qui c'è SV1!!
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'DBUnLoad',None,'FIL','Phase_DBUnLoad.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'DBLoad_PSD',None,'PSD','Phase_DBLoad_PSD.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'Rinse_PSD',None,'PSD','Phase_Rinse_PSD.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'CIP_PSD',None,'PSD','Phase_CIP_PSD.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'SIP_PSD',None,'PSD','Phase_SIP_PSD.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'DBUnLoad_PSD',None,'PSD','Phase_DBUnLoad_PSD.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'BellowsIntegrity_PSD',None,'PSD','Phase_BellowsIntegrity_PSD.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'SteamBarrier_PSD',None,'PSD','Phase_SteamBarrier_PSD.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCSanCycleVar,'CXJackTest',None,'FIL','Phase_CXJackTest.ENG',programs)
        
        # # PRODUZIONE #
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'TankStartUp','D40_02','FIL','Phase_TankStartup.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'TapsFlowing','D40_03','FIL','Phase_TapsFlowing.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'BaseRinsing','D40_09','FIL','Phase_BaseRinsing.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'ProductionDrainage','D40_10','FIL','Phase_ProductionDrainage.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'EndProduction','D40_11','FIL','Phase_EndProduction.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'TankRinsing','D40_12','FIL','Phase_TankRinsing.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'TankCooling', 'D40_13','FIL','Phase_TankCooling.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'ShortCycle', 'D40_20','FIL','Phase_ShortCycle.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'ShortCycleBMMInterface', 'D40_21','FIL','Phase_ShortCycleBMMInterface.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'EmptyBottles', 'D40_30','FIL','Phase_EmptyBottles.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'MicroSampling', 'D40_31','FIL','Phase_MicroSampling.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'ChangeOver', 'D40_32','FIL','Phase_ChangeOver.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'PSDTapsFlowing', 'D40_15','FIL','Phase_PSDTapsFlowing.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'PSDProductionDrainage', 'D40_16','FIL','Phase_PSDProductionDrainage.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'PSDTankRinsing', 'D40_17','FIL','Phase_PSDTankRinsing.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'PSDTankStartUp', 'D40_07','FIL','Phase_PSDTankStartUp.ENG',programs)
        # fnz.CycleDesc('FILLER',PLCProdCycleVar,'BaseSterilization', 'D40_05','FIL','Phase_BaseSterilization.ENG',programs)

        print ('INFO -> FILES GENERATED IN FOLDER ' +  os.getcwd() + cfg.bars + cfg.NomeCartPhasesOUT+ cfg.bars)
    #sys.exit(0)


    ###############
    # IO MESSAGES #
    ###############
    
    if stdargs.iomsg:
        # TO DO: trovare il modo di leggere ACCESSNAME
        #      : Unire a modo le coppie di files
        #      : 

        #  ricavo la lista della macchine esterne #
        CFGPAGE = configparser.ConfigParser(strict= False)
        #CFGPAGE.read_file(open(cfg.fileCFG_PAGE,encoding='utf-8')) 
        CFGPAGE.read_file(open(cfg.INIREAD('filecfgpage'),encoding='utf-8'))
       
        lista_sezioni = CFGPAGE.sections()               # lista con le sezioni
        lista_item = CFGPAGE.items(lista_sezioni[int( cfg.INIREAD('cfg_iomac')) ])     # lista della sezione CFG_IOMAC
        lista_itemDICT = dict(lista_item)               
        lista_macc = []     # lista delle macchine 
        
        # leggo la lista delle macchine di cui leggere i segnali di scambio
        for k in range(1,len(lista_itemDICT.keys())):
            if (lista_itemDICT.get(str(k)) is not None):      # salto eventuali buchi
                lista_macc.append(lista_itemDICT.get(str(k))) # prendo le prime tre lettere che indicano la macchina 

        
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
        
        # creo i file IOMESSAGE
        for a in lista_macc:
            fnz.SignalExc('SignalFILFrom'+a,'ABFIL1',a,OutDir,ctl_tags)
            fnz.SignalExc('SignalFILTo'+a,'ABFIL1',a,OutDir,ctl_tags)
        
        # unisco i file corrispondenti
        for m in lista_macc:
            fnz.MergeFiles(OutDir,m,OutDirFIN)
        
        # svuoto la cartella d'appoggio
        utils.DeleteFolder(OutDir)
       

        print('Files generated in : ' + OutDirFIN ) # avviso in quale cartella ho generato i file uniti


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







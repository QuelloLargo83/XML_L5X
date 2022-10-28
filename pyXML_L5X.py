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
    MainProgram = os.path.splitext(os.path.basename(__file__))[0]
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
   
    # if sys.argv[1].strip() == '--cycleslist':
    if stdargs.cycleslist:
        fnz.ListaCicli(cfg.INIREAD('plcprodcyclevar'),cfg.INIREAD('filecicliprod'),'FILLER',programs) # Cicli Prod
        fnz.ListaCicli(cfg.INIREAD('plcsancyclevar'),cfg.INIREAD('fileciclisan'),'FILLER',programs)   # Cicli San
   

    ##########
    # PHASES #
    ##########
    # SANIFICAZIONE #
    # with open (os.getcwd() + '\\' + fileCicliSan,'r',encoding=IntouchEncoding) as fcs:
    #     SanCycles = fcs.readlines()
    #     for sanc in SanCycles:
    #         CycleDesc('FILLER','D60_00',sanc.strip('\n'),20,'D60_01','FIL',os.getcwd() + '\Phase_'+ sanc.strip('\n') +'_TEST.ENG')
    # if sys.argv[1].strip() == '--cycles':
    if stdargs.cycles:
        PLCProdCycleVar = cfg.INIREAD('plcprodcyclevar')
        PLCSanCycleVar = cfg.INIREAD('plcsancyclevar')

        # SANIFICAZIONE #
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'Drainage','D60_01','FIL','Phase_Drainage.ENG',programs)
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'COP','D60_02','FIL','Phase_COP.ENG',programs)
        try:
            fnz.CycleDesc('FILLER',PLCSanCycleVar,'DBLoad','D28_60_'+ cfg.INIREAD('fx_cx'),'FIL','Phase_DBLoad.ENG',programs)
        except(KeyError):
            pass
        try:
            fnz.CycleDesc('FILLER',PLCSanCycleVar,'CIP','D60_04','FIL','Phase_CIP.ENG',programs) # occhio che questo ne ha due possibili di PhaseMessageInput
        except(KeyError):
            pass
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'SteamFilter','D60_05','FIL','Phase_SteamFilter.ENG',programs)
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'SipFiller','D60_06_'+ cfg.INIREAD('fx_cx'),'FIL','Phase_SipFiller.ENG',programs)
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'SteamBarrier','D60_09','FIL','Phase_SteamBarrier.ENG',programs)
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'PAAExternal','D60_07','FIL','Phase_PAAExternal.ENG',programs)
        try:
            fnz.CycleDesc('FILLER',PLCSanCycleVar,'HEPA1','D60_08_SV1','FIL','Phase_HEPA1.ENG',programs)       #occhio che qui c'è SV1!!
        except(KeyError):
            pass
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'DBUnLoad',None,'FIL','Phase_DBUnLoad.ENG',programs)
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'DBLoad_PSD',None,'PSD','Phase_DBLoad_PSD.ENG',programs)
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'Rinse_PSD',None,'PSD','Phase_Rinse_PSD.ENG',programs)
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'CIP_PSD',None,'PSD','Phase_CIP_PSD.ENG',programs)
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'SIP_PSD',None,'PSD','Phase_SIP_PSD.ENG',programs)
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'DBUnLoad_PSD',None,'PSD','Phase_DBUnLoad_PSD.ENG',programs)
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'BellowsIntegrity_PSD',None,'PSD','Phase_BellowsIntegrity_PSD.ENG',programs)
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'SteamBarrier_PSD',None,'PSD','Phase_SteamBarrier_PSD.ENG',programs)
        fnz.CycleDesc('FILLER',PLCSanCycleVar,'CXJackTest',None,'FIL','Phase_CXJackTest.ENG',programs)
        
        # PRODUZIONE #
        fnz.CycleDesc('FILLER',PLCProdCycleVar,'TankStartUp','D40_02','FIL','Phase_TankStartup.ENG',programs)
        fnz.CycleDesc('FILLER',PLCProdCycleVar,'TapsFlowing','D40_03','FIL','Phase_TapsFlowing.ENG',programs)
        fnz.CycleDesc('FILLER',PLCProdCycleVar,'BaseRinsing','D40_09','FIL','Phase_BaseRinsing.ENG',programs)
        fnz.CycleDesc('FILLER',PLCProdCycleVar,'ProductionDrainage','D40_10','FIL','Phase_ProductionDrainage.ENG',programs)
        fnz.CycleDesc('FILLER',PLCProdCycleVar,'EndProduction','D40_11','FIL','Phase_EndProduction.ENG',programs)
        fnz.CycleDesc('FILLER',PLCProdCycleVar,'TankRinsing','D40_11','FIL','Phase_TankRinsing.ENG',programs)
        fnz.CycleDesc('FILLER',PLCProdCycleVar,'TankCooling', 'D40_13','FIL','Phase_TankCooling.ENG',programs)

        print ('INFO -> FILES GENERATED IN FOLDER ' +  os.getcwd() + '\\' + cfg.NomeCartPhasesOUT+ '\\')
    #sys.exit(0)


    ###############
    # IO MESSAGES #
    ###############
    #if sys.argv[1].strip() == '--iomsg':
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
        OutDir = os.getcwd() +'\\'+ cfg.NomeCartellaOUT +'\\'
        if not os.path.exists (OutDir):
            os.makedirs(OutDir)
        OutDirFIN = os.getcwd() +'\\'+ cfg.NomeCartellaFINALE +'\\'
        if not os.path.exists (OutDirFIN):
            os.makedirs(OutDirFIN)
        
        # creo i file IOMESSAGE
        for a in lista_macc:
            fnz.SignalExc('SignalFILFrom'+a,'ABFIL1',a,OutDir,ctl_tags)
            fnz.SignalExc('SignalFILTo'+a,'ABFIL1',a,OutDir,ctl_tags)
        
        # unisco i file corrispondenti
        for m in lista_macc:
            fnz.MergeFiles(OutDir,m,OutDirFIN)
        
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







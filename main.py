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
import fnz
import cfg



##########
## MAIN ##
##########

#  GESTIONE HELP #
HelpFile = cfg.ResourceFolder + cfg.fileHELP
#se non viene passato alcun argomento, la lista ha un solo elemento che è il percorso completo del sorgente
# in questo caso mostro gli switch disponibili
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
    prj = l5x.Project(cfg.filePLC)
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
        fnz.ListaCicli(cfg.PLCProdCycleVAR,cfg.fileCicliProd,'FILLER',programs) # Cicli Prod
        fnz.ListaCicli(cfg.PLCSanCycleVar,cfg.fileCicliSan,'FILLER',programs)   # Cicli San
   
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
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'Drainage','D60_01','FIL','Phase_Drainage_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'COP','D60_02','FIL','Phase_COP_TEST.ENG',programs)
        # ##fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'DBLoad','D28_60_CX','FIL',os.getcwd() + '\Phase_DBLoad_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'CIP','D60_04','FIL','Phase_CIP_TEST.ENG',programs) # occhio che questo ne ha due possibili di PhaseMessageInput
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'SteamFilter','D60_05','FIL','Phase_SteamFilter_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'SipFiller','D60_06_'+ cfg.Fx_Cx,'FIL','Phase_SipFiller_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'SteamBarrier','D60_09','FIL','Phase_SteamBarrier_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'PAAExternal','D60_07','FIL','Phase_PAAExternal_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'HEPA1','D60_08_SV1','FIL','Phase_HEPA1_TEST.ENG',programs)       #occhio che qui c'è SV1!!
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'DBUnLoad',None,'FIL','Phase_DBUnLoad_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'DBLoad_PSD',None,'PSD','Phase_DBLoad_PSD_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'Rinse_PSD',None,'PSD','Phase_Rinse_PSD_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'CIP_PSD',None,'PSD','Phase_CIP_PSD_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'SIP_PSD',None,'PSD','Phase_SIP_PSD_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'DBUnLoad_PSD',None,'PSD','Phase_DBUnLoad_PSD_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'BellowsIntegrity_PSD',None,'PSD','Phase_BellowsIntegrity_PSD_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'SteamBarrier_PSD',None,'PSD','Phase_BellowsIntegrity_SteamBarrier_PSD.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCSanCycleVar,'CXJackTest',None,'FIL','Phase_CXJackTest.ENG',programs)
        
        # PRODUZIONE #
        # fnz.CycleDesc('FILLER',cfg.PLCProdCycleVAR,'TankStartUp','D40_02','FIL','Phase_TankStartup_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCProdCycleVAR,'TapsFlowing','D40_03','FIL','Phase_TapsFlowing_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCProdCycleVAR,'BaseRinsing','D40_09','FIL','Phase_BaseRinsing_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCProdCycleVAR,'ProductionDrainage','D40_10','FIL','Phase_ProductionDrainage_TEST.ENG',programs)
        # fnz.CycleDesc('FILLER',cfg.PLCProdCycleVAR,'EndProduction','D40_11','FIL','Phase_EndProduction_TEST.ENG',programs)
        fnz.CycleDesc('FILLER',cfg.PLCProdCycleVAR,'TankRinsing','D40_11','FIL','Phase_TankRinsing_TEST.ENG',programs)
        fnz.CycleDesc('FILLER',cfg.PLCProdCycleVAR,'TankCooling', 'D40_13','FIL','Phase_TankCooling_TEST.ENG',programs)

    #sys.exit(0)


    ###############
    # IO MESSAGES #
    ###############
    if sys.argv[1].strip() == '--iomsg':
        # TO DO: trovare il modo di leggere ACCESSNAME
        #      : Unire a modo le coppie di files
        #      : 

        #  ricavo la lista della macchine esterne #
        CFGPAGE = configparser.ConfigParser(strict= False)
        CFGPAGE.read_file(open(cfg.fileCFG_PAGE,encoding='utf-8')) 
        lista_sezioni = CFGPAGE.sections()               # lista con le sezioni
        lista_item = CFGPAGE.items(lista_sezioni[cfg.CFG_IOMAC])     # lista della prima sezione CFG_IOMAC
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







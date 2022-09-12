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
        fnz.CycleDesc('FILLER','D60_00','Drainage','D60_01','FIL',os.getcwd() + '\Phase_Drainage_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','COP','D60_02','FIL',os.getcwd() + '\Phase_COP_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','DBLoad','D60_02','FIL',os.getcwd() + '\Phase_DBLoad_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','CIP','D60_04','FIL',os.getcwd() + '\Phase_CIP_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','SteamFilter','D60_05','FIL',os.getcwd() + '\Phase_SteamFilter_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','SipFiller','D60_06_'+ cfg.Fx_Cx,'FIL',os.getcwd() + '\Phase_SipFiller_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','SteamBarrier','D60_09','FIL',os.getcwd() + '\Phase_SteamBarrier_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','PAAExternal','D60_07','FIL',os.getcwd() + '\Phase_PAAExternal_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','HEPA1','D60_08_SV1','FIL',os.getcwd() + '\Phase_HEPA1_TEST.ENG',programs)       #occhio che qui c'è SV1!!
        fnz.CycleDesc('FILLER','D60_00','DBUnLoad',None,'FIL',os.getcwd() + '\Phase_DBUnLoad_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','DBLoad_PSD',None,'FIL',os.getcwd() + '\Phase_DBLoad_PSD_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','Rinse_PSD',None,'FIL',os.getcwd() + '\Phase_Rinse_PSD_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','CIP_PSD',None,'FIL',os.getcwd() + '\Phase_CIP_PSD_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','SIP_PSD',None,'FIL',os.getcwd() + '\Phase_SIP_PSD_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','DBUnLoad_PSD',None,'FIL',os.getcwd() + '\Phase_DBUnLoad_PSD_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','BellowsIntegrity_PSD',None,'FIL',os.getcwd() + '\Phase_BellowsIntegrity_PSD_TEST.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','SteamBarrier_PSD',None,'FIL',os.getcwd() + '\Phase_BellowsIntegrity_SteamBarrier_PSD.ENG',programs)
        fnz.CycleDesc('FILLER','D60_00','CXJackTest',None,'FIL',os.getcwd() + '\Phase_CXJackTest.ENG',programs)
        # PRODUZIONE #
        fnz.CycleDesc('FILLER','D40_00','TankStartUp','D40_02','FIL',os.getcwd() + '\Phase_TankStartup_TEST.ENG',programs)
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







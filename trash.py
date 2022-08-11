################################
# leggo il file originale .ENG #
# per ricavare le macchine che #
# mi interessano ###############
################################
# config = configparser.ConfigParser(strict= False)
# dc = 'IOMessages_PL01447.ENG'

# config.read_file(open(dc,encoding='utf-16')) # anche se è utf-16-le, il cfg parser funziona con utf-16

# lista_sezioni = config.sections()               # lista con le sezioni
# lista_item = config.items(lista_sezioni[0])     # lista della prima sezione [LIST]
# lista_itemDICT = dict(lista_item)               # converto in dizionario
# #print (lista_itemDICT)

# lista_macc = []     # lista delle macchine gia assegnate nel file ENG originale
# lista_macc_en = []  # lista delle sole macchine abilitate

# # leggo la lista delle macchine di cui leggere i segnali di scambio
# for k in range(1,len(lista_itemDICT.keys())):
#     if (lista_itemDICT.get(str(k)) is not None): # salto eventuali buchi
#         lista_macc.append(utils.left(lista_itemDICT.get(str(k)),3)) #prendo le prime tre lettere che indicano la macchina 
# #print(lista_macc)

# # ricavo una lista delle sole macchine abilitate
# for x in lista_macc:
#     if utils.left(x,1) != "_":
#         lista_macc_en.append(x) 

#print(lista_macc_en)




############################################
## ESEMPIO DI COMMENTI CICLI SANIFICAZIONE ####
############################################

## DRAINAGE PHASE DESCRIPTION
PhaseDesc = programs['FILLER'].tags['D60_00']['Drainage']['Phase'].description
print(PhaseDesc)

print('\n')

# DRAINAGE CYCLEMSG DESCRIPTION
for i in range(0,9):
    CycleMsgDesc = programs['FILLER'].tags['D60_00']['Drainage']['CycleMsgInput'][0][i].description
    print(CycleMsgDesc)

print('\n')

# DRAINAGE PHASEMSG DESCRIPTION
for i in range(0,9):                       #occhio!!
    PhaseMsgDesc = programs['FILLER'].tags['D60_01']['PhaseMessageInput'][0][i].description
    print(PhaseMsgDesc)

print('\n')

############################################
## ESEMPIO DI COMMENTI CICLI PRODUZIONE #
############################################

print('.Phase\n')
PhaseDesc = programs['FILLER'].tags['D40_00']['TankStartUp']['Phase'].description
print(PhaseDesc)

print('\n')
print('.CycleMsg\n')

for i in range(0,9):
    CycleMsgDesc = programs['FILLER'].tags['D40_00']['TankStartUp']['CycleMsgInput'][0][i].description
    print(CycleMsgDesc)

print('\n')
print('.PhaseMsg\n')
for i in range(0,9):                       #occhio!!
    PhaseMsgDesc = programs['FILLER'].tags['D40_02']['PhaseMessageInput'][0][i].description
    print(PhaseMsgDesc)

print('\n')

sys.exit(0)
    ######

 #########
    # PROVE #
    #########
    # for i in range(0,9):
    #     try:
    #         print(programs['FILLER'].tags['D60_0' + str(i)].data_type)
    #     except:
    #         print('INFO-> D60_0' + str(i) +' NOT PRESENT')
        # print(programs['FILLER'].tags['D60_01'].data_type)
        # print(programs['FILLER'].tags['D60_02'].data_type)
        # #print(programs['FILLER'].tags['D60_03'].data_type)
        # print(programs['FILLER'].tags['D60_04'].data_type)
        # print(programs['FILLER'].tags['D60_05'].data_type)
        # print(programs['FILLER'].tags['D60_06_CX'].data_type)
        # print(programs['FILLER'].tags['D60_06_FX'].data_type)
        # print(programs['FILLER'].tags['D60_07'].data_type)
        # print(programs['FILLER'].tags['D60_08_SV1'].data_type)
        # print(programs['FILLER'].tags['D60_09'].data_type)
    #sys.exit(0)
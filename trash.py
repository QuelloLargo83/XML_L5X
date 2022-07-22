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

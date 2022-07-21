import l5x
###########
## DATI ###
###########

file = 'P16164_PLC_20220609_00C.L5X' # file sorgente
fileCicliProd = 'NomiCicliProd.txt'
fileControllerTags = 'ControllerTags.txt'
PLCProdCycleVAR = 'D40_00'
###########################################################



# carico il file in memoria
prj = l5x.Project(file)

# ctl_tags è un ElementDict
ctl_tags = prj.controller.tags
# lista tag name livello controllore
tag_names = ctl_tags.names

# lista nomi programmi
programs_names = prj.programs.names

# struttra speciale ELEMENTDICT
programs = prj.programs


# definisco un dizionario vuoto in cui mettere le variabili che mi interessano
struttura = {}
struttura = programs['FILLER'].tags[PLCProdCycleVAR].value

# le chiavi sono i nomi del livello figlio della struttura
nomi_cicli = struttura.keys()

with open(fileCicliProd,'w',encoding='utf-16-le') as f:
    for n in nomi_cicli:
        f.write(n + '\n')

###########

#stampa lista tag a livello controllore
with open(fileControllerTags,'w',encoding='utf-16-le') as f:
    for tag in tag_names:
        f.write(tag + '\n')

#####


def SignalExc (NomeSegnale):
    """_summary_

    Args:
        NomeSegnale (_type_): _description_
    """

    # scambio è un dizionario le cui chiavi rappresentano i nomi dei segnali di scambio
    scambio = ctl_tags[NomeSegnale].value

    #le chiavi rappresentano i campi dei segnali di scambio
    # for s in scambio.keys():
    #     print(s)

    lev2str = [] # coverto poi l'oggetto in stringa

    for s in scambio.keys():
        lev2 = ctl_tags[NomeSegnale][s]
        lev2str = str(lev2) #converto l'oggetto in stringa
        print (lev2str[9:13], ':',s) # recupero il tipo di dato con un mid dell'oggetto


SignalExc('SignalFILFromBSI')

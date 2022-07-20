import l5x
###########
## DATI ###
###########

file = 'P16164_PLC_20220609_00C.L5X' # file sorgente
fileCicliProd = 'NomiCicliProd.txt'
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


programs = prj.programs



# for prg in programmi_names:
#     print(programs[str(prg)].tags['D40_00.TankCooling.Start'])


# definisco un dizionario vuoto in cui mettere le variabili che mi interessano
struttura = {}
struttura = programs['FILLER'].tags[PLCProdCycleVAR].value

# le chiavi sono i nomi del livello figlio della struttura
nomi_cicli = struttura.keys()

with open(fileCicliProd,'w',encoding='utf-16-le') as f:
    for n in nomi_cicli:
        f.write(n + '\n')



#stampa lista tag a livello controllore
with open('ControllerTags.txt','w',encoding='utf-16-le') as f:
    for tag in tag_names:
        f.write(tag + '\n')


########################
## NON FUNZIONA!! problemi di encoding! dovrebbe leggere
###  le funzioni per la ricerca vanno bene
##


PlcFile = 'F:\SCRIPTING\XML_L5X\INI\PLC\STERILCAP\P16378_PLC_00P.L5X'
text = '## D40_00.Production.Phase - MESSAGE FOR HMI ##'




def line_num_for_phrase_in_file(phrase, filename):
    """ricava il numero della riga in cui compare una frase
    """
    with open(filename,encoding='utf8') as f:
        for (i, line) in enumerate(f):
            if phrase in line:
                return i
    return -1

def GetPhCommentList(textToSearch,l5xFile):

    # ricavo il numero della linea all'interno del file in inizia la struttura dei commenti
    lnum = line_num_for_phrase_in_file(textToSearch,l5xFile)

    with open(l5xFile,encoding='utf8') as f:
        # prendo un area dopo la parola in cui ragionevolmente ci sono tutte le fasi
        lineList = f.readlines()[lnum:lnum+100]
        
        # ricavo l'indice di dove finisce l'area dei commenti del rung
        commentIdx = lnum+100 #inizializzo per prova !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if '</Comment>\n' in lineList:
            commentIdx = lineList.index('</Comment>\n')

        return(lineList[0:commentIdx])



# leggo la lista dal file....ma non va bene...ci sono dei cazzilli!!!
with open('F:\SCRIPTING\XML_L5X\STC_NomiCicliProd.txt','r',encoding='utf-8') as fileCicli:
    ProdCycList = fileCicli.readlines()

for cycle in ProdCycList:
    textComp ='## D40_00.' + cycle.replace('\n','') + '.Phase - MESSAGE FOR HMI ##'
    comments = GetPhCommentList(textComp,PlcFile)
  
print(ord(text[10]))
print(ord(textComp[10]))

if text == textComp:
    print('uguali')
else:
    print('diversi')
    

# comments = GetPhCommentList(text,PlcFile)
print(comments)
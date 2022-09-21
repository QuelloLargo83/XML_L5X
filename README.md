![LastCommit](https://img.shields.io/github/last-commit/QuelloLargo83/XML_L5X)

## SCOPO

Automazione creazione files .ENG per HMI partendo la .L5X del progetto PLC RSLogix5000

## PREREQUISITI

```console
pip install l5x
```

La lettura del file .L5X è basata sul pacchetto [l5x](https://github.com/jvalenzuela/l5x)
testato sulla [Release_v1.5](Release_v1.5)

[README_l5x](https://github.com/jvalenzuela/l5x#readme)


### FUNZIONI
----------------------

1- IOMESSAGE

Prende la lista delle macchine esterne dal file `CFG_INI.ini` (da recuperare in superivisione)
e il file .L5X esportato dal plc e crea un file IOMESSAGE.ENG per ogni macchina

2- NOMI CICLI

Crea file con i nomi dei cicli (un file per i cicli di produzione e uno per i cicli Sterilizzazione/Sanificazione)


### DEBUG
-------

Per lanciare eventalmente il debug editare il file [launch.json](.vscode/launch.json) andando, per esempio, a modificare l'argomento con lo switch che interessa debuggare

### NOTE
-----

La funzione `CycleDesc` ha un parametro che indica il nome della struttura PhaseMsgInput e lo si trova nel plc guardando qui:

![phase](IMG/Phase.png)
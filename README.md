![pyversion](https://img.shields.io/badge/Python%20-3.10.3-green)

## SCOPO

Automazione creazione files .ENG per HMI partendo da `.L5X` del progetto PLC RSLogix5000

## ISTRUZIONI

prendere i seguenti files:

- `CFG_PAGE.ini` da supervisione 
- `IOMessages_PLXXXXX.ENG` da supervisione
- `SETUP_HMI.ini` da supervisione
- `Cycles.ini` da supervisione (da completare utilizzo)
- `****.L5X`        da PLC

1. Mettere i files presi dalla supervisione nella cartella `INI/HMI`
2. Mettere i files .L5X nella cartella `INI/PLC` dividendo filler e processo
3. Eventualmentente modificare [CyclesPhMsg.ini](./INI/CyclesPhMsg.ini)
4. Eventualmente modificare il file di configurazione


### Creare il virtual enviroment
```ps
	python -m venv venv
```
### Attivare il virtual enviroment
```ps
	.\venv\Scripts\Activate.ps1
```
### Installare le librerie necessarie
```ps
	pip install -r requirements.txt
```

### FUNZIONI
----------------------
Lanciare il programma senza switch per ottenere l'help

1 - IOMESSAGE

Prende la lista delle macchine esterne dal file `CFG_INI.ini` (da recuperare in supervisione)
e il file .L5X esportato dal plc e crea un file IOMESSAGE.ENG per ogni macchina

2 - NOMI CICLI

Crea file con i nomi dei cicli (un file per i cicli di produzione e uno per i cicli Sterilizzazione/Sanificazione)

3 - PHASES

Crea un file .ENG per ogni ciclo da esportare.
Il file viene generato con la seguente formattazione:

```INI
[CYCL_FIL_BaseRinsing_Phase]=Program:FILLER.D40_00.BaseRinsing.Phase
10= V; Machine Emptying
20= V; Cleaning
30= V; End Cycle

[CYCL_FIL_BaseRinsing_MSG]=Program:FILLER.D40_00.BaseRinsing.CycleMsg
1= V; - Waiting conditions ready to start cycle
2= V; - Cycle started
3= V; - Cycle running
4= V; - Cycle held
5= V; - Cycle failed
6= V; - Cycle done
7= V; - Waiting "Blow molder empty" signal active from ABF
8= V; - Waiting "Blow molder empty" signal active from SIPA
9= V; - Waiting "Blow molder empty" signal active from KHS
10= V; - Waiting "Sterile water ready" signal from Unitherm


[CYCL_FIL_BaseRinsing_PhaseMSG]=Program:FILLER.D40_00.BaseRinsing.PhaseMessage
1= V;Alarm condition active
2= V;Push machine start
3= V;Waiting Filler in rotation
4= V;Waiting for all active production cycles to end
5= V;Waiting Filler internal bottle counter at zero (Filler empty)
6= V;Valve 261VPW59 open
7= V;Valve CA1VPW06 open
8= V;Valve CA1VPB01 open
```
4 - TAGNAMELISTLANG

Creazione di file Tagnamelistlang per ogni plc prendendo i commenti dalle tag del plc

Esempio

```INI
[TAGNAMELISTLANG]
CONC_SH1_D61GAX01 = D61GAX01 H2O2 TRASMITER
CONC_SH1_D61MTX01 = D61MTX01 VHP CONCENTRATION (CALCOLATED) (PPM)
DGTA_SH1_D61LSX01 = D61LSX01 VAPORIZER CONDENSATE LEVEL
DGTA_SH1_D61PSK03 = D61PSK03 INLET COMMAND AIR LOW PRESSURE AFTER SAFETY VALVE (1 = LOW PRESSURE)
DGTA_SH1_D61TSK02 = D61TSK02 THERMAL OVERLOAD
DGTA_SH1_D61Y0101 = D61Y0101 CONTROL PHOTOCELL CAPS REQUEST CHANNEL 1
DGTA_SH1_D61Y0102 = D61Y0102 CONTROL PHOTOCELL CAPS REQUEST CHANNEL 2
DGTL_SH1_D61PSK01 = D61PSK01 INLET COMMAND AIR LOW PRESSURE BEFORE SAFETY VALVE (0 = LOW PRESSURE)
DGTL_SH1_D61PSK08 = D61PSK08 TREATMENT PRESSURE LOW (1=OK)
DGTL_SH1_D61PSV01 = D61PSV01 STEAM PRESSURE LOW (1=OK)
DGTL_SH1_D61Y0101 = D61Y0101 CHANNEL 1 CAPS LEVEL IN CAP SORTER (1=REQUEST)
DGTL_SH1_D61Y0102 = D61Y0102 CHANNEL 2 CAPS LEVEL IN CAP SORTER (1=REQUEST)
DGTL_SH1_D61Y0201 = D61Y0201 CONTROL PHOTOCELL CHANNEL 1 STOP CAPS SORTER
DGTL_SH1_D61Y0202 = D61Y0202 CONTROL PHOTOCELL CHANNEL 2 STOP CAPS SORTER
DGTL_SH1_D61Y0301 = D61Y0301 CONTROL PHOTOCELL CHANNEL 1 READY START TREATMENT
DGTL_SH1_D61Y0302 = D61Y0302 CONTROL PHOTOCELL CHANNEL 2 READY START TREATMENT
DGTL_SH1_D61Y0401 = D61Y0401 SENSOR STARWHEEL CHANNEL 1
```

### DEBUG
-------

Per lanciare eventalmente il debug editare il file [launch.json](.vscode/launch.json) andando, per esempio, a modificare l'argomento con lo switch che interessa debuggare

### NOTE
-----

La funzione `CycleDesc` ha un parametro che indica il nome della struttura PhaseMsgInput e lo si trova nel plc guardando qui:

<!-- ![phase](IMG/Phase.png) -->

<p align="center">
<img src="IMG/Phase.png"  width=50% height=50%>
</p>

## PREREQUISITI

La lettura del file .L5X è basata sul pacchetto [l5x](https://github.com/jvalenzuela/l5x)
testato sulla [Release_v1.5](Release_v1.5)

[README_l5x](https://github.com/jvalenzuela/l5x#readme)

## SVILUPPI E CONSIDERAZIONI

- Quando la variabile a PLC non corrisponde a SignalFILfrom_MAC_ viene gestito a sw 
  una sezione per segnali di scambio non ordinari:
	es:
	
       - `CFT` indica cio che su PLC è `BFT`
	   - `UTH` ha `SignalUTHToFIL` e `SignalFILToPRO.UTH`

- [x] Fare in modo che compili sempre SX1--SX28 e DX1 --- DX28 anche se ci sono spazi vuoti

- [x] gestire per le Analogiche la parte finale con [TIPO]..K[n]   esempio ..TIMS..K100

- [x] i segnali di scambio delle macchine sono un po' in CFG_PAGE.ini e un po' in IOMESSAGES.ENG
      cercare di unirli in modo furbo

- [ ] gestire il titolo della della parte sx con nomi sensati

- [x] gestire la tilde (~) davanti ad alcuni strumenti (es: ~CA1PTK51)

- [ ] il phaseMsgInput di SH1 ha un problema nel plc: la struttura PhaseMessageInput si chiama MessageInput...prevedere questa eccezione!!!

- [ ] HEPA1 non trova i commenti PhaseMsgInput ma ci sono (sono con _SVHP ma ci sono e ho provato mettendo _SVHP nel file CyclePhMsg.ini )

- [ ] fnz.CycleDesc: nella parte cyclemsg prendere anche gli eventuali a capo (esempio ciclo uht production prende solo la prima riga del commento)
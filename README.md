# EV3 - BTTRC (BackToTheRootsCommunication)

Morsecode und Drucker für den EV3 Mindstorms mit ev3dev. Der Morsecode wird via Internet zum Gesprächspartner gesendet und die Nachrichten des Partners werden via Internet zurück an den Drucker geleitet und gedruckt.

## Setup

In beiden Setups sollte die Umgebungsvariable "EV3_CHATKEY" vorhanden sein, welche in beiden Fällen den gleichen Wert haben sollte.
Dazu kann am Besten im Ordner `/home/robot/ev3-bttrc` eine Datei mit dem Namen `.env` und dem Inhalt `EV3_CHATKEY=*` erstellt werden, wobei * mit einer beliebigen Zahlen- oder Buchstabenfolge ersetzt werden sollte.

### EV3 Setup

```bash
cd /home/robot
mkdir /home/robot/ev3-bttrc
cd ev3-bttrc
mkdir /home/robot/ev3-bttrc/bttrc
wget -O bttrc_update.sh https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc_update.sh
sudo chmod +x bttrc_update.sh
sudo ./bttrc_update.sh
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install requests
```

Zum Starten:

Folgenden Command eingeben oder via Brickman starten.

```bash
brickrun -r --directory="/home/robot/ev3-bttrc" "/home/robot/ev3-bttrc/bttrc_ev3.py"
```

Hinweis: Die letzten drei Commands könnten **sehr** lange dauern, die ist jedoch normal.

### PC Setup

1. Datei "bttrc_pc.py" herunterladen.
2. Python 3.8 installieren
3. Datei ausführen.

## Benutzung

### Kalibrierung

1. Druckkopf nach ganz oben heben (dazu zuerst das Zahnrad hinten links vom Motor lösen, dann der Druckkopf heben und das Zahnrad wieder einrasten).
2. Stift in die Halterung einspannen.
3. `ev3-bttrc/bttrc_calibrate.py` Programm starten
4. Sobald das Programm gestartet ist, bewegt sich der Druckkopf nach unten links.
5. Anschliessend kann mit den Pfeiltasten nach oben/unten der Druckkopf gehoben/gesunken werden.
6. Sobald die gewünschte Höhe erreicht wurde, kann mit der mittleren Taste die Konfiguration abgeschlossen werden.

### Bedienung

1. Falls noch nicht abgeschlossen, Kalibrierung ausführen (siehe [Kalibrierung](#kalibrierung))
2. Programm `ev3-bttrc/bttrc_ev3.py` starten.
3. Programm mit den Tasten steuern (siehe [Tasten](#tasten))

### Tasten

Hinweis: Manche Tasten müssen evtl. bis zu einer Sekunde gedrückt gehalten werden. Auch sind manche Funktionen während eines Druckvorgangs nicht verfügbar.

- Nach oben
  - Wenn kein Papier eingelegt: Papier einziehen
  - Wenn Papier eingelegt: Neue Zeile
- Nach unten
  - Wenn Papier eingelegt: Papier ausgeben
- Nach rechts
  - Wenn Ton abgespielt wird: Aktuelle Tondatei stoppen
- Nach links
  - Programm beenden (Bitte nur ausführen, wenn aktuell kein Papier eingelegt ist, denn dann ist die korrekte Stiftposition garantiert.)

# EV3 - BTTRC (BackToTheRootsCommunication)

Morsecode und Drucker für den EV3 Mindstorms mit ev3dev. Der Morsecode wird via Internet zum Gesprächspartner gesendet und die Nachrichten des Partners werden via Internet zurück an den Drucker geleitet und gedruckt.

Bauanleitung und Kalibration funktionieren gleich wie beim [Original von JKBrickWorks](https://jkbrickworks.com/telegraph-machine-and-printer#1701).

## Setup

### EV3 Setup

Auf dem EV3 muss die Umgebungsvariable "EV3_CHATKEY" vorhanden sein.
Dazu kann am Besten im Ordner `/home/robot/ev3-bttrc` eine Datei mit dem Namen `.env` und dem Inhalt `EV3_CHATKEY=*` erstellt werden, wobei \* mit einer beliebigen Zahlen- oder Buchstabenfolge ersetzt werden muss.

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

Die Programme können anschliessend via Brickman gestartet werden.

Hinweis: Die letzten drei Commands könnten **sehr** lange dauern, die ist jedoch normal.

### Chatpartner Setup

Folgende Webseite öffnen, wobei `CHATKEY` mit dem beim EV3 gespeicherten Chatkey ausgetauscht werden sollte: <https://rafaelurben.herokuapp.com/onlinevars/chat/CHATKEY_toEV3/CHATKEY_fromEV3>

## Benutzung

### Kalibrierung

1.  Druckkopf nach ganz oben heben (dazu zuerst das Zahnrad hinten links vom Motor lösen, dann der Druckkopf heben und das Zahnrad wieder einrasten).
2.  Stift in die Halterung einspannen.
3.  Programm `ev3-bttrc/bttrc_calibrate.py` starten
4.  Sobald das Programm gestartet ist, bewegt sich der Druckkopf nach unten links.
5.  Anschliessend kann mit den Pfeiltasten nach oben/unten der Druckkopf gehoben/gesunken werden.
6.  Sobald die gewünschte Höhe erreicht wurde, kann mit der mittleren Taste die Konfiguration abgeschlossen werden.

### Bedienung

1.  Falls noch nicht abgeschlossen, Kalibrierung ausführen (siehe [Kalibrierung](#kalibrierung))
2.  Programm `ev3-bttrc/bttrc_ev3.py` starten.
3.  Programm mit den Tasten steuern (siehe [Tasten](#tasten))

### Tasten

Hinweis: Manche Tasten müssen evtl. bis zu einer Sekunde gedrückt gehalten werden. Auch sind manche Funktionen während eines Druckvorgangs nicht verfügbar.

| Taste       | Bedingung             | Funktion         |
| ----------- | --------------------- | ---------------- |
| Nach oben   | Kein Papier eingelegt | Papier einziehen |
| Nach oben   | Papier eingelegt      | Neue Zeile       |
| Nach unten  | Papier eingelegt      | Papier ausgeben  |
| Nach rechts | Ton wird abgespielt   | Audio stoppen    |
| Nach links  | -                     | Programm beenden |

Letzteres bitte nur ausführen, wenn aktuell kein Papier eingelegt ist, denn dann ist die korrekte Stiftposition garantiert und der Ev3 muss nicht erneut kalibiriert werden.

### Feedback

Morsecode

| Linke Lampe | Sound  | Bedeutung               |
| ----------- | ------ | ----------------------- |
| Rot         | Beeeep | Abbruch                 |
| Rot         | 5 Beep | Fehler                  |
| Grün        | 1 Beep | Charakter erkannt       |
| Grün        | 2 Beep | Leerzeichen hinzugefügt |
| Grün        | 3 Beep | Wort gelöscht           |
| Grün        | 4 Beep | Nachricht beendet       |
| Gelb        | -      | In Bereitschaft         |
| Orange      | -      | Taste gedrückt          |

Drucker

| Rechte Lampe | Bedeutung           |
| ------------ | ------------------- |
| Rot          | Fehler              |
| Grün         | In Bereitschaft     |
| Gelb         | Arbeitet...         |
| Orange       | Warte auf Papier... |

### Morsecode

Morsecode-Zeichen:

| Text       | Morsecode |
| ---------- | --------- |
| A          | .-        |
| B          | -...      |
| C          | -.-.      |
| D          | -..       |
| E          | .         |
| F          | ..-.      |
| G          | --.       |
| H          | ....      |
| I          | ..        |
| J          | .---      |
| K          | -.-       |
| L          | .-..      |
| M          | --        |
| N          | -.        |
| O          | ---       |
| P          | .--.      |
| Q          | --.-      |
| R          | .-.       |
| S          | ...       |
| T          | -         |
| U          | ..-       |
| V          | ...-      |
| W          | .--       |
| X          | -..-      |
| Y          | -.--      |
| Z          | --..      |
|            |           |
| Ä          | .-.-      |
| Ö          | ---.      |
| Ü          | ..--      |
|            |           |
| 1          | .----     |
| 2          | ..---     |
| 3          | ...--     |
| 4          | ....-     |
| 5          | .....     |
| 6          | -....     |
| 7          | --...     |
| 8          | ---..     |
| 9          | ----.     |
| 0          | -----     |
|            |           |
| :          | --..--    |
| .          | .-.-.-    |
|            |           |
| :          | ---...    |
| '          | .----.    |
| "          | -.--.-    |
|            |           |
| ?          | ..--..    |
| /          | -..-.     |
| -          | -....-    |
|            |           |
| @          | .--.-.    |
| =          | -...-     |
| &          | .-...     |
|            |           |
| (          | -.--.     |
| )          | -.--.-    |
| !          | -.-.--    |
|            |           |
| UNDERSTOOD | ...-.     |

Spezielle Befehle:

| Command              | Morsecode         |
| -------------------- | ----------------- |
| Nachricht senden     | .-.-. oder ...-.- |
| Letztes Wort löschen | ........  (8)     |
| Buchstabe abbrechen  | Gedrückt halten   |

### Chatpartner Commands

Der Chatpartner kann in Nachrichten folgende Befehle verwenden:

| Command            | Aufgabe                  |
| ------------------ | ------------------------ |
| //NEWLINE//        | Zeilenumschlag ausführen |
| //FEEDOUT//        | Papier ausgeben          |
| //SOUND:filename// | Tondatei abspielen       |
| //STOPSOUND//      | Tondatei beenden         |
| //NOPRINT//        | Nachricht nicht drucken  |

Hinweis: Bei Sound die Dateiendung (.wav) weglassen!

# Geschichte

Dieses Projekt ist im Rahmen eines Schulprojekts von [Matthew Haldimann](https://github.com/nightmare23h/) und [Rafael Urben](https://rafaelurben.github.io/diverses/rafaelurben/) entstanden.

# EV3 - BTTRC (BackToTheRootsCommunication)

In beiden Setups sollte die Umgebungsvariable "EV3_CHATKEY" vorhanden sein, welche in beiden Fällen den gleichen Wert haben sollte.

## EV3 Setup

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

```bash
cd /home/robot/ev3-bttrc
brickrun -r --directory="/home/robot/ev3-bttrc" "/home/robot/ev3-bttrc/bttrc_ev3.py"
```

Hinweis: Die letzten drei Commands könnten **sehr** lange dauern, die ist jedoch normal.

## PC Setup

1. Datei "bttrc_pc.py" herunterladen.
2. Python 3.8 installieren
3. Datei ausführen.

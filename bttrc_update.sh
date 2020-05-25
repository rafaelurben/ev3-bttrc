#!/bin/bash
#
# Update ausführen

cd ~
mkdir bttrc


echo "Update gestartet!"


echo "Update: Dateien von GitHub herunterladen..."
wget -q -O bttrc_ev3.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc_ev3.py
wget -q -O bttrc_update.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc_update.py

cd bttrc

wget -q -O __init__.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc/__init__.py
wget -q -O calibrate_printer.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc/calibrate_printer.py
wget -q -O chat.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc/chat.py
wget -q -O morse.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc/morse.py
wget -q -O printer.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc/printer.py


cd ../


echo "Update: Dateien ausführbar machen..."
sudo chmod +x bttrc_ev3.py
sudo chmod +x bttrc_update.py

cd bttrc

sudo chmod +x __init__.py
sudo chmod +x calibrate_printer.py
sudo chmod +x chat.py
sudo chmod +x morse.py
sudo chmod +x printer.py


echo "Update beendet!"

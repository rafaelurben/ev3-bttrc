#!/bin/bash
#
# Back To The Roots Communication
#
# 2020 - Rafael Urben (github.com/rafaelurben)
#
# Update ausführen

mkdir -p /home/robot/ev3-bttrc
mkdir -p /home/robot/ev3-bttrc/bttrc
cd /home/robot/ev3-bttrc


echo "Update gestartet!"


echo "Update: Dateien von GitHub herunterladen..."
wget -O bttrc_ev3.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc_ev3.py
wget -O bttrc_update.sh https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc_update.sh
wget -O bttrc_calibrate.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc_calibrate.py


cd bttrc

wget -O __init__.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc/__init__.py
wget -O chat.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc/chat.py
wget -O morse.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc/morse.py
wget -O printer.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc/printer.py


cd ../


echo "Update: Dateien ausführbar machen..."
sudo chmod +x bttrc_ev3.py
sudo chmod +x bttrc_update.py
sudo chmod +x bttrc_calibrate.py

cd bttrc

sudo chmod +x __init__.py
sudo chmod +x chat.py
sudo chmod +x morse.py
sudo chmod +x printer.py


echo "Update beendet!"

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
wget -q -O bttrc_ev3.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc_ev3.py
wget -q -O bttrc_update.sh https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc_update.sh
wget -q -O bttrc_calibrate.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc_calibrate.py


cd bttrc

wget -q -O __init__.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc/__init__.py
wget -q -O chat.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc/chat.py
wget -q -O morse.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc/morse.py
wget -q -O printer.py https://raw.githubusercontent.com/rafaelurben/ev3-bttrc/master/bttrc/printer.py


cd ../


echo "Update: Dateien ausführbar machen..."
chmod +x bttrc_ev3.py
chmod +x bttrc_update.sh
chmod +x bttrc_calibrate.py

cd bttrc

chmod +x __init__.py
chmod +x chat.py
chmod +x morse.py
chmod +x printer.py


echo "Update beendet!"

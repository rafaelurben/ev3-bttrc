# EV3 - BTTRC (BackToTheRootsCommunication)

Setup:

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

Hinweis: Die letzten drei Commands könnten **sehr** lange dauern, die ist jedoch normal.

# HardHack

Repo for 2020 HardHack

Team member: Nimish, Oliver, Roy, Ben

We implemented a python project that parses the data via a serial com from arduino. 
The Arduino servers as a analog data collector for the ultrosonic sensor and the Raspberry pi, using Python script,
parses the data and sort it accordingly. 

## Installation
```
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install arduino
sudo apt install python3
git clone https://github.com/chychiang/HardHack
cd /HardHack
python serial_test.py
```

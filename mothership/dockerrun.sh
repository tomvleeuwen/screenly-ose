#!/bin/bash

cd mothership
screen -dm python mothership.py 9000
cd ..
screen -dm python beacon.py
python server.py

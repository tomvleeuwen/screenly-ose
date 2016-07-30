#!/bin/bash

cd mothership
screen -dm python mothership.py 9000
cd ..
python server.py

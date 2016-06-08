#!/bin/bash

experiment-cli -u theoleyr -p x9HBHvm8 stop

sudo killall /usr/bin/python > /dev/null 2> /dev/null
sudo killall socat > /dev/null 2> /dev/null
sudo killall ssh > /dev/null 2> /dev/null
sudo killall sleep > /dev/null 2> /dev/null


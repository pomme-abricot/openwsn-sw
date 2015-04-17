#!/bin/bash

for pid in `ps -ef | tr -s " " | grep openV | cut -d " " -f2`
do
	sudo kill -9 $pid
done

for pid in `ps -ef | tr -s " " | grep scons | cut -d " " -f2`
do
	sudo kill -9 $pid
done


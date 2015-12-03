#!/bin/bash

exit


for f in `ls *$1*.graph`
do
	file=`echo $f|sed 's/\(.*\)\.graph/\1/'`
	echo $file
	gnuplot < $file.graph > $file.eps
	epstopdf $file.eps
	rm $file.eps
done

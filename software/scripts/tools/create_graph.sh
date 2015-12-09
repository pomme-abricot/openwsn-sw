#!/bin/bash


#does it exist a .graph script?
#echo "ls *$1*.graph l 2> /dev/null"
RES=`ls *$1*.graph  2> /dev/null`
if [ -z "$RES" ]
then
	echo "no graph to generate"
	exit
fi


for f in `ls *$1*.graph`
do
	file=`echo $f|sed 's/\(.*\)\.graph/\1/'`
	echo $file
	gnuplot < $file.graph > $file.eps
	epstopdf $file.eps
	rm $file.eps
done

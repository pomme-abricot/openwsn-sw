#!/bin/bash

CUR_DIR=`pwd -P`
echo $CUR_DIR


ASN_MIN=1000
ASN_AGG=1000


for dir in */*
do
	#echo "DIRECTORy $dir"
	if [ -e "$dir/openVisualizer.log" ]
	then
		echo "handling $dir/openVisualizer.log"
		if [ -e "$dir/results.csv" ]
		then 
			echo "removes previous $dir/results.csv"
			rm $dir/results.csv
		fi
        cd $dir
		owsn_extract_stats_from_log.sh $ASN_MIN $ASN_AGG openVisualizer.log >/dev/null
		cd $CUR_DIR
	fi
done


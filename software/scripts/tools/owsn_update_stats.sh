#!/bin/bash



ASN_MIN=1000
ASN_AGG=1000


for dir in */*
do
	#echo "DIRECTORy $dir"
		if [ -e "$dir/openVisualizer.log" ]
	then
		echo "handling $dir/openVisualizer.log"
		cd $dir 
		if [ -e "results.csv" ]
		then 
			echo "removes previous results.csv"
			rm results.csv
		fi
		owsn_extract_stats_from_log.sh $ASN_MIN $ASN_AGG openVisualizer.log >/dev/null
	fi
done


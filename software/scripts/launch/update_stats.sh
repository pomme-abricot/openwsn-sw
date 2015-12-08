#!/bin/bash



ASN_MIN=1000
ASN_AGG=1000


for DIRS in "$@"
do
	for dir in $DIRS/*/*
	do
		echo "DIRECTORy $dir"

		if [ -e "$dir/openVisualizer.log" ]
		then
			echo "handling $dir/openVisualizer.log"
			cd $dir 
			if [ -e "results.csv" ]
			then 
				echo "removes previous results.csv"
				rm results.csv
			fi
			compute_stats.sh $ASN_MIN $ASN_AGG openVisualizer.log

		fi
	done
done

#!/bin/bash

#default
CUR_DIR=`pwd`
#the international units
LANG=
echo $#

if [ $# -ne 0 ]
then
	FILEWILDCARD="*"$1"*.cf"
else
	FILEWILDCARD="*.cf"
fi

#for each configuration file present in the current directory
for FILE_CONFIG in $FILEWILDCARD
do

	#basename
	BASENAME=`cat $FILE_CONFIG | grep BASENAME | cut -d "|" -f 2`

	#paramters
    SCHEDALGO_LIST=`cat $FILE_CONFIG | grep SCHEDALGO_LIST | cut -d "|" -f 2`
    RPLMETRIC_LIST=`cat $FILE_CONFIG | grep RPLMETRIC_LIST | cut -d "|" -f 2`
    DISTRCELLS_LIST=`cat $FILE_CONFIG | grep DISTRCELLS_LIST | cut -d "|" -f 2`
    TRACK_LIST=`cat $FILE_CONFIG | grep TRACK_LIST | cut -d "|" -f 2`
    NB_FIXED_COLS=`cat $FILE_CONFIG | grep NB_FIXED_COLS | cut -d "|" -f 2`
	
	#go to the correct directory
	DIR="$CUR_DIR/../$BASENAME/data"
	#DIRS_IN_LIST=`cat $FILE_CONFIG | grep DIRS_IN_LIST | cut -d "|" -f 2`

	#The column id for the x-coordinate of the graph (i.e. the parameter)
	X_COORD_POS=`cat $FILE_CONFIG | grep X_COORD_POS | cut -d "|" -f 2`

	#Nb of columns (discard lines with less or more values)
	NB_OF_COLS=`cat $FILE_CONFIG | grep NB_OF_COLS | cut -d "|" -f 2`

    for SCHEDALGO in $SCHEDALGO_LIST
    do
        for RPLMETRIC in $RPLMETRIC_LIST
        do
        	for TRACKS in $TRACK_LIST
        	do
	       	 	for DISTRCELLS in $DISTRCELLS_LIST
	        	do    
	        		#Variables
					HEAD=""    	
	        	
            		#parameters
            		FILE_OUT_AGGREGATED="$DIR/distribshared="$DISTRCELLS"-tracks="$TRACKS"-rplmetric="$RPLMETRIC"-schedalgo="$SCHEDALGO".txt"
           			FILE_OUT_SORTED="$DIR/../distribshared="$DISTRCELLS"-tracks="$TRACKS"-rplmetric="$RPLMETRIC"--schedalgo="$SCHEDALGO".txt"
		           	rm -f $FILE_OUT_SORTED
           			rm -f $FILE_OUT_AGGREGATED
		
					echo "Handling directory $DIR/distribshared=$DISTRCELLS,tracks=$TRACKS,rplmetric=$RPLMETRIC,schedalgo=$SCHEDALGO*/*"
		
					for exp in $DIR/distribshared=$DISTRCELLS,tracks=$TRACKS,rplmetric=$RPLMETRIC,schedalgo=$SCHEDALGO*/*
					do
						if [ ! -e $exp/results.csv ]
						then
							break
						fi
						
						#echo $exp

						#field names (only done once), and flushes the previous content (> and not >>)
						#if [ -z "$HEAD" ]
						#then
						#	HEAD=`cat $exp/results.csv | head -n 1`
						#	echo "$HEAD" > $FILE_OUT_AGGREGATED 
						#	echo "$HEAD"
						#fi

						#extracts the last line from each file (the stats without the field names)
						LINE=`cat $exp/results.csv | tail -n 1`
						echo "$LINE" >> $FILE_OUT_AGGREGATED 
						echo "$LINE"
	        		done
	        		
	        		
	              	#generates the data (directly used by gnuplot scripts)
	           		echo "cat $FILE_OUT_AGGREGATED | grep -v inf | gawk -f first_col_move.awk -v COL_PARAM=$X_COORD_POS | sort -n | gawk -f compute_avg_and_confidence_intervals.awk -v NB_OF_COLS=$NB_OF_COLS -v NB_FIXED_COLS=$NB_FIXED_COLS > $FILE_OUT_SORTED"
					cat $FILE_OUT_AGGREGATED | grep -v "inf" | gawk -f first_col_move.awk -v COL_PARAM=$X_COORD_POS | sort -n | gawk -f compute_avg_and_confidence_intervals.awk -v NB_OF_COLS=$NB_OF_COLS -v NB_FIXED_COLS=$NB_FIXED_COLS > $FILE_OUT_SORTED
	
					#raw data for debug
					#cat $FILE_OUT_AGGREGATED | grep -v "inf" | gawk -f first_col_move.awk -v COL_PARAM=$X_COORD_POS | sort -n > $FILE_OUT_SORTED
	
					#flush
					echo ""
	        		
				done
	        done
        done
	done
done
	
	
	


#returns to the previous position
cd $CUR_DIR




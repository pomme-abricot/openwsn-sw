#!/bin/bash

#converts a long address (8 bytes) into a short one (2 bytes)
function addr_long_to_short {
	result=${1:12:4}
}


#bug if more than 2 arguments, and less than 1
if [ $# -gt 2 ] || [ $# -lt 1 ]
then
    echo "usage: $0 asn_min [logfile]"
    exit 2
fi 


#constants
TABFILE="results.csv"
TIMESLOT_DURATION=15	# in milliseconds
RATIO_PK_RX=0.7			# at least this ratio of pk has to be transmitted to consider this source (else it probably crashed during the experiment)
ASN_MIN=$1
MAX_NB_PK_TX=0 			# initialization
if [ $# -eq 1 ]
then
	LOGFILE="/home/theoleyre/exp-iotlab/openwsn/openwsn-sw/software/openvisualizer/build/runui/openVisualizer.log";
else
	LOGFILE=$2;
fi

echo "Handling logfile $LOGFILE"
if [ ! -f $LOGFILE ]
then
	echo "File '$LOGFILE' doesn't exist"
	exit 3
fi


#Temporary files
TMPFILE=`mktemp` || exit 1
NODESLIST=`mktemp` || exit 1
TMPGEN=`mktemp` || exit 1
TMPRX=`mktemp` || exit 1


grep STAT_DATARX $LOGFILE | cut -d "|" -f 9 | cut -d "=" -f 2 > $TMPFILE

#get the node list
sort -u $TMPFILE > $NODESLIST
NBNODES=`wc -l $NODESLIST | cut -d " " -f 1` 
#echo "$NBNODES nodes (+dagroot)"

index=0

#get the list of seqnums for each source
for addr_l in `cat $NODESLIST` 
do
    #converts the long address (64B) into a short one (16B)
	addr_long_to_short $addr_l
	addr_s=$result

	echo "node $addr_s: ($addr_l)"

    #nb of packets received
    array_addrs[$index]=$addr_s
    array_pkrx[$index]=0
    array_pktx[$index]=0
    array_delay[$index]=0
    array_pkdup[$index]=0
    
    #prepare the stats for this node
    cat $LOGFILE | grep STAT_DATAGEN | grep "l2Src=$addr_l" > $TMPGEN
    cat $LOGFILE | grep STAT_DATARX | grep "l2Src=$addr_l" > $TMPRX

    #get the list of seqnum generated
    SEQNUMS=`cat $TMPGEN | cut -d "|" -f 8 | cut -d "=" -f 2` 
    for seqnum in $SEQNUMS
    do
        
        #ASNs picked in the logs
        ASN_TX=`cat $TMPGEN | grep "seqnum=$seqnum" | cut -d "|" -f 4 | cut -d "=" -f 2`
        ASN_RX=`cat $TMPRX | grep "seqnum=$seqnum" | cut -d "|" -f 4 | cut -d "=" -f 2`
       
        #discard this packet when this sequence number was txed several times
        eval ASN_TX_ARRAY=($ASN_TX)
        if [ ${#ASN_TX_ARRAY[@]} -gt 1 ]
        then
           ASN_TX=0
        fi

        #I only consider the packets after the bootstrap period
        if [ "$ASN_TX" -gt "$ASN_MIN" ]
        then

            #nb of packets generated
            (( array_pktx[index]++ ))

            #the packet was received: lets' increase the delay
            if [ -n "$ASN_RX" ] 
            then

                #search for duplicates, and keep only the first reception
                eval ASN_RX_ARRAY=($ASN_RX)
                if [ ${#ASN_RX_ARRAY[@]} -gt 1 ]
                then
                    #echo "duplicate"
                    ASN_RX=${ASN_RX_ARRAY[0]}
                    (( array_pkdup[index]++ ))
                fi
            
                #echo "|$ASN_RX| - |$ASN_TX|"

                #compute the delay (in ASN)
                hop_delay=`echo "$ASN_RX - $ASN_TX" | bc -l` 
                array_delay[$index]=`echo "${array_delay[$index]} + $hop_delay" | bc -l` 
           
                #nb of received packets
                (( array_pkrx[index]++ ))

                #bug
                if [ "$hop_delay" -le "0" ]
                then
                    echo "ERROR  - negative delay for one hop"
                    exit
                fi
            fi
        fi

    done

    #remove temporary files
    rm $TMPRX
    rm $TMPGEN

    #prints the stats
    echo "nb_pk_tx[$addr_s]=${array_pktx[$index]}"
    echo "nb_pk_rx[$addr_s]=${array_pkrx[$index]}"
    echo "dupratio_data[$addr_s]=`echo "${array_pkdup[$index]} / ${array_pkrx[$index]}" | bc -l`"
    echo "pdr_data[$addr_s]=`echo "${array_pkrx[$index]} / ${array_pktx[$index]}" | bc -l`"
    echo "avg_delay(ASN)[$addr_s]=`echo "${array_delay[$index]} / ${array_pkrx[$index]}" | bc -l`"
    echo "avg_delay(ms)[$addr_s]=`echo "${array_delay[$index]} / ${array_pkrx[$index]} * 15" | bc -l`"
    echo "----------"

	#remember the max nb. of pkts txed
	if [ "$MAX_NB_PK_TX" -eq "0" ] || [ "${array_pktx[$index]}" -ge "$MAX_NB_PK_TX" ]
	then
		MAX_NB_PK_TX=${array_pktx[$index]}
	fi

    #next node to consider
    (( index++ ))
done


#compute the average stats
global_nbnodes=0
global_pktx=0
global_pkrx=0
global_pkdup=0
global_delay=0
global_jain_pdr=0
global_pdr_avg=0
NB_PKGEN_MIN=`echo "scale=0;$MAX_NB_PK_TX * $RATIO_PK_RX / 1" | bc`
NB_NODES_DISCARDED=0
#tmp values
sum_pdr=0
sum_delay=0
sum2_pdr=0
sum2_delay=0
for i in ${!array_pktx[*]} 
do
    if [ ${array_pktx[$i]} -gt $NB_PKGEN_MIN ]
    then
        (( global_nbnodes++ ))
        global_pktx=`echo "$global_pktx +  ${array_pktx[$i]}" | bc`
        global_pkrx=`echo "$global_pkrx +  ${array_pkrx[$i]}" | bc`
        global_pkdup=`echo "$global_pkdup +  ${array_pkdup[$i]}" | bc`
        global_delay=`echo "$global_delay +  ${array_delay[$i]}" | bc`
           
        #jain indexes
      	sum_pdr=`echo "$sum_pdr + ${array_pkrx[$i]} / ${array_pktx[$i]}" | bc -l`
   		sum2_pdr=`echo "$sum2_pdr + (${array_pkrx[$i]} / ${array_pktx[$i]})^2" | bc -l`
    	sum_delay=`echo "$sum_delay + ${array_delay[$i]} / ${array_pkrx[$i]}" | bc -l`
    	sum2_delay=`echo "$sum2_delay + (${array_delay[$i]} / ${array_pkrx[$i]})^2" | bc -l`
        
          
    else
    	((NB_NODES_DISCARDED=NB_NODES_DISCARDED+1))
    fi
done

#avg values for all the flows
global_pdr_avg=`echo "$global_pkrx / $global_pktx"| bc -l`
global_delay_avg=`echo "$global_delay / $global_pkrx"| bc -l`
global_jain_pdr=`echo "($sum_pdr)^2 / ($sum2_pdr * $global_nbnodes)"| bc -l`
global_jain_delay=`echo "($sum_delay)^2 / ($sum2_delay * $global_nbnodes)"| bc -l`
global_dupratio=`echo "$global_pkdup / ($global_pkrx * $global_nbnodes)"| bc -l`


echo "--------AVG--------"
echo "nb_nodes=$global_nbnodes"
echo "nb_pk_tx_significant=$NB_PKGEN_MIN"
echo "nb_nodes_discarded=$NB_NODES_DISCARDED"
echo "nb_pk_tx[avg]=`echo "$global_pktx / $global_nbnodes"| bc -l`"
echo "nb_pk_rx[avg]=`echo "$global_pkrx / $global_nbnodes"| bc -l`"
echo "dupuratio_data[avg]=$global_dupratio"
echo "pdr_data[avg]=$global_pdr_avg" 
echo "jain_pdr=$global_jain_pdr"
echo "avg_delay(ASN)[avg]=$global_delay_avg"
echo "avg_delay(ms)[avg]=`echo "$global_delay * $TIMESLOT_DURATION / $global_pkrx"| bc -l`"
echo "jain_delay=$global_jain_delay"
echo "-------------------"


if [ ! -f $TABFILE ]
then
	echo "nb_nodes	nb_pk_tx_significant	nb_nodes_discarded	nb_pk_tx	nb_pk_rx	dupuratio_data	pdr_data	jain_pdr	avg_delay(ASN)	avg_delay(ms)	jain_delay" > $TABFILE
fi

echo "$global_nbnodes	$NB_PKGEN_MIN	$NB_NODES_DISCARDED	`echo "$global_pktx / $global_nbnodes"| bc -l`	`echo "$global_pkrx / $global_nbnodes"| bc -l`	$global_dupratio	$global_pdr_avg	$global_jain_pdr	$global_delay_avg	`echo "$global_delay * $TIMESLOT_DURATION / $global_pkrx"| bc -l`	$global_jain_delay" >> $TABFILE






rm $TMPFILE
rm $NODESLIST
#!/bin/bash

#converts a long address (8 bytes) into a short one (2 bytes)
function addr_long_to_short {
#	return ${1:12:4}
	result=${1:12:4}

}


#constants
TIMESLOT_DURATION=15
THRESHOLD_NB_PKTX=0.8   #if a node generates XX% packets less than the other ones (avg), do not consider it (it crashed probably)    


#Temporary files
TMPFILE=`mktemp` || exit 1
NODESLIST=`mktemp` || exit 1
TMPGEN=`mktemp` || exit 1
TMPRX=`mktemp` || exit 1


grep STAT_DATARX $1 | cut -d "|" -f 9 | cut -d "=" -f 2 > $TMPFILE

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

	#echo "node $addr_s: ($addr_l)"

    #nb of packets received
    array_addrs[$index]=$addr_s
    array_pkrx[$index]=0
    array_pktx[$index]=0
    array_delay[$index]=0
    array_pkdup[$index]=0
    
    #prepare the stats for this node
    cat $1 | grep STAT_DATAGEN | grep "l2Src=$addr_l" > $TMPGEN
    cat $1 | grep STAT_DATARX | grep "l2Src=$addr_l" > $TMPRX

    #get the list of seqnum generated
    SEQNUMS=`cat $TMPGEN | cut -d "|" -f 8 | cut -d "=" -f 2` 
    for seqnum in $SEQNUMS
    do
        
        #ASNs picked in the logs
        ASN_TX=`cat $TMPGEN | grep "seqnum=$seqnum" | cut -d "|" -f 4 | cut -d "=" -f 2`
        ASN_RX=`cat $TMPRX | grep "seqnum=$seqnum" | cut -d "|" -f 4 | cut -d "=" -f 2`

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

    done

    #remove temporary files
    rm $TMPRX
    rm $TMPGEN

    #prints the stats
    echo "nb_pk_tx[$addr_s]=${array_pktx[$index]}"
    echo "nb_pk_rx[$addr_s]=${array_pkrx[$index]}"
    echo "ratio_duplicates[$addr_s]=`echo "${array_pkdup[$index]} / ${array_pkrx[$index]}" | bc -l`"
    echo "pdr[$addr_s]=`echo "${array_pkrx[$index]} / ${array_pktx[$index]}" | bc -l`"
    echo "avg_delay(ASN)[$addr_s]=`echo "${array_delay[$index]} / ${array_pkrx[$index]}" | bc -l`"
    echo "avg_delay(ms)[$addr_s]=`echo "${array_delay[$index]} / ${array_pkrx[$index]} * 15" | bc -l`"
    echo "----------"

    #next node to consider
    (( index++ ))
done


#computes the threshold value to detect crashed nodes (i.e. minimum number of transmitted packets)
global_pktx=0
nbnodes=0
for i in ${!array_pktx[*]} 
do
    global_pktx=`echo "$global_pktx + ${array_pktx[$i]}" | bc`
    (( nbnodes++ ))
done 
threshold=`echo "scale=0; ($global_pktx * $THRESHOLD_NB_PKTX / $nbnodes)" | bc`
echo "threshold value=$threshold"


#compute the average stats
global_nbnodes=0
global_pktx=0
global_pkrx=0
global_pkdup=0
global_delay=0
for i in ${!array_pktx[*]} 
do
    if [ ${array_pktx[$i]} -gt $threshold ]
    then
        (( global_nbnodes++ ))
        global_pktx=`echo "$global_pktx +  ${array_pktx[$i]}" | bc`
        global_pkrx=`echo "$global_pkrx +  ${array_pkrx[$i]}" | bc`
        global_pkdup=`echo "$global_pkdup +  ${array_pkdup[$i]}" | bc`
        global_delay=`echo "$global_delay +  ${array_delay[$i]}" | bc`
    fi
done

echo "--------AVG--------"
echo "nb_nodes=$global_nbnodes"
echo "nb_pk_tx[avg]=`echo "$global_pktx / $global_nbnodes"| bc -l`"
echo "nb_pk_rx[avg]=`echo "$global_pkrx / $global_nbnodes"| bc -l`"
echo "ratio_duplicates[avg]=`echo "$global_pkdup / ($global_pkrx * $global_nbnodes)"| bc -l`"
echo "pdr[avg]=`echo "$global_pkrx / $global_pktx"| bc -l`"
echo "avg_delay(ASN)[avg]=`echo "$global_delay / $global_pkrx"| bc -l`"
echo "avg_delay(ms)[avg]=`echo "$global_delay * $TIMESLOT_DURATION / $global_pkrx"| bc -l`"
echo "-------------------"






rm $TMPFILE
rm $NODESLIST

#!/bin/bash

#converts a long address (8 bytes) into a short one (2 bytes)
function addr_long_to_short {
#	return ${1:12:4}
	result=${1:12:4}

}


TMPFILE=`mktemp` || exit 1
NODESLIST=`mktemp` || exit 1
TMPGEN=`mktemp` || exit 1
TMPRX=`mktemp` || exit 1


echo "TMPFILE: $TMPFILE"
echo "NODESLIST: $NODESLIST"


grep STAT_DATARX $1 | cut -d "|" -f 9 | cut -d "=" -f 2 > $TMPFILE

#get the node list
sort -u $TMPFILE > $NODESLIST
NBNODES=`wc -l $NODESLIST | cut -d " " -f 1` 
echo "$NBNODES nodes (+dagroot)"
#cat $NODESLIST


#get the list of seqnums for each source
for addr_l in `cat $NODESLIST` 
do
    #converts the long address (64B) into a short one (16B)
	addr_long_to_short $addr_l
	addr_s=$result

	echo "node $addr_s: ($addr_l)"

    #nb of packets received
    nb_pk_rx=0
    nb_pk_tx=0
    nb_pk_dup=0
    sum_delay=0
    
    #prepare the stats for this node
    cat $1 | grep STAT_DATAGEN | grep "l2Src=$addr_l" > $TMPGEN
    cat $1 | grep STAT_DATARX | grep "l2Src=$addr_l" > $TMPRX

    #get the list of seqnum generated
    SEQNUMS=`cat $1 | grep STAT_DATAGEN | grep "l2Src=$addr_l" | cut -d "|" -f 8 | cut -d "=" -f 2` 
    for seqnum in $SEQNUMS
    do
        
        #ASNs picked in the logs
        ASN_TX=`cat $TMPGEN | grep "seqnum=$seqnum" | cut -d "|" -f 4 | cut -d "=" -f 2`
        ASN_RX=`cat $TMPRX | grep "seqnum=$seqnum" | cut -d "|" -f 4 | cut -d "=" -f 2`

        #nb of packets generated
        nb_pk_tx=$((nb_pk_tx + 1))

        #the packet was received: lets' increase the delay
        if [ -n "$ASN_RX" ]
        then

            #search for duplicates, and keep only the first reception
            eval ASN_RX_ARRAY=($ASN_RX)
            if [ ${#ASN_RX_ARRAY[@]} -gt 1 ]
            then
                #echo "duplicate"
                ASN_RX=${ASN_RX_ARRAY[0]}
                nb_pk_dup=$((nb_pk_dup + 1))
            fi
        
            #echo "|$ASN_RX| - |$ASN_TX|"

            #compute the delay (in ASN)
            hop_delay=`echo "$ASN_RX - $ASN_TX" | bc -l` 
            sum_delay=` echo "$sum_delay + $hop_delay" | bc -l` 
       
            #nb of received packets
            nb_pk_rx=$((nb_pk_rx + 1))

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
    echo "nb_pk_tx=$nb_pk_tx"
    echo "nb_pk_rx=$nb_pk_rx"
    echo "ratio_duplicates=`echo "$nb_pk_dup / $nb_pk_rx" | bc -l`"
    echo "pdr=`echo "$nb_pk_rx / $nb_pk_tx" | bc -l`"
    echo "avg_delay(ASN)=`echo "$sum_delay / $nb_pk_rx" | bc -l`"
    echo "avg_delay(ms)=`echo "$sum_delay / $nb_pk_rx * 15" | bc -l`"
    echo "----------"
 
done



rm $TMPFILE
rm $NODESLIST

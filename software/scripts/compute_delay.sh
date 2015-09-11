#!/bin/bash

#converts a long address (8 bytes) into a short one (2 bytes)
function addr_long_to_short {
#	return ${1:12:4}
	result=${1:12:4}

}


TMPFILE=`mktemp` || exit 1
NODESLIST=`mktemp` || exit 1

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

    #get the list of seqnum generated
    SEQNUMS=`cat $1 | grep STAT_DATAGEN | grep "l2Src=$addr_l" | cut -d "|" -f 8 | cut -d "=" -f 2` 
    for seqnum in $SEQNUMS
    do
        echo $seqnum
        ASN_TX=`cat $1 | grep STAT_DATAGEN | grep "l2Src=$addr_l" | grep "seqnum=$seqnum" | cut -d "|" -f 4 | cut -d "=" -f 2`
        cat $1 | grep STAT_DATARX | grep "l2Src=$addr_l" #| grep "seqnum=$seqnum" | cut -d "|" -f 4 | cut -d "=" -f 2
       echo $ASN_TX
    done

#	PKTX=`cat $1 | grep STAT_DATAGEN | grep "l2Src=$addr_l" | wc -l | cut -d " " -f 1`
#	PKRX=`cat $1 | grep STAT_DATARX | grep "l2Src=$addr_l" | wc -l | cut -d " " -f 1 `

 


#	PDR=`echo "$PKRX / $PKTX" | bc -l`
#	echo "pdr=$PDR ($PKRX / $PKTX)"
 
done



#rm $TMPFILE
#rm $NODESLIST

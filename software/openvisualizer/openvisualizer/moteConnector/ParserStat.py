# Copyright (c) 2015, CNRS. 
# All rights reserved. 
#  
# Released under the BSD 3-Clause license as published at the link below.
# https://openwsn.atlassian.net/wiki/display/OW/License

import logging
log = logging.getLogger('ParserStat')
log.setLevel(logging.INFO)
log.addHandler(logging.NullHandler())

import struct

from pydispatch import dispatcher

from ParserException import ParserException
import Parser

class ParserStat(Parser.Parser):
    
    HEADER_LENGTH  = 2
    MSPERSLOT      = 15 #ms per slot.
   
    #type of stat message 
    SERTYPE_DATA_GENERATION    = 1
    SERTYPE_PKT_TX             = 2
    SERTYPE_PKT_RX             = 3
     
    def __init__(self):
        
        # log
        log.debug("create ParserStat instance")
        
        # initialize parent class
        Parser.Parser.__init__(self,self.HEADER_LENGTH)
        
        self._asn= ['asn_4',           # B
          'asn_2_3',                   # H
          'asn_0_1',                   # H
         ]
    
    
    #======================== public ==========================================
    
    #returns a string with the decimal value of a uint16_t
    def BytesToString(self, bytes):
        str = ""
        i = 0

        #print bytes

        for byte in bytes:
            str = format(eval("{0} + {1} * 256 ** {2}".format(str, byte, i)))
            #print ("{0}:{1}".format(i, str)) 
            i = i + 1      

        return(str)

    def BytesToAddr(self, bytes):
        str = ""
        i = 0

        for byte in bytes:
            str = str + "{:02x}".format(byte) 
            if (i != 7):
                str = str + "-"
            i += 1

        return(str)


    def parseInput(self,input):
        
        # log
        if log.isEnabledFor(logging.DEBUG):
            log.debug("received data {0}".format(input))
        
        #headers
        addr = input[:2]  
        mycomponent = input[2]   
        asnbytes = input[3:8]
        (self._asn) = struct.unpack('<BHH',''.join([chr(c) for c in asnbytes]))
        statType = input[8]   
        

        #depends on the stat-type
        if (statType == self.SERTYPE_DATA_GENERATION):
            log.info("STAT_DATAGEN|addr={0}|comp={1}|asn={2}|type={3}|seqnum={4}|trackinstance={5}|trackowner={6}|".format(
                ''.join('{:02x}'.format(a) for a in addr),
                mycomponent,
                self.BytesToString(asnbytes),
                statType,
                self.BytesToString(input[9:11]),
                self.BytesToString(input[11:13]),
                self.BytesToAddr(input[13:21])
                ));
        elif (statType == self.SERTYPE_PKT_TX):
            log.info("STAT_PK_RX|addr={0}|comp={1}|asn={2}|type={3}|trackinstance={4}|trackowner={5}|length={6}|txpower={7}|l2Dest={8}".format(
                ''.join('{:02x}'.format(a) for a in addr),
                mycomponent,
                self.BytesToString(asnbytes),
                statType,
                self.BytesToString(input[9:11]),
                self.BytesToAddr(input[11:19]),
                input[19],
                input[20],
                self.BytesToAddr(input[21:30])
                ));
 
        elif (statType == self.SERTYPE_PKT_RX):
           log.info("STAT_PK_RX|addr={0}|comp={1}|asn={2}|type={3}|length={4}".format(
                ''.join('{:02x}'.format(a) for a in addr),
                mycomponent,
                self.BytesToString(asnbytes),
                statType,
                input[9]
                ));
 
       
        return ('error',input)



 #======================== private =========================================
 
    def _asndiference(self,init,end):
         
       asninit = struct.unpack('<HHB',''.join([chr(c) for c in init]))
       asnend  = struct.unpack('<HHB',''.join([chr(c) for c in end]))
       if (asnend[2] != asninit[2]): #'byte4'
          return 0xFFFFFFFF
       else:
           pass
       
       diff = 0;
       if (asnend[1] == asninit[1]):#'bytes2and3'
          return asnend[0]-asninit[0]#'bytes0and1'
       else:
          if (asnend[1]-asninit[1]==1):##'bytes2and3'              diff  = asnend[0]#'bytes0and1'
              diff += 0xffff-asninit[0]#'bytes0and1'
              diff += 1;
          else:   
              diff = 0xFFFFFFFF
       
       return diff


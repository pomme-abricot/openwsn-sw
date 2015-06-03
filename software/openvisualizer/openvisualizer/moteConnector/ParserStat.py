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
        log.debug('create ParserStat instance')
        
        # initialize parent class
        Parser.Parser.__init__(self,self.HEADER_LENGTH)
        
        self._asn= ['asn_4',           # B
          'asn_2_3',                   # H
          'asn_0_1',                   # H
         ]
    
    
    #======================== public ==========================================
    
    #returns a string with the decimal value of a uint16_t
    def BytesToString(self, bytes):
        str = ''
        i = 0

        #print bytes

        for byte in bytes:
            str = format(eval('{0} + {1} * 256 ** {2}'.format(str, byte, i)))
            #print ('{0}:{1}'.format(i, str)) 
            i = i + 1      

        return(str)

    def BytesToAddr(self, bytes):
        str = ''
        i = 0

        for byte in bytes:
            str = str + '{:02x}'.format(byte) 
            if (i < len(bytes)-1):
                str = str + '-'
            i += 1

        return(str)

    def ByteToL4protocol(self, byte):
       
        IANA = {
        'IANA_IPv6HOPOPT'                     : 0x00,
        'IANA_TCP'                            : 0x06,
        'IANA_UDP'                            : 0x11,
        'IANA_IPv6ROUTE'                      : 0x2b,
        'IANA_ICMPv6'                         : 0x3a,
        'IANA_ICMPv6_ECHO_REQUEST'            :  128,
        'IANA_ICMPv6_ECHO_REPLY'              :  129,
        'IANA_ICMPv6_RS'                      :  133,
        'IANA_ICMPv6_RA'                      :  134,
        'IANA_ICMPv6_RA_PREFIX_INFORMATION'   :    3,
        'IANA_ICMPv6_RPL'                     :  155,
        'IANA_ICMPv6_RPL_DIO'                 : 0x01,
        'IANA_ICMPv6_RPL_DAO'                 : 0x02,
        'IANA_RSVP'                           :   46,
        'IANA_UNDEFINED'                      :  250
        } 

        for key, value in IANA.iteritems():
            if value == byte:
                return(key)
        return("IANA_UNKNOWN")

 

    def parseInput(self,input):
        
        # log
        if log.isEnabledFor(logging.DEBUG):
            log.debug('received data {0}'.format(input))
        
        #headers
        addr = input[:2]  
        mycomponent = input[2]   
        asnbytes = input[3:8]
        (self._asn) = struct.unpack('<BHH',''.join([chr(c) for c in asnbytes]))
        statType = input[8]   
        

        #depends on the stat-type
        if (statType == self.SERTYPE_DATA_GENERATION):
            log.info('STAT_DATAGEN|addr={0}|comp={1}|asn={2}|type={3}|trackinstance={4}|trackowner={5}|seqnum={6}|'.format(
                self.BytesToAddr(addr),
                mycomponent,
                self.BytesToString(asnbytes),
                statType,
                self.BytesToString(input[9:11]),
                self.BytesToAddr(input[11:19]),
                self.BytesToString(input[19:20])
                ));
        elif (statType == self.SERTYPE_PKT_TX):
            log.info('STAT_PK_TX|addr={0}|comp={1}|asn={2}|type={3}|trackinstance={4}|trackowner={5}|length={6}|l2Dest={7}|txpower={8}|numTxAttempts={9}|l4protocol={10}'.format(
                self.BytesToAddr(addr),
                mycomponent,
                self.BytesToString(asnbytes),
                statType,
                self.BytesToString(input[9:11]),
                self.BytesToAddr(input[11:19]),
                input[19],
                self.BytesToAddr(input[20:28]),
                input[28],
                input[29],
                self.ByteToL4protocol(input[30])
                ));
        elif (statType == self.SERTYPE_PKT_RX):
           log.info('STAT_PK_RX|addr={0}|comp={1}|asn={2}|type={3}|trackinstance={4}|trackowner={5}|length={6}|l2Src={7}|rssi={8}|lqi={9}|crc={10}'.format(
                self.BytesToAddr(addr),
                mycomponent,
                self.BytesToString(asnbytes),
                statType,
                self.BytesToString(input[9:11]),
                self.BytesToAddr(input[11:19]),
                input[19],
                self.BytesToAddr(input[20:28]),
                input[28],
                input[29],
                input[30]
                ));
 
 
       
        return ('error',input)



 #======================== private =========================================
 
  

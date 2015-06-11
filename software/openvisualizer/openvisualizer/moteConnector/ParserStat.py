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
    SERTYPE_CELL_ADD           = 4
    SERTYPE_CELL_REMOVE        = 5
    SERTYPE_ACK_TX             = 6
    SERTYPE_ACK_RX             = 7
     
 
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

    def ByteToFrameType(self, byte):
        IEEE154_TYPE = {
        'IEEE154_TYPE_BEACON'                 : 0,
        'IEEE154_TYPE_DATA'                   : 1,
        'IEEE154_TYPE_ACK'                    : 2,
        'IEEE154_TYPE_CMD'                    : 3,
        'IEEE154_TYPE_UNDEFINED'              : 5
        }
 
        for key, value in IEEE154_TYPE.iteritems():
            if value == byte:
                return(key)
        return("FTYPE_UNKNOWN")


    def ByteToUDPPort(self, bytes):
        
        result = eval(self.BytesToString(bytes))
        

        WKP = {
        'WKP_TCP_HTTP'                        :    80,
        'WKP_TCP_ECHO'                        :     7,
        'WKP_UDP_COAP'                        :  5683,
        'WKP_UDP_ECHO'                        :     7,
        'WKP_UDP_RINGMASTER'                  : 15000
        }

        for key, value in WKP.iteritems():
            if value == result:
                return(key)
        return("WKP_UNKNOWN")


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
            log.info('STAT_DATAGEN|addr={0}|comp={1}|asn={2}|statType={3}|trackinstance={4}|trackowner={5}|seqnum={6}|'.format(
                self.BytesToAddr(addr),
                mycomponent,
                self.BytesToString(asnbytes),
                statType,
                self.BytesToString(input[9:11]),
                self.BytesToAddr(input[11:19]),
                self.BytesToString(input[19:20])
                ));
        elif (statType == self.SERTYPE_PKT_TX):
            log.info('STAT_PK_TX|addr={0}|comp={1}|asn={2}|statType={3}|trackinstance={4}|trackowner={5}|length={6}|frameType={7}|l2Dest={8}|txpower={9}|numTxAttempts={10}|l4protocol={11}|l4srcport={12}|l4destport={13}'.format(
                self.BytesToAddr(addr),
                mycomponent,
                self.BytesToString(asnbytes),
                statType,
                self.BytesToString(input[9:11]),
                self.BytesToAddr(input[11:19]),
                input[19],
                self.ByteToFrameType(input[20]),
                self.BytesToAddr(input[21:29]),
                input[29],
                input[30],
                self.ByteToL4protocol(input[31]),
                self.ByteToUDPPort(input[32:34]),
                self.ByteToUDPPort(input[34:36])
                ));
        elif (statType == self.SERTYPE_PKT_RX):
           log.info('STAT_PK_RX|addr={0}|comp={1}|asn={2}|statType={3}|trackinstance={4}|trackowner={5}|length={6}|frameType={7}|l2Src={8}|rssi={9}|lqi={10}|crc={11}'.format(
                self.BytesToAddr(addr),
                mycomponent,
                self.BytesToString(asnbytes),
                statType,
                self.BytesToString(input[9:11]),
                self.BytesToAddr(input[11:19]),
                input[19],
                self.ByteToFrameType(input[20]),
                self.BytesToAddr(input[21:29]),
                input[29],
                input[30],
                input[31]
                ));
        elif (statType == self.SERTYPE_CELL_ADD):
           log.info('STAT_CELL_ADD|addr={0}|comp={1}|asn={2}|statType={3}|trackinstance={4}|trackowner={5}|slotOffset={6}|type={7}|shared={8}|channelOffset={9}|neighbor={10}'.format(
                self.BytesToAddr(addr),
                mycomponent,
                self.BytesToString(asnbytes),
                statType,
                self.BytesToString(input[9:11]),
                self.BytesToAddr(input[11:19]),
                input[19],
                input[20],
                input[21],
                input[22],
                self.BytesToAddr(input[23:31])
                ));       
        elif (statType == self.SERTYPE_CELL_REMOVE):
           print('STAT_CELL_REMOVE|addr={0}|comp={1}|asn={2}|statType={3}|trackinstance={4}|trackowner={5}|slotOffset={6}|type={7}|shared={8}|channelOffset={9}|neighbor={10}'.format(
                self.BytesToAddr(addr),
                mycomponent,
                self.BytesToString(asnbytes),
                statType,
                self.BytesToString(input[9:11]),
                self.BytesToAddr(input[11:19]),
                input[19],
                input[20],
                input[21],
                input[22],
                self.BytesToAddr(input[23:31])
                ));
        elif (statType == self.SERTYPE_ACK_TX):
           log.info('STAT_ACK_TX|addr={0}|comp={1}|asn={2}|statType={3}'.format(
                self.BytesToAddr(addr),
                mycomponent,
                self.BytesToString(asnbytes),
                statType
                ));
        elif (statType == self.SERTYPE_ACK_RX):
           log.info('STAT_ACK_RX|addr={0}|comp={1}|asn={2}|statType={3}'.format(
                self.BytesToAddr(addr),
                mycomponent,
                self.BytesToString(asnbytes),
                statType
                ));
        else:
            print('received data {0}'.format(input))
 
       
        return ('error', input)



 #======================== private =========================================
 
  

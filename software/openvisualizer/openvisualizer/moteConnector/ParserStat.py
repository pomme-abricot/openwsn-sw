# Copyright (c) 2015, CNRS. 
# All rights reserved. 
#  
# Released under the BSD 3-Clause license as published at the link below.
# https://openwsn.atlassian.net/wiki/display/OW/License
import logging
log = logging.getLogger('ParserStat')
log.setLevel(logging.ERROR)
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


     
    def__init__(self):
        
        # log
        log.info("create SS instance stat")
        
        # initialize parent class
        Parser.Parser.__init__(self,self.HEADER_LENGTH)
        
        self._asn= ['asn_4',                     # B
          'asn_2_3',                   # H
          'asn_0_1',                   # H
         ]
    
    
    #======================== public ==========================================
    
    def parseInput(self,input):
        
        # log
        if log.isEnabledFor(logging.DEBUG):
            log.debug("received data {0}".format(input))
        print "received data {0}".format(input)
        
        #headers
        addr = input[:2]  
        mycomponent = input[2]   
        asnbytes = input[3:8]
        (self._asn) = struct.unpack('<BHH',''.join([chr(c) for c in asnbytes]))
        statType = input[8]   
        
      
        #depends on the stat-type
        if (statType == self.SERTYPE_DATA_GENERATION):
            print(" SPECIFIC: data generation")
        

        print("statserial: addr=", addr, ", mycomponent=", mycomponent, ", asn=", asnbytes)

        
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

# DO NOT EDIT DIRECTLY!
# This file was generated automatically by GenStackDefines.py
# on Tue, 19 Jul 2016 14:44:07
#

components = {
   0: "NULL",
   1: "OPENWSN",
   2: "IDMANAGER",
   3: "OPENQUEUE",
   4: "OPENSERIAL",
   5: "PACKETFUNCTIONS",
   6: "RANDOM",
   7: "RADIO",
   8: "IEEE802154",
   9: "IEEE802154E",
  10: "SIXTOP_TO_IEEE802154E",
  11: "IEEE802154E_TO_SIXTOP",
  12: "SIXTOP",
  13: "NEIGHBORS",
  14: "SCHEDULE",
  15: "SIXTOP_RES",
  16: "OPENBRIDGE",
  17: "IPHC",
  18: "FORWARDING",
  19: "ICMPv6",
  20: "ICMPv6ECHO",
  21: "ICMPv6ROUTER",
  22: "ICMPv6RPL",
  23: "OPENTCP",
  24: "OPENUDP",
  25: "OPENCOAP",
  26: "C6T",
  27: "CEXAMPLE",
  28: "CINFO",
  29: "CLEDS",
  30: "CSENSORS",
  31: "CSTORM",
  32: "CWELLKNOWN",
  33: "TECHO",
  34: "TOHLONE",
  35: "UECHO",
  36: "UINJECT",
  37: "RRT",
  38: "SECURITY",
  39: "OTF",
}

errorDescriptions = {
   1: "received an echo request",
   2: "received an echo reply",
   3: "getData asks for too few bytes, maxNumBytes={0}, fill level={1}",
   4: "the input buffer has overflown",
   5: "the command is not allowerd, command = {0}",
   6: "unknown transport protocol {0} (code location {1})",
   7: "wrong TCP state {0} (code location {1})",
   8: "TCP reset while in state {0} (code location {1})",
   9: "unsupported port number {0} (code location {1})",
  10: "unexpected DAO (code location {0})",
  11: "unsupported ICMPv6 type {0} (code location {1})",
  12: "unsupported 6LoWPAN parameter {1} at location {0}",
  13: "no next hop",
  14: "invalid parameter",
  15: "invalid forward mode",
  16: "large DAGrank {0}, set to {1}",
  17: "packet discarded hop limit reached",
  18: "loop detected due to previous rank {0} lower than current node rank {1}",
  19: "upstream packet set to be downstream, possible loop.",
  20: "neighbors table is full (max number of neighbor is {0})",
  21: "there is no sent packet in queue",
  22: "there is no received packet in queue",
  23: "schedule overflown",
  24: "wrong celltype {0} at slotOffset {1}",
  25: "unsupported IEEE802.15.4 parameter {1} at location {0}",
  26: "got desynchronized at slotOffset {0}",
  27: "synchronized at slotOffset {0}",
  28: "large timeCorr.: {0} ticks (code loc. {1})",
  29: "wrong state {0} in end of frame+sync",
  30: "wrong state {0} in startSlot, at slotOffset {1}",
  31: "wrong state {0} in timer fires, at slotOffset {1}",
  32: "wrong state {0} in start of frame, at slotOffset {1}",
  33: "wrong state {0} in end of frame, at slotOffset {1}",
  34: "maxTxDataPrepare overflows while at state {0} in slotOffset {1}",
  35: "maxRxAckPrepapare overflows while at state {0} in slotOffset {1}",
  36: "maxRxDataPrepapre overflows while at state {0} in slotOffset {1}",
  37: "maxTxAckPrepapre overflows while at state {0} in slotOffset {1}",
  38: "wdDataDuration overflows while at state {0} in slotOffset {1}",
  39: "wdRadio overflows while at state {0} in slotOffset {1}",
  40: "wdRadioTx overflows while at state {0} in slotOffset {1}",
  41: "wdAckDuration overflows while at state {0} in slotOffset {1}",
  42: "busy sending",
  43: "sendDone for packet I didn't send",
  44: "no free packet buffer (code location {0})",
  45: "freeing unused memory",
  46: "freeing memory unsupported memory",
  47: "unsupported command {0}",
  48: "unknown message type {0}",
  49: "wrong address type {0} (code location {1})",
  50: "bridge mismatch (code location {0})",
  51: "header too long, length {1} (code location {0})",
  52: "input length problem, length={0}",
  53: "booted",
  54: "invalid serial frame",
  55: "invalid packet from radio, length {1} (code location {0})",
  56: "busy receiving when stop of serial activity, buffer input length {1} (code location {0})",
  57: "wrong CRC in input Buffer (input length {0})",
  58: "synchronized when received a packet",
  59: "security error on frameType {0}, code location {1}",
  60: "otf does not have enough cells (trackInstance {0}, nbCells to add {1})",
  61: "Unknown neighbor {0}{1} (4 last bytes)",
  62: "sixtop expects another parameter in its request (bw {0}, nbcells {1})",
  63: "sixtop current state {0}, location {1}",
  64: "sixtop requires a non null handler",
  65: "a timeout has been fired. We have to flush 6top packets (we have the state {0}, timeout {1})",
  66: "a packet has been removed from the queue (owner {0], creator {1})",
  67: "the best effort track cannot have an owner (here type {0} and addr {1})",
  68: "not enough space in openqueue for non prioritar packets",
  69: "received frame with invalid CRC",
  70: "invalid IEEE 802.15.4e headers",
  71: "output buffer overflow in openserial (available space {0}, towrite {1})",
  72: "openqueue overflow: too many packets (space left {0}, reserved for management {1})",
  73: "too many cells to reserve in the sixtop request (asked {0}, max {1})",
  74: "the cells from the same LinkRem are associated with different tracks",
  75: "a packet cannot be allocated for component {0} when the node is not synchronized",
  76: "The component {0} cannot trigger this command (location {1})",
  77: "Sixtop cannot remove any cell to the parent {0}{1} (none existing)",
  78: "generic error {0} {1}",
  79: "unknown error, location {0}, arg {1}",
}

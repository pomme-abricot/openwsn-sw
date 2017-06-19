class Event_DataGen(object):
    time = ""
    addr = ""
    comp = ""
    asn = ""
    statType = ""
    trackinstance = ""
    trackowner = ""
    seqnum = ""
    l2Src = ""
    l2Dest = ""
    queuePos = ""
    recu = 0.
    

    def __init__(self, time, addr, comp, asn, statType, trackinstance, trackowner, seqnum, l2Src, l2Dest, queuePos, recu):
        self.time = time
        self.addr = addr
        self.comp = comp
        self.asn = asn
        self.statType = statType
        self.trackinstance = trackinstance
        self.trackowner = trackowner
        self.seqnum = seqnum
        self.l2Src = l2Src
        self.l2Dest = l2Dest
        self.queuePos = queuePos
        self.recu = recu

def make_event_DataGen(time, addr, comp, asn, statType, trackinstance, trackowner, seqnum, l2Src, l2Dest, queuePos, recu):
    event_DataGen = Event_DataGen(time, addr, comp, asn, statType, trackinstance, trackowner, seqnum, l2Src, l2Dest, queuePos, recu)
    return event_DataGen



class Event_PK_TX(object):
    time = ""
    addr = ""
    comp = ""
    asn = ""
    statType = ""
    trackinstance = ""
    trackowner = ""
    length = ""
    frameType = ""
    slotOffset = ""
    frequency = ""
    l2Dest = ""
    txpower = "" 
    numTxAttempts = ""
    queuePos = ""
    recu = 0.
    

    def __init__(self, time, addr, comp, asn, statType, trackinstance, trackowner, length, frameType, slotOffset, frequency, l2Dest, txpower, numTxAttempts, queuePos, recu):
        self.time = time
        self.addr = addr
        self.comp = comp
        self.asn = asn
        self.statType = statType
        self.trackinstance = trackinstance
        self.trackowner = trackowner
        self.length = length
        self.frameType = frameType
        self.slotOffset = slotOffset
        self.frequency = frequency
        self.l2Dest = l2Dest
        self.txpower = txpower
        self.numTxAttempts = numTxAttempts
        self.queuePos = queuePos
        self.recu = recu

def make_event_PK_TX(time, addr, comp, asn, statType, trackinstance, trackowner, length, frameType, slotOffset, frequency, l2Dest, txpower, numTxAttempts, queuePos, recu):
    event_PK_TX = Event_PK_TX(time, addr, comp, asn, statType, trackinstance, trackowner, length, frameType, slotOffset, frequency, l2Dest, txpower, numTxAttempts, queuePos, recu)
    return event_PK_TX


class Event_PK_RX(object):
    time = ""
    addr = ""
    comp = ""
    asn = ""
    statType = ""
    trackinstance = ""
    trackowner = ""
    length = ""
    frameType = ""
    slotOffset = ""
    frequency = ""
    l2Src = ""
    rssi = "" 
    lqi = ""
    crc = ""
    queuePos = ""

    

    def __init__(self, time, addr, comp, asn, statType, trackinstance, trackowner, length, frameType, slotOffset, frequency, l2Src, rssi, lqi, crc, queuePos):
        self.time = time
        self.addr = addr
        self.comp = comp
        self.asn = asn
        self.statType = statType
        self.trackinstance = trackinstance
        self.trackowner = trackowner
        self.length = length
        self.frameType = frameType
        self.slotOffset = slotOffset
        self.frequency = frequency
        self.l2Src = l2Src
        self.rssi = rssi
        self.lqi = lqi
        self.crc = crc
        self.queuePos = queuePos


def make_event_PK_RX(time, addr, comp, asn, statType, trackinstance, trackowner, length, frameType, slotOffset, frequency, l2Src, rssi, lqi, crc, queuePos):
    event_PK_RX = Event_PK_RX(time, addr, comp, asn, statType, trackinstance, trackowner, length, frameType, slotOffset, frequency, l2Src, rssi, lqi, crc, queuePos)
    return event_PK_RX


class Cell_Reservation(object):
    id = 0
    asn = []
    succes = 0.
    numAttempts = ""
    simult = ""
    queuePos = []
    slot = ""
    ch = ""
    src = ""
    dest = ""
    owner = ""
    state = 0
    
    def __init__(self, id, asn, succes, numAttempts, simult, queuePos, slot, ch, src, dest, owner, state):
        self.id = id
        self.asn = asn
        self.succes = succes
        self.numAttempts = numAttempts
        self.simult = simult
        self.queuePos = queuePos
        self.slot = slot
        self.ch = ch
        self.src = src
        self.dest = dest
        self.owner = owner
        self.state = state
        
def make_cell_reservation(id, asn, succes, numAttempts, simult, queuePos, slot, ch, src, dest, owner, state):
    cell_Reservation = Cell_Reservation(id, asn, succes, numAttempts, simult, queuePos, slot, ch, src, dest, owner, state)
    return cell_Reservation
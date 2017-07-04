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
    asn1 = ""
    asn2 = ""
    asn3 = ""
    succes = 0.
    numAttempts = ""
    simult = ""
    queuePos = []
    slot1 = ""
    ch1 = ""
    s1 = ''
    lot2 = ""
    ch2 = ""
    s2 = ''
    lot3 = ""
    ch3 = ""
    s3 = ''
    src = ""
    dest = ""
    owner = ""
    state = 0
    
    def __init__(self, id, asn1, asn2, asn3, succes, numAttempts, simult, queuePos, slot1, ch1, s1, slot2, ch2, s2, slot3, ch3, s3, src, dest, owner, state, nbCellsReq, nbCellsRep):
        self.id = id
        self.asn1 = asn1
        self.asn2 = asn2
        self.asn3 = asn3
        self.succes = succes
        self.numAttempts = numAttempts
        self.simult = simult
        self.queuePos = queuePos
        self.slot1 = slot1
        self.ch1 = ch1
        self.s1= s1
        self.slot2 = slot2
        self.ch2 = ch2
        self.s2= s2
        self.slot3 = slot3
        self.ch3 = ch3
        self.s3= s3
        self.src = src
        self.dest = dest
        self.owner = owner
        self.state = state
        self.nbCellsReq = nbCellsReq
        self.nbCellsRep = nbCellsRep
        
def make_cell_reservation(id, asn1, asn2, asn3, succes, numAttempts, simult, queuePos, slot1, ch1, s1, slot2, ch2, s2, slot3, ch3, s3, src, dest, owner, state, nbCellsReq, nbCellsRep):
    cell_Reservation = Cell_Reservation(id, asn1, asn2, asn3, succes, numAttempts, simult, queuePos, slot1, ch1, s1, slot2, ch2, s2, slot3, ch3, s3, src, dest, owner, state, nbCellsReq, nbCellsRep)
    return cell_Reservation
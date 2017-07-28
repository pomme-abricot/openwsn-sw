# -*-coding:Latin-1 -*

import re
import pandas as pd

#replace the substring old by new for the nb of occurrence starting from the END of the string
#def rreplace(s, old, new, occurrence):
 
#rearange la ligne pour les ligne de type event ParserStat
#def fix_line(line):

# separe data.log en sous fichier en fonction du type
#def sep_data_event(nom_fichier_data):

 #separe le fichier log selon les neuds | retourne la liste des noeuds
#def sep_data_addr(nom_fichier_data):

#TOUS LES GETTERS ET SETTERS VARIABLES LORS DES LECTURE DE LIGNES


#replace the substring old by new for the nb of occurrence starting from the END of the string
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

#rearange la ligne pour les ligne de type event ParserStat
def fix_line(line):
    #separe toutes les variable par "|"
    line_fixed = rreplace(line," ", "|", line.count(' ') - 1)
    #ajouter "time="
    line_fixed = "time="+line_fixed
    #ajouter "type=" devant [***]
    line_fixed = line_fixed[:line_fixed.find("|")+1] + 'type=' + line_fixed[line_fixed.find("|")+1:]
    #ajouter "eventType=" apres le 2eme "|"
    line_fixed = line_fixed[:line_fixed.find("|",line_fixed.find("|")+1)+1] + 'eventType=' + line_fixed[line_fixed.find("|",line_fixed.find("|")+1)+1:]
    return line_fixed


# separe data.log en sous fichier en fonction du type 
def sep_data_event(nom_fichier_data):
    with open(nom_fichier_data) as origin_file:
        for line in origin_file:
            #Pour trouver ce qu'il y a entre []
            #data_type = re.findall('\[(.*?)\]', line)
            #if data_type:
                #print data_type[0]
            if "STAT_CELL" in line:
                with open("data/parsed/event/STAT_CELL.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_ACK" in line:
                with open("data/parsed/event/STAT_ACK.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_PK_TX" in line:
                with open("data/parsed/event/STAT_PK_TX.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_PK_RX" in line:
                with open("data/parsed/event/STAT_PK_RX.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_6PCMD" in line:
                with open("data/parsed/event/STAT_6PCMD.log", "a") as f:
                    f.write(fix_line(line))
            else:
                #on traite les cas differents
                #Pour trouver ce qu'il y a entre []
                data_type = re.findall('\[(.*?)\]', line)
                #on verifie qu'il y a [***] dans la ligne
                if data_type:
                    if "ParserInfoErrorCritical" in data_type[0]:
                        with open("data/parsed/event/data_OTHER_ParserInfoErrorCritical.log", "a") as f:
                            f.write(line) 
                    elif "moteState" in data_type[0]:
                        with open("data/parsed/event/data_OTHER_moteState.log", "a") as f:
                            f.write(line) 
                    elif "ParserPrintf" in data_type[0]:
                        with open("data/parsed/event/data_OTHER_ParserPrintf.log", "a") as f:
                            f.write(line) 
                    # pour ne pas separer [openvisualizer] des lignes qui le suivent
                    elif "openVisualizerApp" in data_type[0]: 
                        with open("data/parsed/event/data_OTHER.log", "a") as f:
                            f.write(line)
                    else: 
                        with open("data/parsed/event/data_OTHER_.log", "a") as f:
                            f.write(line)
                else:
                    with open("data/parsed/event/data_OTHER.log", "a") as f:
                            f.write(line)
                            
                            
#modifier pour nouveau type de données
"""                           
# separe data.log en sous fichier en fonction du type 
def sep_data_event(nom_fichier_data):
    with open(nom_fichier_data) as origin_file:
        for line in origin_file:
            #Pour trouver ce qu'il y a entre []
            #data_type = re.findall('\[(.*?)\]', line)
            #if data_type:
                #print data_type[0]
            if "STAT_DATAGEN" in line:
                with open("data/parsed/event/data_STAT_DATAGEN.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_DATARX" in line:
                with open("data/parsed/event/data_STAT_DATARX.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_PK_TX" in line:
                with open("data/parsed/event/data_STAT_PK_TX.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_PK_RX" in line:
                with open("data/parsed/event/data_STAT_PK_RX.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_CELL_ADD" in line:
                with open("data/parsed/event/data_STAT_CELL_ADD.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_CELL_REMOVE" in line:
                with open("data/parsed/event/data_STAT_CELL_REMOVE.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_ACK_TX" in line:
                with open("data/parsed/event/data_STAT_ACK_TX.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_ACK_RX" in line:
                with open("data/parsed/event/data_STAT_ACK_RX.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_PK_TIMEOUT" in line:
                with open("data/parsed/event/data_STAT_PK_TIMEOUT.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_PK_ERROR" in line:
                with open("data/parsed/event/data_STAT_PK_ERROR.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_PK_BUFFEROVERFLOW" in line:
                with open("data/parsed/event/data_STAT_PK_BUFFEROVERFLOW.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_DIOTX" in line:
                with open("data/parsed/event/data_STAT_DIOTX.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_DAOTX" in line:
                with open("data/parsed/event/data_STAT_DAOTX.log", "a") as f:
                    f.write(fix_line(line))
            elif "STAT_NODESTATE" in line:
                with open("data/parsed/event/data_STAT_NODESTATE.log", "a") as f:
                    f.write(fix_line(line))
            else:
                #on traite les cas differents
                #Pour trouver ce qu'il y a entre []
                data_type = re.findall('\[(.*?)\]', line)
                #on verifie qu'il y a [***] dans la ligne
                if data_type:
                    if "ParserInfoErrorCritical" in data_type[0]:
                        with open("data/parsed/event/data_OTHER_ParserInfoErrorCritical.log", "a") as f:
                            f.write(line) 
                    elif "moteState" in data_type[0]:
                        with open("data/parsed/event/data_OTHER_moteState.log", "a") as f:
                            f.write(line) 
                    elif "ParserPrintf" in data_type[0]:
                        with open("data/parsed/event/data_OTHER_ParserPrintf.log", "a") as f:
                            f.write(line) 
                    # pour ne pas separer [openvisualizer] des lignes qui le suivent
                    elif "openVisualizerApp" in data_type[0]: 
                        with open("data/parsed/event/data_OTHER.log", "a") as f:
                            f.write(line)
                    else: 
                        with open("data/parsed/event/data_OTHER_.log", "a") as f:
                            f.write(line)
                else:
                    with open("data/parsed/event/data_OTHER.log", "a") as f:
                            f.write(line)
"""
             
 #separe le fichier log selon les neuds | retourne la liste des noeuds
def sep_data_addr(nom_fichier_data):
    addr = []
    nom_fichier_dest = ""
    with open(nom_fichier_data) as origin_file:
        for line in origin_file:
            #Pour trouver l'addresse
            if "addr" in line:
                addr_tmp = line[line.find("addr")+5:line.find("|",line.find("addr"))]
                #si l'element a deja ete compte, on ajoute la ligne au fichier correspondant
                nom_fichier_dest = "data/parsed/node/" + addr_tmp +".log"
                with open(nom_fichier_dest, "a") as f:
                    f.write(fix_line(line)) 
                    
                    
#recupere les variables
def get_time(line):
    return line[line.find("time")+len("time="):line.find("|", line.find("time"))]
    
def get_addr(line):
    return line[line.find("addr")+len("addr="):line.find("|", line.find("addr"))]

def get_comp(line):
    return line[line.find("comp")+len("comp="):line.find("|", line.find("comp"))]

def get_asn(line):
    return line[line.find("asn")+len("asn="):line.find("|", line.find("asn"))]

def get_trackinstance(line):
    return line[line.find("trackinstance")+len("trackinstance="):line.find("|", line.find("trackinstance"))]

def get_trackowner(line):
    return line[line.find("trackowner")+len("trackowner="):line.find("|", line.find("trackowner"))]

def get_length(line):
    return line[line.find("length")+len("length="):line.find("|", line.find("length"))]

def get_frameType(line):
    return line[line.find("frameType")+len("frameType="):line.find("|", line.find("frameType"))]
    
def get_slotOffset(line):
    return line[line.find("slotOffset")+len("slotOffset="):line.find("|", line.find("slotOffset"))]

def get_frequency(line):
    return line[line.find("frequency")+len("frequency="):line.find("|", line.find("frequency"))]

def get_l2Dest(line):
    return line[line.find("l2Dest")+len("l2Dest="):line.find("|", line.find("l2Dest"))]

def get_l2Src(line):
    return line[line.find("l2Src")+len("l2Src="):line.find("|", line.find("l2Src"))]

def get_txpower(line):
    return line[line.find("txpower")+len("txpower="):line.find("|", line.find("txpower"))]

def get_numTxAttempts(line):
    return line[line.find("numTxAttempts")+len("numTxAttempts="):line.find("|", line.find("numTxAttempts"))]

def get_queuePos(line):
    return line[line.find("queuePos")+len("queuePos="):line.find("|", line.find("queuePos"))]

def get_rssi(line):
    return line[line.find("rssi")+len("rssi="):line.find("|", line.find("rssi"))]

def get_lqi(line):
    return line[line.find("lqi")+len("lqi="):line.find("|", line.find("lqi"))]

def get_crc(line):
    return line[line.find("crc")+len("crc="):line.find("|", line.find("crc"))]

def get_statType(line):
    return line[line.find("statType")+len("statType="):line.find("|", line.find("statType"))]

def get_seqnum(line):
    return line[line.find("seqnum")+len("seqnum="):line.find("|", line.find("seqnum"))]

def get_L3Src(line):
    return line[line.find("L3Src")+len("L3Src="):line.find("|", line.find("L3Src"))]

def get_L3Dest(line):
    return line[line.find("L3Dest")+len("L3Dest="):line.find("|", line.find("L3Dest"))]

def get_L4Proto(line):
    return line[line.find("L4Proto")+len("L4Proto="):line.find("|", line.find("L4Proto"))]

def get_L4SrcPort(line):
    return line[line.find("L4SrcPort")+len("L4SrcPort="):line.find("|", line.find("L4SrcPort"))]

def get_status(line):
    return line[line.find("status")+len("status="):line.find("|", line.find("status"))]

def get_command(line):
    return line[line.find("command")+len("command="):line.find("|", line.find("command"))]

def get_choffset(line):
    return line[line.find("choffset")+len("choffset="):line.find("|", line.find("choffset"))]

def get_slotoffset(line):
    return line[line.find("slotoffset")+len("slotoffset="):line.find("|", line.find("slotoffset"))]

def get_neigh(line):
    return line[line.find("neigh")+len("neigh="):line.find("|", line.find("neigh"))]

def get_command(line):
    return line[line.find("command")+len("command="):line.find("|", line.find("command"))]

def get_celltype(line):
    return line[line.find("celltype")+len("celltype="):line.find("|", line.find("celltype"))]

def get_neighbor(line):
    return line[line.find("neighbor")+len("neighbor="):line.find("|", line.find("neighbor"))]

def get_src(line):
    return line
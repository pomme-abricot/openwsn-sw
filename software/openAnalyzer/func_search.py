# -*-coding:Latin-1 -*

import re
import pandas as pd

 #donne la liste de noeuds de l'experimentation
#def get_all_addr(nom_fichier_data):

#cree une liste des evenements pour un neud avec une numerotation selon l'ordre d'apparition
#def list_event(nom_fichier_data):

#cree une liste des evenements pour un neud avec une numerotation predefinie
#def list_event2(nom_fichier_data):

# obtenir les voisins d'un noeud a un asn donné
#def get_neighbor_node(addr_1, asn_data):
                    
 #donne la liste de noeuds de l'experimentation
def get_all_addr(nom_fichier_data):
    addr = []
    with open(nom_fichier_data) as origin_file:
        for line in origin_file:
            #Pour trouver l'addresse
            if "addr" in line:
                addr_tmp = line[line.find("addr")+5:line.find("|",line.find("addr"))]
                #si l'element a deja ete compte, on ne l'ajoute pas a la liste
                if addr_tmp not in addr and len(addr_tmp)<5:
                    addr.append(addr_tmp)
    return addr
    
#cree une liste des evenements pour un neud avec une numerotation selon l'ordre d'apparition
def list_event(nom_fichier_data):
    list_of_event = []
    name_of_event = []
    
    with open(nom_fichier_data) as origin_file:
        for line in origin_file:
            event_tmp = line[line.find("eventType")+len("eventType="):line.find("|",line.find("eventType"))]
            if event_tmp in name_of_event:
                pass
            else:
                name_of_event.append(event_tmp)
            list_of_event.append(name_of_event.index(event_tmp))
    return name_of_event, list_of_event


#cree une liste des evenements pour un neud avec une numerotation predefinie
def list_event2(nom_fichier_data):
    list_of_event = []
    name_of_event = ['STAT_CELL_ADD', 'STAT_CELL_REMOVE', 'STAT_DIOTX', 'STAT_DAOTX', 'STAT_PK_TX', 'STAT_PK_RX', 'STAT_ACK_TX', 'STAT_ACK_RX', 'STAT_DATAGEN', 'STAT_DATARX', 'STAT_PK_TIMEOUT', 'STAT_PK_ERROR', 'STAT_PK_BUFFEROVERFLOW', 'STAT_NODESTATE']
    
    with open(nom_fichier_data) as origin_file:
        for line in origin_file:
            event_tmp = line[line.find("eventType")+len("eventType="):line.find("|",line.find("eventType"))]
            list_of_event.append(name_of_event.index(event_tmp))
    return name_of_event, list_of_event


# obtenir les voisins d'un noeud a un asn donné
def get_neighbor_node(addr_1, asn_data):
    # on remonte au dernier envoi de msg beacon, et on regarde qui repond
    # par defaut nb_nei est a 0 cad que le noeud n'a pas de voisin
    nb_neig = 0
    list_neigh = []
    asn_last_beac = 0

    #on cherche le dernier msg beacon envoyé | on lit le fichier a l'envers pour s'arreter la premiere
    #fois que l'on trouve un asn < asn_data avec les données correspondantes
    for line in reversed(open("data/parsed/event/data_STAT_PK_TX.log", "r").readlines()):
            if (addr_1 == get_addr(line) and get_frameType(line) == "IEEE154_TYPE_BEACON"
               and asn_data > int(get_asn(line))):
                asn_last_beac = get_asn(line)
                break
                
    if asn_last_beac != 0:
        #on regarde quels sont les noeuds qui ont recus le msg
        with open("data/parsed/event/data_STAT_PK_RX.log", "r") as f_rx:
            for line in f_rx:
                if (get_l2Src(line).endswith(addr_1) and get_frameType(line) == "IEEE154_TYPE_BEACON"
                   and asn_last_beac == get_asn(line)):
                    nb_neig+=1
                    list_neigh.append(get_addr(line))

    return nb_neig, list_neigh


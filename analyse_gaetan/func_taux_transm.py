# -*-coding:Latin-1 -*

from func_search import *
from func_def_class import *
from func_parsing_logfile import *

import numpy as np



##fonction qui calcule le taux de livraison pour un noeud | données : nom du noeud, largeur fenetre asn, pas
#def transmission_ratio_addr(addr_node, Dasn, step):

##retourne le taux de transmission entre deux noeuds | donnée nom de l'emetteur, nom du recepteur
#def transmission_ratio_flow(addr_1, addr_2, Dasn, step):

##calcul le taux de transmission vu par le noeud emeteur (addr1)
#def transmission_ratio_flow_node(addr_1, addr_2, Dasn, step):

## obtenir les voisins d'un noeud a un asn donné
#def get_neighbor_node(addr_1, asn_data):

##obtenir le taux de transm a un asn donné | asn_data  | Dasn est la fenetre pour laquelle on calcule le taux
##le taux est de -1 si aucun msg n'a été envoyés 
#prend en entré PT_OF_VIEW_NODE qui est vrai si on se restraint aux msg dont le noeud recois les aquittements
#def get_ration_trans_node(addr_1, addr_2, asn_data, Dasn, PT_OF_VIEW_NODE):

##afficher une reservation
##def print_res(res):


#fonction qui calcule le taux de livraison pour un noeud | données : nom du noeud, largeur fenetre asn, pas
def transmission_ratio_addr(addr_node, Dasn, step):
    asn_debut = 0
    #liste_ev ne comprend que les elemt qui sont dans la fenetre asn 
    list_ev = []
    #liste_ev_tot contient toutes les tx du noeud 
    list_ev_datagen = []
    #liste qui contient la valeur de transmission pour chaque fenetre / -1 si pas de valeurs
    taux_transm = []

    #pour obtenir la valeur asn finale, la liste des tx du noeud :
    with open("data/parsed/event/data_STAT_DATAGEN.log", "r") as f_tx:
        for line in f_tx:
            #print get_addr(line), addr_node
            if (addr_node == get_addr(line)):
                list_ev_datagen.append(make_event_DataGen(get_time(line), 
                                                           get_addr(line), 
                                                           get_comp(line), 
                                                           get_asn(line), 
                                                           get_statType(line), 
                                                           get_trackinstance(line), 
                                                           get_trackowner(line), 
                                                           get_seqnum(line), 
                                                           get_l2Src(line), 
                                                           get_l2Dest(line), 
                                                           get_queuePos(line),
                                                           0.))

        asn_fin = int(get_asn(line))
        
    #on verifie si ces msgs ont été recus
    with open("data/parsed/event/data_STAT_DATARX.log", "r") as f_rx:
        for line in f_rx:
            #si la source est le noeud 
            if get_l2Src(line).endswith(addr_node):
                for event in list_ev_datagen:
                    if event.seqnum == get_seqnum(line):
                        event.recu=1.
                        
                        
    #pour chaque elmt transmit on ne selectionne que ceux qui proviennent du noeud
    #et ceux qui sont dans l'intervalle Dasn
    while (asn_debut < asn_fin):
        del list_ev[:]
        list_ev = []
        for event in list_ev_datagen:
            if (int(event.asn) < (asn_debut + Dasn) and int(event.asn) > asn_debut):
                list_ev.append(event.recu)
        if list_ev:
            taux_transm.append(np.sum(list_ev)/len(list_ev))
        else:
            taux_transm.append(-1.)
        asn_debut = asn_debut + step
        
    return taux_transm


#retourne le taux de transmission entre deux noeuds | donnée nom de l'emetteur, nom du recepteur
def transmission_ratio_flow(addr_1, addr_2, Dasn, step):
    asn_debut = 0
    #liste_ev ne comprend que les elemt qui sont dans la fenetre asn 
    list_ev = []
    #liste des msg envoyés entre noeud1 et 2
    list_ev_tx_1 = []
    list_ev_tx_2 = []
    #liste des msg recu par noeud 1 et 2
    list_ev_rx_1 = []
    list_ev_rx_2 = []
    #resultat
    taux_transm_1=[]
    taux_transm_2=[]
    
    #on classe les envois dans list_tx_1 et list_tx_2 
    with open("data/parsed/event/data_STAT_PK_TX.log", "r") as f_tx:
        for line in f_tx:
            #pour le noeud 1:
            if (addr_1 == get_addr(line) and get_l2Dest(line).endswith(addr_2)):
                list_ev_tx_1.append(make_event_PK_TX(get_time(line), 
                                                           get_addr(line), 
                                                           get_comp(line), 
                                                           get_asn(line), 
                                                           get_statType(line), 
                                                           get_trackinstance(line), 
                                                           get_trackowner(line), 
                                                           get_length(line), 
                                                           get_frameType(line), 
                                                           get_slotOffset(line), 
                                                           get_frequency(line), 
                                                           get_l2Dest(line), 
                                                           get_txpower(line), 
                                                           get_numTxAttempts(line),
                                                           get_queuePos(line),
                                                           0.))
            elif (addr_2 == get_addr(line) and get_l2Dest(line).endswith(addr_1)):
                list_ev_tx_2.append(make_event_PK_TX(get_time(line), 
                                                           get_addr(line), 
                                                           get_comp(line), 
                                                           get_asn(line), 
                                                           get_statType(line), 
                                                           get_trackinstance(line), 
                                                           get_trackowner(line), 
                                                           get_length(line), 
                                                           get_frameType(line), 
                                                           get_slotOffset(line), 
                                                           get_frequency(line), 
                                                           get_l2Dest(line), 
                                                           get_txpower(line), 
                                                           get_numTxAttempts(line),
                                                           get_queuePos(line),
                                                           0.))
        asn_fin = int(get_asn(line))
    
    #on recupere les receptions
    with open("data/parsed/event/data_STAT_PK_RX.log", "r") as f_rx:
        for line in f_rx:
            #pour le noeud 1:
            if (addr_1 == get_addr(line) and get_l2Src(line).endswith(addr_2)):
                list_ev_rx_1.append(make_event_PK_RX(get_time(line), 
                                                           get_addr(line), 
                                                           get_comp(line), 
                                                           get_asn(line), 
                                                           get_statType(line), 
                                                           get_trackinstance(line), 
                                                           get_trackowner(line), 
                                                           get_length(line), 
                                                           get_frameType(line), 
                                                           get_slotOffset(line), 
                                                           get_frequency(line), 
                                                           get_l2Src(line), 
                                                           get_rssi(line), 
                                                           get_lqi(line),
                                                           get_crc(line),
                                                           get_queuePos(line)))
            elif (addr_2 == get_addr(line) and get_l2Src(line).endswith(addr_1)):
                list_ev_rx_2.append(make_event_PK_RX(get_time(line), 
                                                           get_addr(line), 
                                                           get_comp(line), 
                                                           get_asn(line), 
                                                           get_statType(line), 
                                                           get_trackinstance(line), 
                                                           get_trackowner(line), 
                                                           get_length(line), 
                                                           get_frameType(line), 
                                                           get_slotOffset(line), 
                                                           get_frequency(line), 
                                                           get_l2Src(line), 
                                                           get_rssi(line), 
                                                           get_lqi(line),
                                                           get_crc(line),
                                                           get_queuePos(line)))
                
                
    #on verifie quel msg on été recus
    #pour un msg de 1 -> 2
    for trans in list_ev_tx_1:
        #on verifie que le msg a été recu
        for recep in list_ev_rx_2:
            if (int(recep.asn) == int(trans.asn)):
                trans.recu = 1
                
    #pour un msg de 2 -> 1
    for trans in list_ev_tx_2:
        #on verifie que le msg a été recu
        for recep in list_ev_rx_1:
            if (int(recep.asn) == int(trans.asn)):
                trans.recu = 1
    
    #pour chaque elmt transmit on ne selectionne que ceux qui proviennent du noeud
    #et ceux qui sont dans l'intervalle Dasn
    #pour le noeud 1 vers 2
    while (asn_debut < asn_fin):
        del list_ev[:]
        list_ev = []
        for event in list_ev_tx_1:
            if (int(event.asn) < (asn_debut + Dasn) and int(event.asn) >= asn_debut):
                list_ev.append(event.recu)
        if list_ev:
            taux_transm_1.append(np.sum(list_ev)/len(list_ev))
        else:
            taux_transm_1.append(-1.)
        asn_debut = asn_debut + step
        
    #pour le noeud 2 vers 1
    asn_debut = 0
    while (asn_debut < asn_fin):
        del list_ev[:]
        list_ev = []
        for event in list_ev_tx_2:
            if (int(event.asn) < (asn_debut + Dasn) and int(event.asn) >= asn_debut):
                list_ev.append(event.recu)
        if list_ev:
            taux_transm_2.append(np.sum(list_ev)/len(list_ev))
        else:
            taux_transm_2.append(-1.)
        asn_debut = asn_debut + step
              
    return taux_transm_1, taux_transm_2

#calcul le taux de transmission vu par le noeud emeteur (addr1)
def transmission_ratio_flow_node(addr_1, addr_2, Dasn, step):
    asn_debut = 0
    #liste_ev ne comprend que les elemt qui sont dans la fenetre asn 
    list_ev = []
    #liste des msg envoyés entre noeud1 et 2
    list_ev_tx = []
    #resultat
    taux_transm=[]
    
    #on recupere les envois
    with open("data/parsed/event/data_STAT_PK_TX.log", "r") as f_tx:
        for line in f_tx:
            if (addr_1 == get_addr(line) and get_l2Dest(line).endswith(addr_2)):
                list_ev_tx.append(make_event_PK_TX(get_time(line), 
                                                           get_addr(line), 
                                                           get_comp(line), 
                                                           get_asn(line), 
                                                           get_statType(line), 
                                                           get_trackinstance(line), 
                                                           get_trackowner(line), 
                                                           get_length(line), 
                                                           get_frameType(line), 
                                                           get_slotOffset(line), 
                                                           get_frequency(line), 
                                                           get_l2Dest(line), 
                                                           get_txpower(line), 
                                                           get_numTxAttempts(line),
                                                           get_queuePos(line),
                                                           0.))
        asn_fin = int(get_asn(line))
    
    #on verifie si ces msgs ont été recus
    with open("data/parsed/event/data_STAT_ACK_RX.log", "r") as f_rx:
        for line in f_rx:
            for trans in list_ev_tx:
                #si le noeud a recu un ack a cet asn
                if (get_addr(line) == addr_1 and get_asn(line) == trans.asn):
                    trans.recu=1.
                
    #pour chaque elmt transmit on ne selectionne que ceux qui proviennent du noeud
    #et ceux qui sont dans l'intervalle Dasn
    while (asn_debut < asn_fin):
        del list_ev[:]
        list_ev = []
        for event in list_ev_tx:
            if (int(event.asn) < (asn_debut + Dasn) and int(event.asn) > asn_debut):
                list_ev.append(event.recu)
        if list_ev:
            taux_transm.append(np.sum(list_ev)/len(list_ev))
        else:
            taux_transm.append(-1.)
        asn_debut = asn_debut + step
              
    return taux_transm



#obtenir le taux de transm a un asn donné | asn_data  | Dasn est la fenetre pour laquelle on calcule le taux (0 si on veux le savoir pour un seul msg)
#le taux est de -1 si aucun msg n'a été envoyés 
#prend en entré PT_OF_VIEW_NODE qui est vrai si on se restraint aux msg dont le noeud recois les aquittements
def get_ratio_trans_node(addr_1, addr_2, asn_data, Dasn, PT_OF_VIEW_NODE=False):
    #liste des msg envoyés entre noeud1 et 2 | qui appartienent a: [asn_data-Dasn; asn_data]
    list_ev_tx = []
    del list_ev_tx[:]
    #contient 0 ou 1 si le msg est recu
    list_recu_tx = [] 
    del list_recu_tx[:]
    #resultat
    taux_transm = -1
    
    #on recupere les envois
    with open("data/parsed/event/data_STAT_PK_TX.log", "r") as f_tx:
        for line in f_tx:
            if (addr_1 == get_addr(line) and get_l2Dest(line).endswith(addr_2)
               and int(get_asn(line)) >= (asn_data-Dasn) and int(get_asn(line)) <= asn_data):
                list_ev_tx.append(make_event_PK_TX(get_time(line), 
                                                           get_addr(line), 
                                                           get_comp(line), 
                                                           get_asn(line), 
                                                           get_statType(line), 
                                                           get_trackinstance(line), 
                                                           get_trackowner(line), 
                                                           get_length(line), 
                                                           get_frameType(line), 
                                                           get_slotOffset(line), 
                                                           get_frequency(line), 
                                                           get_l2Dest(line), 
                                                           get_txpower(line), 
                                                           get_numTxAttempts(line),
                                                           get_queuePos(line),
                                                           0.))
    # si il y a eu des msg envoyés
    if list_ev_tx:
        if PT_OF_VIEW_NODE == True:
            #on verifie si ces msgs ont été recus | VUE PAR LE NOEUD
            with open("data/parsed/event/data_STAT_ACK_RX.log", "r") as f_rx:
                for line in f_rx:
                    #on sort de la boucle si on a depasser l'asn pour economiser du temps  
                    if (int(get_asn(line)) > int(list_ev_tx[-1].asn)):
                        break
                    for trans in list_ev_tx:
                        #si le noeud a recu un ack a cet asn
                        if (get_addr(line) == addr_1 and get_asn(line) == trans.asn):
                            trans.recu=1.
        else:
            #on verifie si ces msgs ont été recus | VUE PAR LA RECEPTION DU MSG
            with open("data/parsed/event/data_STAT_PK_RX.log", "r") as f_rx:
                for line in f_rx:
                    #on sort de la boucle si on a depasser l'asn pour economiser du temps  
                    if (int(get_asn(line)) > int(list_ev_tx[-1].asn)):
                        break
                    for trans in list_ev_tx:
                        #si le dest a recu un msg a ce moment
                        if (get_addr(line) == addr_2 and get_l2Src(line).endswith(addr_1) and 
                            get_asn(line) == trans.asn):
                            trans.recu=1.
    
    
    #on calcule le taux
    if list_ev_tx:                
        for elm in list_ev_tx:
            list_recu_tx.append(elm.recu)
        
        taux_transm = np.sum(list_recu_tx)/len(list_recu_tx)
        
    
    return taux_transm
    

    
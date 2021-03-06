# -*-coding:Latin-1 -*

import re
import pandas as pd
from func_def_class import *
import ast




# crée un df avec les reservations
def create_df_res(data_file):
    list_res = []
    del list_res[:]
    #nombre de reservations simultanées | NE FONCTIONNE PAS ET EST GEREE PAR UNE AUTRE FONCTION
    simult = 0

    #### ETATs : 1=linkreq enqued | 3=linkreq send/rcvd  |  4=linkrep send/recvd -> RES REUSSIE
    ###   -1=linkreq failed |  -2=linkrep failed  |  -3 timeout

    numAttempts = 0
    ch_default = -1
    slot_default = -1
    succes_default = -1
    l_queuePos=[]
    #in_prog = 0 si aucune reservation n'est en cours | 1 sinon | ne sert a rien
    #in_progress = 0
    #liste des numero en cours
    i=[]
    del i[:]
    #liste des echecs successifs | contient des couples id res fail, numAtt
    fail_list=[]
    del fail_list[:]
    fail_list_tmp=[]
    del fail_list_tmp[:]
    #id de la reservation
    id_res = 0
    debug_cont = 0
    #src et dest tmp pour la mise a jour des numAtt en cas de réussite | succes_tmp 
    dest_tmp = ""
    src_tmp=""
    succes_tmp=0
    #liste temporaire pour la mise a jour des positions dans la queue des etapes
    queue_tmp = []
    #liste pour les chanelsXslot de pris | au debut rien n'est occupé
    chsl_busy = []
    del chsl_busy[:]
    #liste d'asn pour voir les asn des differentes etapes
    l_asn = []
    del l_asn[:]
    asn_tmp = []
    del asn_tmp[:]

    with open(data_file) as origin_file:
        for line in origin_file:

            if "LinkReq enqueued" in line:
            # si enqueued, on créé une réservation. 
                asn = line[line.find("asn")+len("asn="):line.find(")", line.find("asn"))]
                src = line[line.find("from")+len("from "):line.find(":", line.find("from"))]
                dest = line[line.find("to ")+len("to "):line.find(",", line.find("to "))]
                queuePos = line[line.find("queuePos")+len("queuePos="):line.find(",", line.find("queuePos"))]
                owner = line[line.find("owner")+len("owner="):line.find(",", line.find("owner"))]

                #on réinitialise queuepos
                del l_queuePos[:]
                del l_asn[:]
                #
                ####    UPDATE NUMATTEMPTS
                #
                # si la res est nouvelle num att sera 1
                numAttempts = 0
                """
                #sinon si une res du meme type a été fait dans les 3 derniéres res et que elle a été raté (succes = 0)
                if list_res!=0:
                    for el in list_res[-2:]:
                        if src == list_res[elem].src and dest == list_res[elem].dest and owner == list_res[elem].owner and list_res[elem].succes == 0:
                            numAttempts = list_res[elem].numAttempts
                """
                #si une res similaire est dans la fail list on récupere le numAtt
                if fail_list!=0:
                    for elem in fail_list:
                        if src == list_res[elem[0]].src and dest == list_res[elem[0]].dest:
                            numAttempts = elem[1]

                #si une res du meme style existe deja -> on incrémente numAtte
                if i!=0:
                    for elem in i:
                        if src == list_res[elem].src and dest == list_res[elem].dest:
                            numAttempts = list_res[elem].numAttempts

                #l_queuePos.append(int(queuePos))
                #l_asn.append(int(asn))
                #print l_asn
                #on créé la reservation et on l'ajoute a la liste
                list_res.append(make_cell_reservation(id_res, l_asn, succes_default, numAttempts+1,
                                    simult, l_queuePos, slot_default, ch_default, src, dest,
                                    owner, 1))


                asn_tmp = list_res[-1].asn[:]
                asn_tmp.append(int(asn))
                list_res[-1].asn = asn_tmp[:]
                queue_tmp = list_res[-1].queuePos[:]
                queue_tmp.append(int(queuePos))
                list_res[-1].queuePos = queue_tmp[:]

                #quand une réservation est créée elle est ajoutée a la liste des element en cours
                i.append(id_res)
                simult+=1
                id_res+=1

                #on met a jour le nombre d'experice max simultanée
                if i!=0:
                    for elem in i:
                        if list_res[elem].simult < simult:
                            list_res[elem].simult = simult

                #
                #####    TEST  ON AJOUTE L'ELEM A LA FAIL LIST TANT QU'IL N'A PAS ETE RECU
                ##       LES RES QUI SONT FAITE ALORS QU'UNE RES SIMILAIRE EST EN COURS AURONT
                ##       NUM ATT +1 MEME SI LA 1ere RES MARCHE

                ##      ON N'AJOUTE PAS LES RES DANS LA FAIL LIST SI ILS ONT ECHOUE (VOIR LINKREP/K FAIL)
                #

                ##fail_list.append([elem,list_res[elem].numAttempts])


            #si le linkreq fail
            if "LinkReq failed" in line and i!=0:

                asn = line[line.find("asn")+len("asn="):line.find(")", line.find("asn"))]
                src = line[line.find("from")+len("from "):line.find(":", line.find("from"))]
                dest = line[line.find("to ")+len("to "):line.find(",", line.find("to "))]
                queuePos = line[line.find("queuePos")+len("queuePos="):line.find(" ", line.find("queuePos"))]


                #pour les reservations en cours on verifie laquelle a échouée
                for elem in i:
                    if src == list_res[elem].src and dest == list_res[elem].dest and list_res[elem].state==1:
                        list_res[elem].succes = 0
                        list_res[elem].state = -1
                        queue_tmp = list_res[elem].queuePos[:]
                        queue_tmp.append(int(queuePos))
                        list_res[elem].queuePos = queue_tmp[:]
                        asn_tmp = list_res[elem].asn[:]
                        asn_tmp.append(int(asn))
                        list_res[elem].asn = asn_tmp[:]
                        #on retire l'element de la liste des reservation en cours
                        i.remove(elem)
                        #on réduit le nb de res en cours
                        simult-=1
                        #on ajoute l'id de l'element qui a echoué dans fail list
                        fail_list.append([elem,list_res[elem].numAttempts])
                        #on sort de la boucle, car la reservation concernée est deja traitée
                        break


            # on considère que si le link req est txed il est rcvd
            """
            #si le linkreq est envoyé et qu'il y a une réservation en cours (sinon c'est un bug)
            if "LinkReq txed" in line and i!=0:
                asn = line[line.find("asn")+len("asn="):line.find(")", line.find("asn"))]
                src = line[line.find("from")+len("from "):line.find(":", line.find("from"))]
                dest = line[line.find("to ")+len("to "):line.find(",", line.find("to "))]

                #pour les reservations en cours on verifie laquelle est concernée
                for elem in i:
                    if src == list_res[elem].src and dest == list_res[elem].dest and list_res[elem].state==1:
                        #on met son état a 2
                        list_res[elem].state = 2
                        #on sort de la boucle, car la reservation concernée est deja traitée
                        break


            """    
            #si le linkreq est recu
            if "LinkReq rcvd" in line and i!=0:
                asn = line[line.find("asn")+len("asn="):line.find(")", line.find("asn"))]
                # la srce du linkrep est la dest des etapes 1/2 (on prend comme src la src de la res cad le 2eme from)
                src = line[line.find("from",line.find("from")+1)+len("from "):line.find(",", line.find("from",line.find("from")+1))]
                #dest de la res est la src du linkrep cad le 1er from
                dest = line[line.find("from")+len("from "):line.find(":", line.find("from"))]
                # le slot et le ch on été choisi, on les met a jour
                ch = line[line.find("ch ")+len("ch "):line.find(",", line.find("ch "))]
                slot = line[line.find("slot ")+len("slot "):line.find(",", line.find("slot "))]
                queuePos = line[line.find("queuePos")+len("queuePos="):line.find(",", line.find("queuePos"))]

                #pour les reservations en cours on verifie laquelle est concernée
                for elem in i:
                    # etat = 1 car on ne verifie pas l'envoi
                    if src == list_res[elem].src and dest == list_res[elem].dest and list_res[elem].state==1:
                        list_res[elem].state = 3
                        # on met a jour les infos slot et ch
                        list_res[elem].ch = ch
                        list_res[elem].slot = slot
                        queue_tmp = list_res[elem].queuePos[:]
                        queue_tmp.append(int(queuePos))
                        list_res[elem].queuePos = queue_tmp[:]
                        asn_tmp = list_res[elem].asn[:]
                        asn_tmp.append(int(asn))
                        list_res[elem].asn = asn_tmp[:]
                        #on sort de la boucle, car la reservation concernée est deja traitée
                        break   



            #si le linkreP est envoyé  |  = le linkrep est recu
            if "LinkRep txed" in line and i!=0:
                asn = line[line.find("asn")+len("asn="):line.find(")", line.find("asn"))]
                # la srce du linkrep est la dest des etapes 1/2 (on prend comme src la src de la res cad le to )
                src = line[line.find("to ")+len("to "):line.find(",", line.find("to "))]
                #dest de la res est la src du linkrep cad le from
                dest = line[line.find("from")+len("from "):line.find(":", line.find("from"))]
                queuePos = line[line.find("queuePos")+len("queuePos="):line.find(",", line.find("queuePos"))]
                #pour les reservations en cours on verifie laquelle est concernée
                for elem in i:
                    if src == list_res[elem].src and dest == list_res[elem].dest and list_res[elem].state==3:
                        list_res[elem].state = 4
                        queue_tmp = list_res[elem].queuePos[:]
                        queue_tmp.append(int(queuePos))
                        list_res[elem].queuePos = queue_tmp[:]
                        asn_tmp = list_res[elem].asn[:]
                        asn_tmp.append(int(asn))
                        list_res[elem].asn = asn_tmp[:]
                        #
                        #####   LA RESERVATION EST REUSSIE
                        #
                        list_res[elem].succes = 1
                        #on retire l'element de la liste des reservation en cours
                        i.remove(elem)
                        #il y a une res en cours de moins
                        simult-=1

                        #on réinitialise la liste temporaire
                        del fail_list_tmp[:]
                        #on retire l'elem de fail_list si il s'agit d'un res qui avais echoué
                        for el in fail_list:
                            if list_res[el[0]].dest == dest and list_res[el[0]].src == src:
                                pass
                            else:
                                fail_list_tmp.append(el)
                        fail_list = fail_list_tmp

                        #on met succes_tmp a 1 le temp de mettre a jour les numatt
                        succes_tmp=1
                        dest_tmp = dest
                        src_tmp = src

                        # on rempli la liste des slot/chanel
                        chsl_busy.append([list_res[elem].ch, list_res[elem].slot])

                        #on sort de la boucle, car la reservation concernée est deja traitée
                        break   

                if succes_tmp == 1:
                # on réinitialise le num Att des elements de la liste en cours
                    numAttempts=1
                    for el in i:
                        if src_tmp == list_res[el].src and dest_tmp == list_res[el].dest:
                            list_res[el].numAttempts = numAttempts
                            numAttempts +=1
                    succes_tmp=0

            # Si le linkrep est txed il est recu
            """
            #si le linkreP est recu
            if "LinkRep rcvd" in line and i!=0:
                asn = line[line.find("asn")+len("asn="):line.find(")", line.find("asn"))]
                src = line[line.find("from")+len("from "):line.find(":", line.find("from"))]
                dest = line[line.find("from",line.find("from")+1)+len("from "):line.find(",", line.find("from",line.find("from")+1))]

                #pour les reservations en cours on verifie laquelle est concernée
                for elem in i:
                    if src == list_res[elem].src and dest == list_res[elem].dest and list_res[elem].state==4:
                        #on met son état a 5 | dernier etat possible -> la réservation est faite
                        list_res[elem].state = 5

                        #
                        #####   LA RESERVATION EST REUSSIE
                        # A VOIR POURQUOI LE LINKREP EST RECU AVANT D'ETRE ENVOYE

                        #list_res[elem].succes = 1
                        #on retire l'element de la liste des reservation en cours
                        #i.remove(elem)
                        #il y a une res en cours de moins
                        #simult-=1


                        #on sort de la boucle, car la reservation concernée est deja traitée
                        break   
            """

            # si le linkrep echoue
            if "LinkRep failed" in line and i!=0:
                asn = line[line.find("asn")+len("asn="):line.find(")", line.find("asn"))]
                src = line[line.find("to ")+len("to "):line.find(",", line.find("to "))]
                dest = line[line.find("from")+len("from "):line.find(":", line.find("from"))]
                queuePos = line[line.find("queuePos")+len("queuePos="):line.find(",", line.find("queuePos"))]

                #pour les reservations en cours on verifie laquelle est concernée
                for elem in i:
                    if src == list_res[elem].src and dest == list_res[elem].dest and list_res[elem].state==3:
                        list_res[elem].state = -2
                        list_res[elem].succes = 0
                        queue_tmp = list_res[elem].queuePos[:]
                        queue_tmp.append(int(queuePos))
                        list_res[elem].queuePos = queue_tmp[:]
                        asn_tmp = list_res[elem].asn[:]
                        asn_tmp.append(int(asn))
                        list_res[elem].asn = asn_tmp[:]
                        #on retire l'element de la liste des reservation en cours
                        i.remove(elem)
                        #il y a une res en cours de moins
                        simult-=1
                        fail_list.append([elem,list_res[elem].numAttempts])

                        #on sort de la boucle, car la reservation concernée est deja traitée
                        break


            ###     SUPPRIMER UNE RES SI ELLE EST EN COURS DEPUIS TROP LONGTEMPS
            #

            # Si une res est en attente depuis trop longtemps on la met en echec et on la supprime des res en cours
            asn = line[line.find("asn")+len("asn="):line.find(")", line.find("asn"))]
            for elem in i:
                #print type(list_res[elem].asn[0]), type(int(asn))
                if list_res[elem].asn[0] + 10000 <= int(asn):
                    #print "COUCOU"
                    list_res[elem].state = -3
                    list_res[elem].succes = 0
                    #on retire l'element de la liste des reservation en cours
                    i.remove(elem)
                    #il y a une res en cours de moins
                    simult-=1
                    fail_list.append([elem,list_res[elem].numAttempts])
                    #on sort de la boucle, car la reservation concernée est deja traitée
                    break

    
    
    i=0
    df = pd.DataFrame(columns=('asn', 'succes', 'numAttempts', 'simult_req', 'simult_rep', 'queuePos', 'slot', 'ch', 'src', 'dest', 'owner', 'state', 'info'))
    for elem in list_res:
        df.loc[i]=[elem.asn, 
                   elem.succes, 
                   elem.numAttempts, 
                   "", 
                   "", 
                   elem.queuePos, 
                   elem.slot, 
                   elem.ch, 
                   elem.src, 
                   elem.dest, 
                   elem.owner,
                   elem.state,
                  ""]
                   
        i+=1
    
    
    
    
    df.to_csv('data_csv/res.csv',index=False)
    
    
    
def print_res(res):
    if isinstance(res, Cell_Reservation):
        print "asn : ", res.asn
        print "dest : ", res.dest
        print "src : ", res.src
        print "numAtt", res.numAttempts
        print "succes : ", res.succes
    else:
        print "Ce n'est pas une réservation"
        
        
#fonction get simult df | entrée un df res tmp et df tx, en sortie une liste des simult
def get_simult_df(df_tmp, df_tx):
    liste_tmp = []
    del liste_tmp[:]
    i=0
    numAtt = 0
    simult = 0
    asn_tmp=0
    
    #si la liste tmp est vide, on retourne une liste vide. (ne devrait pas arriver)
    if df_tmp.empty:
        return liste_tmp
    #    liste_tmp.append(len(  df_tx.loc[ (df_tx['asn']==  df_tmp.iloc[-1]["asn"] )]  ))
    numAtt = df_tmp.iloc[-1]["numTxAttempts"]
    #SI il y a un mismatch dans les res -> par exemple que un pkt avec numAtt = 2/3/4 mais pas les precedent, on ne reonte pas
    if len(df_tmp) >= numAtt:
        for i in range(numAtt):
            asn_tmp = df_tmp.loc[  df_tx['numTxAttempts'] == numAtt-i   ]["asn"].iloc[-1]
            simult = len( df_tx.loc[ (df_tx['asn']==  asn_tmp )] )
            liste_tmp.append( simult )
    else:
        asn_tmp = df_tmp.loc[  df_tx['numTxAttempts'] == numAtt   ]["asn"].iloc[-1]
        simult = len( df_tx.loc[ (df_tx['asn']==  asn_tmp )] )
        liste_tmp.append( simult )
    liste_tmp.reverse()
    return liste_tmp


# si la res a marcher (etat == 4) -> les tx de paquets sont entre :
# linkreq - asn[0] et asn[1]
#linkrep - asn[1] et asn[2]

#simult est une liste qui prend comme elemts : [A,B] | A=liste:nb de tx simult lors de l'envois du linkreq
#B=liste:nb de tx simult pour linkrep
def fill_simult(df_res, df_tx):
    simult = []
    A=[]
    B=[]

    #data frame tmp 
    df_tmp = pd.DataFrame

    #pour A
    i=0
    for i in range(len(df_res)):
        if (df_res.loc[i]["state"] == "4") or (df_res.loc[i]["state"] == "-1") or (df_res.loc[i]["state"] == "-2"):
            df_tmp = df_tx.loc[ (df_tx['asn']<=ast.literal_eval(df_res.loc[i]["asn"])[1]) & 
                                (df_tx['asn']>=ast.literal_eval(df_res.loc[i]["asn"])[0]) &
                                (df_tx['addr']==df_res.loc[i]["src"]) &
                                (df_tx['l2Dest'].str.endswith(df_res.loc[i]["dest"])) &
                                (df_tx['frameType']=="IEEE154_TYPE_DATA") &
                                ((df_tx['trackinstance']=="4") | (df_tx['trackinstance']=="0") )]

            A = get_simult_df(df_tmp, df_tx)
            df_res.set_value(i,"simult_req", A)
        elif df_res.loc[i]["state"] == "-3":
            # pas assez d'info
            pass

    #pour B
    i=0
    for i in range(len(df_res)):
        if (df_res.loc[i]["state"] == "4") or (df_res.loc[i]["state"] == "-2"):
            df_tmp = df_tx.loc[ (df_tx['asn']<=ast.literal_eval(df_res.loc[i]["asn"])[2]) & 
                                (df_tx['asn']>=ast.literal_eval(df_res.loc[i]["asn"])[1]) &
                                (df_tx['addr']==df_res.loc[i]["src"]) &
                                (df_tx['l2Dest'].str.endswith(df_res.loc[i]["dest"])) &
                                (df_tx['frameType']=="IEEE154_TYPE_DATA") &
                                ((df_tx['trackinstance']=="4") | (df_tx['trackinstance']=="0") )]

            B = get_simult_df(df_tmp, df_tx)
            df_res.set_value(i,"simult_rep", B)
        elif df_res.loc[i]["state"] == "-3":
            # pas assez d'info
            pass

    df_res.to_csv('data_csv/res.csv',index=False)
    

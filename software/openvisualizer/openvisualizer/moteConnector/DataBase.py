# -*-coding:Latin-1 -*

import MySQLdb

class DataBase(object):

    def __init__(self, expid):

        self.expid = expid

        self.typedata = {
            1 : ["DATA_GENERATION", "addr", "comp", "asn", "trackInstance", "trackOwner", "seqNum", "l2Src", "l2Dest", "expid"],
            2 : ["DATA_RX", "addr", "comp", "asn", "trackInstance", "trackOwner", "seqNum", "l2Src", "l2Dest", "expid"],
            3 : ["PKT_TX", "addr", "comp", "asn", "trackInstance", "trackOwner", "length", "type", "slotOffset", "frequency", "l2Dest", "txPower", "numTxAttempts", "expid"],
            4 : ["PKT_RX", "addr", "comp", "asn", "trackInstance", "trackOwner", "length", "type", "slotOffset", "frequency", "l2Src", "rssi", "lqi", "crc", "expid"],
            5 : ["CELL_ADD", "addr", "comp", "asn", "trackInstance", "trackOwner", "slotOffset", "type", "shared", "channelOffset", "neighbor", "expid"],
            6 : ["CELL_REMOVE", "addr", "comp", "asn", "trackInstance", "trackOwner", "slotOffset", "type", "shared", "channelOffset", "neighbor", "expid"],
            7 : ["ACK_TX", "addr", "comp", "asn", "expid"],
            8 : ["ACK_RX", "addr", "comp", "asn", "expid"],
            9 : ["PKT_TIMEOUT", "addr", "comp", "asn", "trackInstance", "trackOwner", "length", "type", "slotOffset", "frequency", "l2Dest", "txPower", "numTxAttempts", "expid"],
            10 : ["PKT_ERROR", "addr", "comp", "asn", "trackInstance", "trackOwner", "length", "type", "slotOffset", "frequency", "l2Dest", "txPower", "numTxAttempts", "expid"],
            11 : ["PKT_BUFFEROVERFLOW", "addr", "comp", "asn", "trackInstance", "trackOwner", "length", "type", "slotOffset", "frequency", "l2Src", "rssi", "lqi", "crc", "expid"],
            12 : ["DIOTX", "addr", "comp", "asn", "expid"],
            13 : ["DAOTX", "addr", "comp", "asn", "parent", "expid"],
            14 : ["NODESTATE", "addr", "comp", "asn", "dutyCycleRatio", "numDeSync", "expid"]
        }

        self.typecolumn = {
            "addr" : "VARCHAR(20)",
            "comp" : "VARCHAR(30)",
            "asn" : "INT",
            "parent" : "VARCHAR(20)",
            "dutyCycleRatio" : "DOUBLE",
            "numDeSync" : "INT",
            "trackInstance" : "INT",
            "trackOwner" : "VARCHAR(20)",
            "seqNum" : "BIGINT",
            "l2Src" : "VARCHAR(20)",
            "l2Dest" : "VARCHAR(20)",
            "queuePos" : "INT",
            "slotOffset" : "INT",
            "type" : "VARCHAR(30)",
            "shared" : "INT",
            "channelOffset" : "INT",
            "neighbor" : "VARCHAR(20)",
            "txPower" : "INT",
            "numTxAttempts" : "INT",
            "frequency" : "INT",
            "rssi" : "INT",
            "lqi" : "INT",
            "crc" : "VARCHAR(5)",
            "length" : "INT",
            "expid" : "INT"
        }


        print ("Initialisation de la base de données...")

        self.config = {
          "user": "util", #yanis
          "passwd": "util", #g2s$&nm9qqk
          "host": "localhost", #130.79.48.108
          "db": "openwsn"
        }

        try:
            self.db = MySQLdb.connect(**self.config)

            self.cur = self.db.cursor()
        except MySQLdb.Error as err:
            print("Erreur : {0}".format(err))
            return

        self.cur.execute("SHOW TABLES")
        self.tables = self.cur

        for table_name in self.tables:
            table_name = str(table_name)
            table_name = table_name.replace("(", "")
            table_name = table_name.replace(")", "")
            table_name = table_name.replace(",", "")
            table_name = table_name.replace("'", "")
            print(table_name)

        for table_name in self.tables:
            table_name = str(table_name)
            table_name = table_name.replace("(", "")
            table_name = table_name.replace(")", "")
            table_name = table_name.replace(",", "")
            table_name = table_name.replace("'", "")
            dele = "DELETE FROM {} WHERE expid={}".format(table_name, self.expid)
            print(dele)
            self.cur.execute(dele)

        print("Base de données OK\n")


    def Store(self, type, data):
        # création d'une table avec colonnes correspondantes si inexistante
        crtable = """CREATE TABLE IF NOT EXISTS {}(""".format(self.typedata[type][0])
        for i in range (1, len(self.typedata[type])-1):
            crtable+="""{} {}, """.format(self.typedata[type][i], self.typecolumn[self.typedata[type][i]])
        crtable+="""{} {})""".format(self.typedata[type][len(self.typedata[type])-1], self.typecolumn[self.typedata[type][len(self.typedata[type])-1]])
        print(crtable)
        self.cur.execute(crtable)

        # insertion
        insert = """INSERT INTO {} (""".format(self.typedata[type][0])

        for i in range (1, len(self.typedata[type])-1):
            insert+="""{}, """.format(self.typedata[type][i])
        insert+="""{})""".format(self.typedata[type][len(self.typedata[type])-1])

        insert+=""" VALUES ("""
        for i in range(0, len(data)):
            if (self.typecolumn[self.typedata[type][i+1]] == "INT"):
                insert+="""{}, """.format(data[i])
            else:
                insert+="""'{}', """.format(data[i])

        insert+="""{})""".format(self.expid)

        print(insert)
        self.cur.execute(insert)

        self.db.commit()

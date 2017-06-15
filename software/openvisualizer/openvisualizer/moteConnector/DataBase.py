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

        self.config = {
          "user": "util",
          "passwd": "util",
          "host": "localhost",
          "db": "openwsn"
        }

        try:
            self.db = MySQLdb.connect(**self.config)
            self.cur = self.db.cursor()
        except MySQLdb.Error as err:
            print("/!\ Erreur : {0}".format(err))
            return

    def reinit(self):
        self.cur.execute("SHOW TABLES")
        self.tables = self.cur.fetchall()

        for table_name in self.tables:
            dele = "DELETE FROM {} WHERE expid={}".format(table_name[0], self.expid)
            self.cur.execute(dele)
            self.cur.execute("UNLOCK TABLES")
            self.db.commit()

    def update_pdr(self):
        print("APPEL")
        self.cur.execute("CREATE TABLE IF NOT EXISTS RT_STATS (pdr FLOAT, e2e FLOAT, JIndex FLOAT, expid INT)")
        self.cur.execute("DROP TABLE IF EXISTS PDR")
        self.cur.execute("CREATE TABLE IF NOT EXISTS PDR(pdr FLOAT, expid INT)")
        self.cur.execute("DELETE FROM RT_STATS WHERE expid = {}".format(self.expid))
        self.cur.execute("UNLOCK TABLES")

        # PDR
        self.cur.execute("SELECT COUNT(*) FROM DATA_GENERATION")
        count_gen = self.cur.fetchone()[0]
        self.cur.execute("SELECT COUNT(*) FROM DATA_RX")
        count_rx = self.cur.fetchone()[0]
        pdr = float(count_gen) / float(count_rx)
        self.cur.execute("INSERT INTO PDR (pdr) VALUES ({})".format(pdr))

        # E2E Delay
        self.cur.execute("SELECT asn, trackOwner, seqNum FROM DATA_RX")
        rx = self.cur.fetchall()

        cnt = 0
        e2e = 0

        for r in rx:
            asn = r[0]
            trackOwner = r[1]
            seqNum = r[2]

            self.cur.execute("SELECT COUNT(*) FROM DATA_GENERATION WHERE trackOwner='{}' AND seqNum={}".format(trackOwner, seqNum))
            count = self.cur.fetchone()[0]

            if (count > 0):
                self.cur.execute("SELECT asn FROM DATA_GENERATION WHERE trackOwner='{}' AND seqNum={}".format(trackOwner, seqNum))

                asn2 = self.cur.fetchone()[0]

                cnt+=1
                e2e += (asn-asn2)

        if (cnt > 0):
            e2e /= float(cnt)
        else:
            e2e = -1

        # Jain Index
        self.cur.execute("SELECT pdr FROM PDR")
        pdrl = self.cur.fetchall()

        self.cur.execute("SELECT COUNT(*) FROM PDR")
        c = self.cur.fetchone()

        haut = 0
        bas = 0

        for p in pdrl:
            haut += p[0]
            bas += p[0]**2

        haut = haut**2
        bas *= c[0]

        if (bas > 0):
            jindex = haut / bas
        else:
            jindex = -1

        # Stockage
        query = "INSERT INTO RT_STATS (pdr, e2e, JIndex, expid) VALUES ({}, {}, {}, {})".format(float(pdr), float(e2e), float(jindex), self.expid)
        print(query)
        self.cur.execute(query)

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

        self.cur.execute("UNLOCK TABLES")

        self.db.commit()

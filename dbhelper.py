# import sqlite3
import psycopg2
import os

class DBuser:
    def __init__(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    def setup(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = "CREATE TABLE IF NOT EXISTS userr (id INT PRIMARY KEY, rang INT)"
        cur = conn.cursor()
        cur.execute(stmt)
        conn.commit()

    def add_authuser(self,addinguser):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = ("INSERT INTO userr VALUES ((%s),1)"%(addinguser))
        cur = conn.cursor()
        cur.execute(stmt)
        conn.commit()

    def delete_authuser(self,deluser):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = "DELETE FROM userr WHERE id = %s"%(deluser)
        args = (deluser, )
        cur = conn.cursor()
        cur.execute(stmt, args)
        conn.commit()

    def get_authuser(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        stmt = "SELECT id FROM userr"

        cur.execute(stmt)
        return [x[0] for x in cur.fetchall()]

    def get_master(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        stmt = "SELECT id FROM userr WHERE rang = 2"

        cur.execute(stmt)
        return [x[0] for x in cur.fetchall()]

    def make_master(self,muser):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = "UPDATE userr SET rang = 2 WHERE id = %s"%(muser)
        cur = conn.cursor()
        cur.execute(stmt)
        conn.commit()

class DBbike:
    def __init__(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    def setup(self):

        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = "CREATE TABLE IF NOT EXISTS bike (bnr SERIAL PRIMARY KEY,status INT, lat real, long real,pw INT,userr INT,spender text)"
        
        cur = conn.cursor()
        cur.execute(stmt)
        conn.commit()

    def delete_bike(self,dbike):

        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = "DELETE FROM bike WHERE bnr = %s"%(dbike)

        cur = conn.cursor()
        cur.execute(stmt)
        conn.commit()

    def up_status1(self,sbike):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = "UPDATE bike SET status = 1 WHERE bnr = %s"%(sbike)

        cur = conn.cursor()
        cur.execute(stmt)
        conn.commit()

    def up_status0(self,sbike):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = "UPDATE bike SET status = 0 WHERE bnr = %s"%(sbike)

        cur = conn.cursor()
        cur.execute(stmt)
        conn.commit()

    def up_long(self,llong,sbike):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = ("UPDATE bike SET long = %f WHERE bnr = %s"%(llong,sbike))
        
        cur = conn.cursor()
        cur.execute(stmt)
        conn.commit()

    def up_lat(self,llat,sbike):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = ("UPDATE bike SET lat = %f WHERE bnr = %s"%(llat,sbike))
        
        cur = conn.cursor()
        cur.execute(stmt)
        conn.commit()

    def up_pw(self,ppw,sbike):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = ("UPDATE bike SET pw = %s WHERE bnr = %s",ppw,sbike)
        
        cur = conn.cursor()
        cur.execute(stmt)
        conn.commit()

    def up_user(self,uuser,sbike):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = ("UPDATE bike SET userr = %s WHERE bnr = %s"%(uuser,sbike))
        
        cur = conn.cursor()
        cur.execute(stmt)
        conn.commit()

    def add_bike(self,sstatus,llat,llong,ppw,sspender):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        sspender=("\'%s\'"%(sspender))
        stmt = ("INSERT INTO bike VALUES (DEFAULT,%s,%s,%s,%s,0,%s)"%(sstatus,llat,llong,ppw,sspender))
        
        cur = conn.cursor()
        cur.execute(stmt)
        conn.commit()

    def get_lat(self,sbike):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = ("SELECT lat FROM bike WHERE bnr=%s"% sbike)
        
        cur = conn.cursor()
        cur.execute(stmt)
        return [x[0] for x in cur.fetchall()]

    def get_long(self,sbike):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = ("SELECT long FROM bike WHERE bnr=%s"% sbike)

        cur = conn.cursor()
        cur.execute(stmt)
        return [x[0] for x in cur.fetchall()]

    def get_user(self,sbike):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = ("SELECT userr FROM bike WHERE bnr=%s"% sbike)
        
        cur = conn.cursor()
        cur.execute(stmt)
        return [x[0] for x in cur.fetchall()] 

    def get_bikes(self,uuser):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = ("SELECT bnr FROM bike WHERE userr=%s"% uuser)
        
        cur = conn.cursor()
        cur.execute(stmt)
        return [x[0] for x in cur.fetchall()] 

    def get_pw(self,sbike):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = ("SELECT pw FROM bike WHERE bnr=%s"% sbike)
        
        cur = conn.cursor()
        cur.execute(stmt)
        return [x[0] for x in cur.fetchall()] 

    def get_freebikes(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = ("SELECT bnr FROM bike WHERE status=1")
        
        cur = conn.cursor()
        cur.execute(stmt)
        return [x[0] for x in cur.fetchall()]  

    def get_allbikes(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        stmt = ("SELECT bnr FROM bike")

        cur = conn.cursor()
        cur.execute(stmt)
        return [x[0] for x in cur.fetchall()]  
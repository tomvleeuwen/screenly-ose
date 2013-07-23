
import sqlite3
from datetime import datetime



CREATE_TABLE="""CREATE TABLE IF NOT EXISTS pod (
                 uuid        TEXT     PRIMARY KEY UNIQUE, 
		 label TEXT,
                 destination TEXT, 
                 lastseen    DATETIME 
                 );"""


def initDB():
	global conn
	conn = sqlite3.connect('mothership.db', check_same_thread = False)
	c = conn.cursor()

	# Create table
	c.execute(CREATE_TABLE)

	# Save (commit) the changes	
	conn.commit()
	
def addEntry(uuid,dst):
	global conn
	timestamp=datetime.now()
	timestr=timestamp.strftime("%Y-%m-%d %H:%M:%S")
	cur = conn.cursor()
	cur.execute("INSERT OR REPLACE INTO pod(uuid,destination,lastseen) VALUES(?,?,?)", (str(uuid), str(dst),str(timestr)));
	conn.commit()


def updateLabel(uuid,label):
	global conn
	cur = conn.cursor()
	cur.execute("UPDATE pod SET label=? WHERE uuid=?", (str(label), str(uuid)));
	conn.commit()
	
def delete(uuid):
	global conn
	cur = conn.cursor()
	cur.execute("DELETE from pod WHERE uuid=?", ([uuid]));
	conn.commit()


def getAll():
	global conn
	cur = conn.cursor()
	cur.execute("SELECT uuid,label,destination,lastseen from pod");
	return cur.fetchall()
	
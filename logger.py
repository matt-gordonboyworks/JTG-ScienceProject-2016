import os
import time
import datetime
from pyfirmata import util, Arduino
import sqlite3

mydb_path = "JTGScience2016.db"

if not os.path.exists(mydb_path):
    db = sqlite3.connect(mydb_path)
    db.execute('''create table datalog(record_time text, voltage_solar real,
        current_solar real, voltage_wind real, current_wind real)''')
else:
    db = sqlite3.connect(mydb_path)

board = Arduino('/dev/ttyUSB0')
it = util.Iterator(board)
it.start()

v_solar = board.get_pin('a:0:i')
i_solar = board.get_pin('a:1:i')
v_wind = board.get_pin('a:2:i')
i_wind = board.get_pin('a:3:i')

while 1:
    cursor = db.cursor()
    v1 = v_solar.read()
    v2 = v_wind.read()
    i1 = i_solar.read()
    i2 = i_wind.read()
    t = time.time(),v1,i1,v2,i2
    print t
    #print 'Timestamp: {0}, Solar Voltage: {1}, Solar Current: {2}, Wind Voltage: {3}, Wind Current: {4}'.format(t)
    cursor.execute('''INSERT INTO datalog(record_time,voltage_solar,
        current_solar,voltage_wind,current_wind)
        VALUES(datetime('now'),?,?,?,?)''',
        (v1,i1,v2,i2))
    db.commit()
    time.sleep(5)

db.close()
board.exit()

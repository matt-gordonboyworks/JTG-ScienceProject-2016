import os
import time
import datetime
from pyfirmata import util, Arduino
import sqlite3

mydb_path = "/home/pi/JTGScience2016.db"

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
    print type(v_solar.read())
    cursor.execute('''INSERT INTO datalog(record_time,voltage_solar,
        current_solar,voltage_wind,current_wind)
        VALUES(datetime('now'),?,?,?,?)''',
        (v_solar.read(),i_solar.read(),v_wind.read(),i_wind.read()))
    db.commit()
    time.sleep(5)

db.close()
board.exit()

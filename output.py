import os
import sqlite3
import csv

mydb_path = "/home/pi/JTGScience2016.db"
myfile_path = "/home/pi/JTGScience2016.csv"

# if not os.path.exists(myfile_path):
#     myfile = open(myfile_path, 'a')
#     myfile.close()

db = sqlite3.connect(mydb_path)
cursor = db.cursor()
cursor.execute('select * from datalog')
with open(myfile_path, 'a') as out:
    fields = ['Record Time', 'Solar Voltage', 'Solar Current', 'Wind Voltage', 'Wind Current']
    writer = csv.writer(out,quoting=csv.QUOTE_MINIMAL)
    headers = ['Timestamp','Solar Voltage','Solar Current','Wind Voltage','Wind Current']
    writer.writerow(headers)
    for row in cursor:
        writer.writerow(row)

db.close()
out.close()

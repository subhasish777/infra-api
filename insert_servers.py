import sqlite3

connection = sqlite3.connect("servers.db")

cursor=connection.cursor()
'''
name = input("Enter server name: ")
ip = input("Enter IP address: ")
os = input("Enter operating system: ")




#cursor.execute(SQL, PARAMETERS)

cursor.execute("INSERT INTO servers (name,ip,os) VALUES(?,?,?)" , (name,ip,os) )

connection.commit()
'''
cursor.execute("Select * from servers")

rows=cursor.fetchall()

print(rows)
print("servers inserted successfully")

connection.close()
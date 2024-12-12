import sqlite3

conn = sqlite3.connect('D:\Wajith\Shirt Craft\shirtcraft.db')
c = conn.cursor()



print("Command executed successfully...")

conn.commit()
conn.close()

import sqlite3
connection = sqlite3.connect("yelp_sql/yelp_sql")
cursor = connection.cursor()

command = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='dbName' "


sql_command = """
CREATE TABLE employee (
staff_number INTEGER PRIMARY KEY,
fname VARCHAR(20),
lname VARCHAR(30),
gender CHAR(1),
joining DATE,
birth_date DATE);"""

cursor.execute(command)

print("\nfetch one:")
res = cursor.fetchone()
print(res)
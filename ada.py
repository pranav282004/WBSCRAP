import mysql.connector


data = [

]

for dd in range(1,200000):
    xy=[]
    xy.append("hgggggggggggggggggggggrtnhoooooooooooooooooo")
    xy.append("hufjfioeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeertiiir")
    data.append(tuple(xy))

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd="root",
    database = 'url_to_count_data'
)
cursor = db.cursor()
#cursor.execute("CREATE DATABASE url_to_count_data")
#cursor.execute("CREATE TABLE Data_ID (id int PRIMARY KEY AUTO_INCREMENT,URL VARCHAR(50),COUNT VARCHAR(50))")


stmt = "INSERT INTO Data_ID (URL,COUNT) VALUES (%s,%s)"
cursor.executemany(stmt, data)
db.commit()
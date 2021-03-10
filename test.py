import sqlite3


#db = sqlite3.connect('people.db')
#branch_name = 3456
#branch_code = 456
#branch_location = 4567

#db.execute("insert into branch(name , code , location) values (? , ? , ?)",(branch_name, branch_code, branch_location))
#db.commit()
#print('Branch Added')

from peewee import MySQLDatabase

db = MySQLDatabase('myapp', user='root', password='toor', host='localhost', port=3306)

mycurser = db.cursor("CREATE DATABASE testdb")
mycurser.execute("SHOW DATABASES")
for db in mycurser:
    print(db)

Client_Data = self.lineEdit_37.text()

    # عبدالرحمن لاحض هنا
        if self.comboBox_30.currentIndex() == 0 :
            print(0)
            sql = (''' SELECT * FROM clients WHERE name = %s ''')
            self.cur.execute(sql, [(Client_Data)])
            data = self.cur.fetchone()
            print(data)
        if self.comboBox_30.currentIndex() == 1 :
            print(1)
            sql = (''' SELECT * FROM clients WHERE mail = %s ''')
            self.cur.execute(sql, [(Client_Data)])
            data = self.cur.fetchone()
            print(data)
        if self.comboBox_30.currentIndex() == 2 :
            print(2)
            sql = (''' SELECT * FROM clients WHERE phone = %s ''')
            self.cur.execute(sql, [(Client_Data)])
            data = self.cur.fetchone()
            print(data)
        if self.comboBox_30.currentIndex() == 3 :
            print(3)
            sql = (''' SELECT * FROM clients WHERE national_id = %s ''')
            self.cur.execute(sql, [(Client_Data)])
            data = self.cur.fetchone()
            print(data)

        self.lineEdit_36.setText(data[1])
        self.lineEdit_35.setText(data[2])
        self.lineEdit_34.setText(data[3])
        self.lineEdit_46.setText(str(data[5]))
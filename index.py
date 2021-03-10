import datetime
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import QFileInfo
from PyQt5.uic import loadUiType
import sys
import MySQLdb
import sqlite3

# مكتبة ملف الاكسل
from xlsxwriter import *
from xlrd import *

MainUI,_ = loadUiType('untitled.ui')

class Main(QMainWindow, MainUI):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.UI_Changes()
        self.Db_Connect()
        self.Handel_Button()

        self.Retreive_Day_Work()

        #الصفحة الاولى
        self.Open_Daily_movements_Tab()

        self.Show_All_Category()
        self.Show_Brannchies()
        self.Show_Publishers()
        self.Show_Authors()
        self.Show_Employee()

        self.Show_All_Books()
        self.Show_All_CLients()

    #تغييرات واجهة المستخدم
    def UI_Changes(self):
        # UI Changes in Login
        self.tabWidget.tabBar().setVisible(False)

    #اتصال قاعدة البيانات
    def Db_Connect(self):
        #  Connection between app and Database
        self.db = sqlite3.connect('people.db')
        self.db = MySQLdb.connect(host='localhost', user='root', password='toor', db='indexapp')
        self.cur = self.db.cursor()
        print('تم الاتصال بقاعدة البيانات')

    # ازرار التحكم
    def Handel_Button(self):
        # Handel All Buttons In Our App
        self.pushButton_37.clicked.connect(self.Open_Daily_movements_Tab)
        self.pushButton_30.clicked.connect(self.Open_Books_Tab)
        self.pushButton_15.clicked.connect(self.Open_Clients_Tab)
        self.pushButton_12.clicked.connect(self.Open_Dashboard_Tab)
        self.pushButton_13.clicked.connect(self.Open_History_Tab)
        self.pushButton_20.clicked.connect(self.Open_Reports_Tab)
        self.pushButton_21.clicked.connect(self.Open_Settings_Tab)

        self.pushButton.clicked.connect(self.Add_Branch)
        self.pushButton_3.clicked.connect(self.Add_Publisher)
        self.pushButton_2.clicked.connect(self.Add_Author)
        self.pushButton_4.clicked.connect(self.Add_Category)

        self.pushButton_17.clicked.connect(self.Add_Employee)
        self.pushButton_32.clicked.connect(self.Check_Employee_Data)
        self.pushButton_24.clicked.connect(self.Edit_Employee_Data)

        self.pushButton_10.clicked.connect(self.Add_New_Book)
        self.pushButton_26.clicked.connect(self.Add_New_CLient)

        self.pushButton_18.clicked.connect(self.Edit_Book_Search)
        self.pushButton_11.clicked.connect(self.Edit_Book)
        self.pushButton_19.clicked.connect(self.Delete_book)
        self.pushButton_38.clicked.connect(self.All_Books_Filter)
        self.pushButton_43.clicked.connect(self.Book_Export_Report)

        self.pushButton_28.clicked.connect(self.Edit_CLient_Search)
        self.pushButton_35.clicked.connect(self.Edit_CLient)
        self.pushButton_29.clicked.connect(self.Delete_CLient)
        self.pushButton_31.clicked.connect(self.All_CLients_Filter)
        self.pushButton_47.clicked.connect(self.Client_Export_Report)

        # TODAY page
        self.pushButton_9.clicked.connect(self.Handel_to_Day_Work)

        # Employee
        self.pushButton_5.clicked.connect(self.Add_Employee_Permissions)


    def Handel_Login(self):
        # Handel Login
        pass

    def Handel_Reset_Password(self):
        # Handel Reset Password
        pass

    ##################################################################
    # Today

    def Handel_to_Day_Work(self):
        # Handel to Day operations
        book_title = self.lineEdit_8.text()
        client_national_id = self.lineEdit_29.text()
        type = self.comboBox_11.currentIndex()
        from_date = str(datetime.date.today())
        # to_date = self.dateEdit_4.date()
        to_date = str(datetime.date.today())
        date = datetime.datetime.now()
        branch = 1
        employee = 1
        self.cur.execute("""
            INSERT INTO daily_movements(book_id , client_id , type,date,branch_id,book_from , book_to , employee_id) 
            VALUES(  %s ,  %s ,  %s ,  %s ,  %s ,  %s ,  %s ,  %s )
            """,(book_title,client_national_id,type,date,branch,from_date,to_date,employee))
        self.db.commit()
        print('done')
        self.Retreive_Day_Work()

    def Retreive_Day_Work(self):
        self.cur.execute("""
            SELECT book_id, type, client_id , book_from , book_to FROM  daily_movements
            """)
        data = self.cur.fetchall()
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.insertRow(0)
        for row, form in enumerate(data):
            for column , item in enumerate(form):
                if column == 1:
                    if item == 0 :
                        self.tableWidget_4.setItem(row, column, QTableWidgetItem(str("Rent")))
                    else:
                        self.tableWidget_4.setItem(row, column, QTableWidgetItem(str("Retrieve")))
                elif column == 0:
                    sql = """ SELECT title FROM  books WHERE barcod = %s """
                    self.cur.execute(sql, [(item)])
                    barcod_name = self.cur.fetchone()
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(barcod_name[0])))

                elif column == 2:
                    sql = """ SELECT name  FROM  clients WHERE national_id = %s """
                    self.cur.execute(sql, [(item)])
                    client_name = self.cur.fetchone()
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(client_name[0])))
                else:
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_position)

    ##############################################################
    #Books
    def Show_All_Books(self):
        # Show All Books
        self.tableWidget_7.setRowCount(0)
        self.tableWidget_7.insertRow(0)
        self.cur.execute(
            '''
            SELECT code, title, category_id, author_id, publisher_id, price FROM  books
            '''
        )
        data = self.cur.fetchall()
            ## row = iteration , form = mdata
        sum = 0
        for row , form in enumerate(data):
            for column, item in enumerate(form):
                if column == 5 :
                    sum = sum + item
                if column == 2:
                    sql = """ SELECT category_name FROM  category WHERE category_name = %s  """
                    self.cur.execute(sql, [(item)])
                    category_name = self.cur.fetchone()
                    self.tableWidget_7.setItem(row, column, QTableWidgetItem(str(category_name[0])))
                    # يستخدم هذا الكود في حالة ارجاع الاندكس
                #elif column == 3:
                 #   sql = """ SELECT name FROM  author WHERE name = %s  """
                 #   self.cur.execute(sql, [(item)])
                 #   author_name = self.cur.fetchone()
                 #   self.tableWidget_7.setItem(row, column, QTableWidgetItem(str(author_name[0])))
                #elif column == 4:
                 #   sql = """ SELECT name FROM  puplisher WHERE name = %s  """
                 #   self.cur.execute(sql, [(item)])
                 #   puplisher_name = self.cur.fetchone()
                 #   self.tableWidget_7.setItem(row, column, QTableWidgetItem(str(puplisher_name[0])))
                else:
                    self.tableWidget_7.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget_7.rowCount()
            self.tableWidget_7.insertRow(row_position)

        row += 1
        self.tableWidget_7.setItem(row, 2, QTableWidgetItem(str('Total Price')))
        self.tableWidget_7.setItem(row, 3, QTableWidgetItem(str(sum)+str(' ريال ')))

    def All_Books_Filter(self):
        self.tableWidget_7.setRowCount(0)
        self.tableWidget_7.insertRow(0)
        book_title = self.lineEdit_19.text()
        category = self.comboBox_12.currentText()
        sql = """ SELECT code, title, category_id, author_id, publisher_id, price FROM  books WHERE title = %s  """ # category_id = %s
        self.cur.execute(sql, [(book_title)]) #, category
        data = self.cur.fetchall()
        sum = 0
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                if column == 5 :
                    sum = sum + item
                if column == 2:
                    sql = """ SELECT category_name FROM  category WHERE category_name = %s  """
                    self.cur.execute(sql, [(item)])
                    category_name = self.cur.fetchone()
                    self.tableWidget_7.setItem(row, column, QTableWidgetItem(str(category_name[0])))
                    # elif column == 3:
                    #   sql = """ SELECT name FROM  author WHERE name = %s  """
                    #   self.cur.execute(sql, [(item)])
                    #   author_name = self.cur.fetchone()
                    #   self.tableWidget_7.setItem(row, column, QTableWidgetItem(str(author_name[0])))
                    # elif column == 4:
                    #   sql = """ SELECT name FROM  puplisher WHERE name = %s  """
                    #   self.cur.execute(sql, [(item)])
                    #   puplisher_name = self.cur.fetchone()
                    #   self.tableWidget_7.setItem(row, column, QTableWidgetItem(str(puplisher_name[0])))
                else:
                    self.tableWidget_7.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget_7.rowCount()
            self.tableWidget_7.insertRow(row_position)

        row += 1
        self.tableWidget_7.setItem(row, 2, QTableWidgetItem(str('Total Price')))
        self.tableWidget_7.setItem(row, 3, QTableWidgetItem(str(sum)))

    def Add_New_Book(self):
        # Add New Book
        book_title = self.lineEdit_11.text()
        book_desc = self.textEdit_3.toPlainText()
        book_category = self.comboBox_16.currentText()
        book_code = self.lineEdit_14.text()
        barcode = self.lineEdit_26.text()
        book_part_order = self.lineEdit_13.text()
        book_price = self.lineEdit_12.text()
        book_publisher = self.comboBox_13.currentText()
        book_auther = self.comboBox_14.currentText()
        book_status = self.comboBox_15.currentIndex()
        date = datetime.datetime.now()

        self.cur.execute(
            '''
            INSERT INTO  books(title, description, category_id, code, barcod, part_order,
             price, publisher_id, author_id,status, date ) 
            VALUES (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s )
            ''', (book_title, book_desc, book_category, book_code, barcode, book_part_order,
                  book_price, book_publisher, book_auther, book_status, date)
        )

        self.db.commit()
        self.Show_All_Books()
        self.statusBar().showMessage('تم أضافة معلومات الكتاب بنجاح')

    def Edit_Book_Search(self):
        # Edit Book
        book_code = self.lineEdit_15.text()

        sql = (
            '''
            SELECT * FROM books WHERE code = %s
            '''
        )
        self.cur.execute(sql, [(book_code)])
        data = self.cur.fetchone()

        print(data)
        self.lineEdit_18.setText(data[1])
        self.textEdit_4.setPlainText(data[2])
        self.comboBox_20.setCurrentText(str(data[10]))
        self.lineEdit_17.setText(str(data[6]))
        self.comboBox_17.setCurrentText(str(data[11]))
        self.comboBox_18.setCurrentText(str(data[12]))
        self.comboBox_19.setCurrentIndex(int(data[8]))
        self.lineEdit_16.setText(str(data[5]))

    def Edit_Book(self):
        book_title = self.lineEdit_18.text()
        book_desc = self.textEdit_4.toPlainText()
        book_category = self.comboBox_20.currentText()
        book_code = self.lineEdit_15.text()
        book_part_order = self.lineEdit_16.text()
        book_price = self.lineEdit_17.text()
        book_publisher = self.comboBox_17.currentText()
        book_auther = self.comboBox_18.currentText()
        book_status = self.comboBox_19.currentIndex()

        self.cur.execute (
            '''
            UPDATE books SET title = %s, description = %s, category_id = %s, code = %s, part_order = %s,
             price = %s, publisher_id = %s, author_id = %s, status = %s WHERE code = %s
            ''' , (book_title, book_desc, book_category, book_code, book_part_order,
                  book_price, book_publisher, book_auther, book_status,book_code)
        )

        self.db.commit()
        print('تم التعديل')

        self.statusBar().showMessage('تم تعديل معلومات الكتاب بنجاح')
        #QMessageBox.information(self, 'success', 'تم تعديل معلومات الكتاب بنجاح')
        self.Show_All_Books()

    def Delete_book(self):
        # Delete book from DB --> (Database)
        book_code = self.lineEdit_15.text()
        delete_massage = QMessageBox.warning(self, 'مسح معلومات الكتاب', "هل انت متاكد من مسح الكتاب ", QMessageBox.Yes, QMessageBox.No)
        if delete_massage == QMessageBox.Yes :
            self.cur.execute(''' DELETE FROM books WHERE code = %s ''', (book_code,))
            self.db.commit()
            self.statusBar().showMessage('تم حذف الكتاب بنجاح')
            self.Show_All_Books()
        elif delete_massage == QMessageBox.No:
            self.statusBar().showMessage('تم تم الغا عملية حذف الكتاب بنجاح')

    ###########################################################
    #CLients
    def Show_All_CLients(self):
        # Show All CLients
        self.tableWidget_8.setRowCount(0)
        self.tableWidget_8.insertRow(0)
        self.cur.execute(
            '''
            SELECT name, mail, phone, national_id, date FROM Clients 
            '''
        )
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col , item in enumerate(form):
                self.tableWidget_8.setItem(row, col , QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget_8.rowCount()
            self.tableWidget_8.insertRow(row_position)



    def All_CLients_Filter(self):
        self.tableWidget_8.setRowCount(0)
        self.tableWidget_8.insertRow(0)
        name_Client = self.lineEdit_44.text()

        sql =""" SELECT name, mail, phone, national_id, date FROM Clients  WHERE name = %s """
        self.cur.execute(sql, [(name_Client)])
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for column , item in enumerate(form):
                self.tableWidget_8.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget_8.rowCount()
            self.tableWidget_8.insertRow(row_position)

    def Add_New_CLient(self):
        # Add New CLients
        name = self.lineEdit_31.text()
        mail = self.lineEdit_32.text()
        phone = self.lineEdit_33.text()
        national_id = self.lineEdit_45.text()
        data = datetime.datetime.now()

        self.cur.execute(
            '''
            INSERT INTO Clients(name, mail, phone, national_id, date) VALUES(%s,%s,%s,%s,%s)
            ''',(name, mail, phone, national_id, data)
        )
        self.db.commit()
        self.statusBar().showMessage('تم تسجيل معلومات العميل بنجاح')
        self.Show_All_CLients()

    def Edit_CLient_Search(self):
        # Edit CLients
        Clinet_data = self.lineEdit_37.text()

        if self.comboBox_30.currentIndex() == 0 :
            sqr = (''' SELECT * FROM cLients WHERE name = %s ''')
            self.cur.execute(sqr, [(Clinet_data)])
            data = self.cur.fetchone()
        if self.comboBox_30.currentIndex() == 1 :
            sqr = (''' SELECT * FROM cLients WHERE mail = %s ''')
            self.cur.execute(sqr, [(Clinet_data)])
            data = self.cur.fetchone()
        if self.comboBox_30.currentIndex() == 2 :
            sqr = (''' SELECT * FROM cLients WHERE phone = %s ''')
            self.cur.execute(sqr, [(Clinet_data)])
            data = self.cur.fetchone()
        if self.comboBox_30.currentIndex() == 3 :
            sqr = (''' SELECT * FROM cLients WHERE national_id = %s ''')
            self.cur.execute(sqr, [(Clinet_data)])
            data = self.cur.fetchone()

        self.lineEdit_36.setText(data[1])
        self.lineEdit_35.setText(data[2])
        self.lineEdit_34.setText(data[3])
        self.lineEdit_46.setText(str(data[5]))

    def Edit_CLient(self):
        # Edit CLients
        Clinet_data = self.lineEdit_37.text()

        Clients_name = self.lineEdit_36.text()
        Clients_mail = self.lineEdit_35.text()
        Clients_phone = self.lineEdit_34.text()
        Clients_national_id = self.lineEdit_46.text()
        if self.comboBox_30.currentIndex() == 0 :
            self.cur.execute('''
                        UPDATE clients SET name=%s , mail=%s , phone=%s , national_id=%s WHERE name = %s 
                    ''', (Clients_name, Clients_mail, Clients_phone, Clients_national_id, Clinet_data))
        if self.comboBox_30.currentIndex() == 1 :
            self.cur.execute('''
                        UPDATE clients SET name=%s , mail=%s , phone=%s , national_id=%s WHERE mail = %s 
                    ''', (Clients_name, Clients_mail, Clients_phone, Clients_national_id,Clinet_data))
        if self.comboBox_30.currentIndex() == 2 :
            self.cur.execute('''
                        UPDATE clients SET name=%s , mail=%s , phone=%s , national_id=%s WHERE phone = %s 
                    ''', (Clients_name, Clients_mail, Clients_phone, Clients_national_id, Clinet_data))
        if self.comboBox_30.currentIndex() == 3 :
            self.cur.execute('''UPDATE clients SET name=%s , mail=%s , phone=%s , national_id=%s WHERE national_id = %s 
                      ''', (Clients_name, Clients_mail, Clients_phone, Clients_national_id, Clinet_data))
        self.db.commit()
        self.statusBar().showMessage('تم تعديل معلومات العميل بنجاح')
        self.Show_All_CLients()

    def Delete_CLient(self):
        # Delete CLients from DB --> (Database)
        Client_data = self.lineEdit_37.text()
        delete_massage = QMessageBox.warning(self, 'مسح معلومات الكتاب', "هل انت متاكد من مسح الكتاب ", QMessageBox.Yes,
                                             QMessageBox.No)
        if delete_massage == QMessageBox.Yes:
            if self.comboBox_30.currentIndex() == 0:
                sql = ('''DELETE FROM clients WHERE name = %s ''')
                self.cur.execute(sql, [(Client_data)])
            if self.comboBox_30.currentIndex() == 1:
                self.cur.execute('''
                            DELETE FROM clients WHERE mail = %s 
                        ''', (Client_data,))
            if self.comboBox_30.currentIndex() == 2:
                self.cur.execute('''
                            DELETE FROM clients WHERE phone = %s 
                        ''', (Client_data,))
            if self.comboBox_30.currentIndex() == 3:
                self.cur.execute('''DELETE FROM clients WHERE national_id = %s 
                          ''', (Client_data,))
            self.db.commit()
            self.statusBar().showMessage('تم حذف العميل بنجاح')
            self.Show_All_CLients()
        elif delete_massage == QMessageBox.No:
            self.statusBar().showMessage('تم تم الغا عملية حذف الكتاب بنجاح')

    ###########################################################
    # Dashboard

    ###########################################################
    # History

    def Show_History(self):
        # Show All History to The Admin
        pass

    ###########################################################
    # books Report
    def All_books_Report(self):
        #  Report for All Book
        pass

    def books_Filter_Report(self):
        # show  Report for Filter books
        pass

    def Book_Export_Report(self):
        # export books data to excel file
        self.cur.execute(
            '''
            SELECT code, title, category_id, author_id, price FROM  books
            '''
        )
        data = self.cur.fetchall()
        self.cur.execute(
            '''
            SELECT price FROM  books
            '''
        )
        data2 = self.cur.fetchall()

         # Pdf
        fn, _ = QFileDialog.getSaveFileName(self, 'Export PDF',None,'PDF file (.pdf);;All Files()')
        if fn != '':
            if QFileInfo(fn).suffix() == "":
                fn += '.pdf'
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            data2.document().print_(printer)

        excel_file = Workbook('books_Report.xlsx')
        sheet1 = excel_file.add_worksheet()
        sheet1.write(0, 0, "Book Code")
        sheet1.write(0, 1, "Book Title")
        sheet1.write(0, 2, "Category")
        sheet1.write(0, 3, "Author")
        sheet1.write(0, 4, "Price")

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1
        row_number = 1

        # كود من ابداعاتي لحساب مجموع المبيعات
        sum = 0
        for row in data2:
            column_number = 0
            for item in row:
                sum = sum + item
                column_number += 1
            row_number += 1
        row_number += 1
        sheet1.write(row_number, 0, "Total")
        sheet1.write(row_number, 1, str(sum))
        #

        excel_file.close()
        self.statusBar().showMessage('تم إنشاء التقرير بنجاح بنجاح')

    ###############################################
    ###############################################
    def All_Client_Report(self):
        #  Report for All Client
        pass

    def Client_Filter_Report(self):
        # show  Report for Filter Client
        pass

    def Client_Export_Report(self):
        # export Client data to excel file
        self.cur.execute(
            '''
            SELECT name, mail, phone, national_id, date FROM Clients
            '''
        )
        data = self.cur.fetchall()
        excel_file = Workbook('Clients_Report.xlsx')
        sheet1 = excel_file.add_worksheet()
        sheet1.write(0, 0, "Client Name")
        sheet1.write(0, 1, "Client Mail")
        sheet1.write(0, 2, "Client Phone")
        sheet1.write(0, 3, "Client ID")
        sheet1.write(0, 4, "Client Date")

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1

        # row_number += 1
        # sheet1.write(row_number, 0, "Total")

        excel_file.close()
        self.statusBar().showMessage('تم إنشاء التقرير بنجاح بنجاح')

    ################################################
    ################################################
    def Monthly_Report(self):
        # Show one Month Report
        pass

    def Monthly_Report_Export(self):
        # export Monthly data to excel file
        pass

    ###########################################################
    #  Settings
    def Add_Branch(self):
        # Add new branch
        branch_name = self.lineEdit.text()
        branch_code = self.lineEdit_2.text()
        branch_location = self.lineEdit_3.text()
        #mysql
        self.cur.execute(''' INSERT INTO branch(name , code , location) VALUES (%s , %s , %s)
        ''',(branch_name, branch_code, branch_location))
        #sqlite3
        #self.cur.execute("INSERT into branch(name , code , location) values (? , ? , ?)",(branch_name, branch_code, branch_location))
        self.db.commit()
        print('Branch Added')
        self.Show_Brannchies()

    def Add_Category(self):
        # Add new categry
        category_name = self.lineEdit_6.text()
        parent_category_Text = self.comboBox.currentText()

        #query = ''' SELECT id FROM  category WHERE category_name = %s'''
        #self.cur.execute(query, [(parent_category_Text)])
        #data = self.cur.fetchone()
        #parent_category = data[0]

        self.cur.execute(''' INSERT INTO category(category_name, parent_category) VALUES (%s, %s)
                ''', (category_name, parent_category_Text))
        self.db.commit()
        print('Category Added')
        self.Show_All_Category()

    def Add_Publisher(self):
        # add new Publisher
        puplisher_name = self.lineEdit_7.text()
        puplisher_location = self.lineEdit_9.text()

        self.cur.execute(''' INSERT INTO Puplisher(name , location) VALUES ( %s , %s) ''', (puplisher_name, puplisher_location))
        #self.cur.execute("INSERT INTO Puplisher(name ,  location) VALUES (? , ?)",(puplisher_name, puplisher_location))
        self.db.commit()
        print('Publisher Added')
        self.Show_Publishers()

    def Add_Author(self):
        # Add new author
        author_name = self.lineEdit_4.text()
        author_location = self.lineEdit_5.text()

        self.cur.execute(''' INSERT INTO Author(name , location) VALUES ( %s , %s)
                ''', (author_name, author_location))
        #self.cur.execute("INSERT INTO Author(name  , location) VALUES (?,?)",(author_name, author_location))
        self.db.commit()
        print('Author Added')
        self.Show_Authors()

########################################################################
    #####################################################

    def Show_All_Category(self):
        self.comboBox_12.clear()
        self.comboBox.clear()
        self.comboBox_16.clear()
        self.comboBox_20.clear()
        self.cur.execute(
            '''
            SELECT category_name FROM category
            '''
        )
        categories = self.cur.fetchall()
        #print(categories)
        for category in categories:
            # حل من اغتراعي وشتغل بشكل صحيح
            # self.comboBox.addItems(categories[0])
            self.comboBox.addItem(str(category[0]))
            self.comboBox_16.addItem(category[0])
            self.comboBox_20.addItem(category[0])
            self.comboBox_12.addItem(category[0])

    def Show_Brannchies(self):
        self.comboBox_9.clear()
        self.comboBox_10.clear()
        self.cur.execute(
            '''
            SELECT name FROM Branch
            '''
        )
        branchies = self.cur.fetchall()
        for branch in branchies :
            self.comboBox_9.addItem(branch[0])
            self.comboBox_10.addItem(branch[0])

    def Show_Publishers(self):
        self.comboBox_13.clear()
        self.comboBox_17.clear()
        self.cur.execute(
            '''
            SELECT name FROM Puplisher
            '''
        )
        Publishers = self.cur.fetchall()
        for publish in Publishers:
            self.comboBox_13.addItem(publish[0])
            self.comboBox_17.addItem(publish[0])

    def Show_Authors(self):
        self.comboBox_18.clear()
        self.comboBox_14.clear()
        self.cur.execute(
            '''
            SELECT name FROM Author
            '''
        )
        Authors = self.cur.fetchall()
        for auther in Authors:
            self.comboBox_18.addItem(auther[0])
            self.comboBox_14.addItem(auther[0])

    def Show_Employee(self):
        self.comboBox_7.clear()
        self.cur.execute(
            '''
            SELECT name FROM employee
            '''
        )
        Authors = self.cur.fetchall()
        for employee in Authors:
            self.comboBox_7.addItem(employee[0])
    ###############################################
    ###############################################
    def Add_Employee(self):
        # add new employee
        employee_name = self.lineEdit_22.text()
        employee_mail = self.lineEdit_30.text()
        employee_phone = self.lineEdit_23.text()
        employee_branch = self.comboBox_9.currentIndex()
        employee_id = self.lineEdit_38.text()
        employee_periority = self.lineEdit_39.text()
        employee_password = self.lineEdit_40.text()
        employee_password_again = self.lineEdit_41.text()
        date = datetime.datetime.now()

        if employee_password == employee_password_again:
            self.cur.execute(
                '''
                INSERT INTO  employee(name, mail, phone, branch, national_id, date, periority, Password) 
                VALUES (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s )
                ''', (employee_name, employee_mail, employee_phone, employee_branch, employee_id, date,
                      employee_periority,employee_password)
            )
            self.db.commit()
            self.lineEdit_22.setText('')
            self.lineEdit_30.setText('')
            self.lineEdit_23.setText('')
            self.lineEdit_38.setText('')
            self.lineEdit_39.setText('')
            self.lineEdit_40.setText('')
            self.lineEdit_41.setText('')
            self.comboBox_10.setCurrentIndex(0)
            self.statusBar().showMessage('تم إضافة الموظف بنجاح')

        else:
            print('wrong Password ')

    def Check_Employee_Data(self):
        user = self.lineEdit_48.text()
        password = self.lineEdit_50.text()

        self.cur.execute(""" SELECT * FROM employee """)
        data = self.cur.fetchall()
        for row in data:
            if row[1] == user and row[7] == password:
                self.groupBox_12.setEnabled(True)
                self.lineEdit_52.setText(row[2])
                self.lineEdit_49.setText(row[3])
                self.comboBox_10.setCurrentIndex(row[8])
                self.lineEdit_53.setText(str(row[5]))
                self.lineEdit_54.setText(str(row[6]))
                self.lineEdit_55.setText(row[7])

    def Edit_Employee_Data(self):
        # edit employee data
        user = self.lineEdit_48.text()
        password = self.lineEdit_50.text()
        mail = self.lineEdit_52.text()
        phone = self.lineEdit_49.text()
        branch = self.comboBox_10.currentIndex()
        national_id = self.lineEdit_53.text()
        priority = self.lineEdit_54.text()
        password2 = self.lineEdit_55.text()
        date = datetime.datetime.now()

        if password == password2:
            self.cur.execute(
                '''
                UPDATE employee SET  mail = %s , phone = %s , date = %s , national_id = %s , 
                periority = %s , Password = %s  , branch = %s WHERE name = %s 
                ''', (mail, phone, date, national_id, priority, password2, branch, user)
            )
            self.db.commit()
            self.lineEdit_48.setText('')
            self.lineEdit_50.setText('')
            self.lineEdit_52.setText('')
            self.lineEdit_49.setText('')
            self.lineEdit_53.setText('')
            self.lineEdit_54.setText('')
            self.lineEdit_55.setText('')
            self.comboBox_10.setCurrentIndex(0)
            self.statusBar().showMessage('تم التعديل  معلومات الموظف بنجاح')
            self.groupBox_12.setEnabled(False)


    ###############################################
    ###############################################

    def Add_Employee_Permissions(self):
        # Add permissions to any employee
        employee_name = self.comboBox_7.currentText()

        if self.checkBox_30.isChecked() == True :
            self.cur.execute("""
                            INSERT INTO employee_permissions (employee_name, books_tab, clients_tab, dashboard_tab, history_tab, reports_tab, settings_tab,
                            add_book, edit_book, delete_book, import_book, export_book, 
                            add_client, edit_client, delete_client, import_client, export_client,
                            add_Branch, add_Publisher, add_Author, add_Category, add_Employee, edit_Employee, is_Admin )
                            VALUES (%s , %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s )
                        """, (
            employee_name, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
            self.db.commit()
            print('permission added')
            self.statusBar().showMessage('تم إضافة كل الصلاحيات للموظف المسؤل بنجاح')

        else:
            Books_tab = 0
            Clients_tab = 0
            Dashboard_tab = 0
            History_tab = 0
            Reports_tab = 0
            Settings_tab = 0

            add_Book = 0
            edit_Book = 0
            delete_Book = 0
            Import_Book = 0
            Export_Book = 0

            add_client = 0
            edit_client = 0
            delete_client = 0
            Import_client = 0
            Export_client = 0

            add_Branch = 0
            add_Publisher = 0
            add_Author = 0
            add_Category = 0
            add_Employee = 0
            edit_Employee = 0


            if self.checkBox_2.isChecked() == True :
                Books_tab = 1
            if self.checkBox_4.isChecked() == True :
                Clients_tab = 1
            if self.checkBox_7.isChecked() == True :
                Dashboard_tab = 1
            if self.checkBox_12.isChecked() == True :
                History_tab = 1
            if self.checkBox_13.isChecked() == True :
                Reports_tab = 1
            if self.checkBox_14.isChecked() == True :
                Settings_tab = 1

            if self.checkBox_6.isChecked() == True :
                add_Book = 1
            if self.checkBox.isChecked() == True :
                edit_Book = 1
            if self.checkBox_9.isChecked() == True :
                delete_Book = 1
            if self.checkBox_15.isChecked() == True :
                Import_Book = 1
            if self.checkBox_16.isChecked() == True :
                Export_Book = 1

            if self.checkBox_10.isChecked() == True :
                add_client = 1
            if self.checkBox_11.isChecked() == True :
                edit_client = 1
            if self.checkBox_8.isChecked() == True :
                delete_client = 1
            if self.checkBox_17.isChecked() == True :
                Import_client = 1
            if self.checkBox_18.isChecked() == True :
                Export_client = 1

            if self.checkBox_26.isChecked() == True :
                add_Branch = 1
            if self.checkBox_25.isChecked() == True :
                add_Publisher = 1
            if self.checkBox_24.isChecked() == True :
                add_Author = 1
            if self.checkBox_27.isChecked() == True :
                add_Category = 1
            if self.checkBox_28.isChecked() == True :
                add_Employee = 1
            if self.checkBox_29.isChecked() == True :
                edit_Employee = 1

            self.cur.execute("""
                INSERT INTO employee_permissions (employee_name, books_tab, clients_tab, dashboard_tab, history_tab, reports_tab, settings_tab,
                add_book, edit_book, delete_book, import_book, export_book, 
                add_client, edit_client, delete_client, import_client, export_client,
                add_Branch, add_Publisher, add_Author, add_Category, add_Employee, edit_Employee )
                VALUES (%s , %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s,%s )
            """, (employee_name , Books_tab, Clients_tab, Dashboard_tab, History_tab, Reports_tab, Settings_tab,
                  add_Book, edit_Book, delete_Book, Import_Book, Export_Book,
                  add_client, edit_client, delete_client, Import_client, Export_client,
                  add_Branch, add_Publisher, add_Author, add_Category, add_Employee, edit_Employee))
            self.db.commit()
            print('permission added')
            self.statusBar().showMessage('تم إضافة الصلاحيات للموظف بنجاح')


    ###############################################
    ###############################################

    def Admin_Report(self):
        # send report to the admin
        pass

    #############################################################



    #########################################################
    ######################################################
    ####################################################
    def Open_Login_Tab(self):
        self.tabWidget.setCurrentIndex(0)
    def Open_Reset_Password_Tab(self):
        self.tabWidget.setCurrentIndex(1)
    def Open_Daily_movements_Tab(self):
        self.tabWidget.setCurrentIndex(0)
    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_3.setCurrentIndex(0)
    def Open_Clients_Tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.tabWidget_5.setCurrentIndex(0)
    def Open_Dashboard_Tab(self):
        self.tabWidget.setCurrentIndex(5)
    def Open_History_Tab(self):
        self.tabWidget.setCurrentIndex(6)
    def Open_Reports_Tab(self):
        self.tabWidget.setCurrentIndex(7)
        self.tabWidget_6.setCurrentIndex(0)
    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_4.setCurrentIndex(0)


    ####################################################
def main():
    app = QApplication(sys.argv)
    windo = Main()
    windo.show()
    app.exec_()

if __name__ == '__main__':
    main()
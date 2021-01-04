import sys
import sqlite3
import pymongo
from bson.objectid import ObjectId
from pandas import DataFrame
import socket


from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QComboBox,
    QFormLayout,
    QLineEdit,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QCheckBox,
    QLabel,
    QSlider,
    QTableView,
    QAbstractScrollArea,
    QHeaderView
)

conn = sqlite3.connect(r"C:\Users\krist\OneDrive\Υπολογιστής\smarthome.db") #connect to local sqlite database
cursor = conn.cursor() #initialize cursor, used to execute queries
#conn.execute("PRAGMA foreign_keys = 1") #enforces referential integrity constraints

client = pymongo.MongoClient('localhost', 27017) #connect to local mongodb server
db = client['smarthome'] #connect to smarthome database

class TableModel(QAbstractTableModel): #defining abstract class which extends the model class used to fill the QTableView below, by including pandas capabilities

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    #Abstract methods defined so that they allow dataframe structure
    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role): #used to index rows and columns
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

    def sort(self, Ncol, order): #sorting 
        """Sort table by given column number.
        """
        try:
            self.layoutAboutToBeChanged.emit() #emite signal when header pressed
            self._data = self._data.sort_values(self._data.columns[Ncol], ascending=not order) #sort data by column selected
            self.layoutChanged.emit()
        except Exception as e: #thrown exception when data in column does not allow sorting
            print(e)


        
class Window2(QMainWindow): #window containing a QTableView with the commands history as data
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smarthome History")

        self.table = QTableView() #initialize table widget        
        sql   = ''' select date_time,username_pragma,eidos,dwmatio,command,command_id,device_id from 
                    ((pragmatopoiei join elegxei on elegxei.command_id_ele = pragmatopoiei.command_id_pragma) a1 
                    join syskeyi on a1.device_id_ele = syskeyi.device_id) a2 
                    join entoli on entoli.command_id = a2.command_id_ele
                    order by date_time desc '''#triple join of tables elegxei,syskeyi,entoli,pragmatopoiei to include all necessary data

        cursor.execute(sql) #execute query
        self.commands = cursor.fetchall() #save the query result
        
        history = [] #initialaze 2d data array that will be fed in the model
        
        for i in self.commands:
            
            instance = [i[0],i[1],i[2]+' '+i[3]] #initialize each row with the first 3 columns (datetime,username,appliance)
            appliance_commands = db['appliances'].find({'_id':ObjectId(i[6])})[0]['entoles'] #query appliances collection to find the appliance with the specified id
            
            for j in appliance_commands.keys(): #iterrate over thiw appliances commands
                if appliance_commands[j]['entolh_id'] == ObjectId(i[4]): #and once the command with the specified id is found add it to the data row (command column)
                    instance.append(j)

            instance.append(db['arxeio_entolwn'].find({"_id":ObjectId('0'*(24-len(str(i[5])))+str(i[5]))})[0]['parametroi']) #query arxeio_entolwn collection to find command with the specified command_id
            history.append(instance) #add row to data
            
        
        data = DataFrame(history, columns = ['Date/Time', 'Username', 'Appliance','Command','Parameters']) #use data to create dataframe

        self.model = TableModel(data) #feed dataframe to model
        self.table.setModel(self.model) #feed model to table

        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents) #adjust window size to table size
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.table.setSortingEnabled(True) #enable table sorting
        self.setCentralWidget(self.table)
    

class Window(QWidget): #main window of the application
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smarthome")
        
        cursor.execute("SELECT * FROM syskeyi") #query to get all appliances
        self.appliances = cursor.fetchall() #save them to appliances variable
        
        # Create a top-level layout
        layout = QVBoxLayout() #top level layout structured as a vertical box
        self.setLayout(layout) #set it as layout

        # Create the stacked layout
        self.stackedLayout = QStackedLayout() #rest of the app is structured as a stacked layout, many layouts one on top of the other with the ability to switch between them
        
        # Create the first page (select profile page)
        self.page1 = QWidget() #initialize the first page
        self.page1Layout = QFormLayout() #specify its layout

        self.new_button = QPushButton('Create new profile') #button, when pressed switches to create profile page
        self.page1Layout.addRow(self.new_button)
        self.new_button.clicked.connect(self.newProfile) 
        
        cursor.execute("SELECT * FROM 'profil_xristi';") #query to get all profiles
        self.profiles = cursor.fetchall() # save the to profiles variable
        
        for i in self.profiles: #for each profile create a button, switches to profile actions pages when pressed
            self.button = QPushButton(i[0])
            self.page1Layout.addRow(self.button)
            self.button.clicked.connect(self.selectProfile)

            
        self.page1.setLayout(self.page1Layout) 
        self.stackedLayout.addWidget(self.page1) #add layout to StackedLayout

        
        # Create the second page (enter password page)
        self.page2 = QWidget() #As above, those specific lines will be similar for each page 
        self.page2Layout = QFormLayout()

        self.password_field = QLineEdit() #LineEdit where user can type password
        self.page2Layout.addRow(self.password_field)

        self.label = QLabel() #Label used to show messages to user when password is incorrect
        self.page2Layout.addRow(self.label)
        
        self.button = QPushButton('Enter') #button, enters password
        self.page2Layout.addRow(self.button)
        self.button.clicked.connect(self.enterPassword)
        
        self.page2.setLayout(self.page2Layout)
        self.stackedLayout.addWidget(self.page2)

        # Create the third page as a new stacked layout(create new profile page)
        self.newProfilePage = QWidget() #the third page is structured as a second stacked layout, since both primary and secondary profile creations share actions
        self.newProfilePageLayout = QVBoxLayout()
        
        
        self.pageCombo = QComboBox() #ComboBox used to specify if user is creating a primary or secondary profile
        self.pageCombo.addItems(["Primary Profile", "Secondary Profile"])
        self.pageCombo.activated.connect(self.switchPage)

        self.new_username = QLineEdit() #user enters desired username
        self.new_username.setPlaceholderText("Enter username")
        self.new_password = QLineEdit() #user enters desired password
        self.new_password.setPlaceholderText("Enter password")
        self.new_alternative_password = QLineEdit() #user enters desired alternative password
        self.new_alternative_password.setPlaceholderText("Enter alternative password")
        self.isPublic = QCheckBox("Public") #checkbox, new profile is public when checked
        self.isMulti = QCheckBox("Multiple users") #checkbox, new profile supports multiple users when checked

        self.cancel_new_profile = QPushButton('Cancel') #cancel button, returns user to previous panel when pressed
        self.cancel_new_profile.clicked.connect(self.cancel_new)
        self.error_label = QLabel('')

        
        self.stackedLayout2 = QStackedLayout() #stacked layout portion of third page
        
        #page 1
        self.page3 = QWidget()
        self.page3Layout = QFormLayout()

        self.primary_profile_button = QPushButton('Enter') #nothing extra, besides enter button that saves the new primary profile
        self.page3Layout.addRow(self.primary_profile_button)
        self.primary_profile_button.clicked.connect(self.createPrimaryProfile)
        
        
        self.page3.setLayout(self.page3Layout)
        self.stackedLayout2.addWidget(self.page3)

        #page2
        self.page4 = QWidget()
        self.page4Layout = QFormLayout()

        cursor.execute("SELECT * FROM 'proteuon_profil';") #query returning all primary profiles
        masterprofiles = cursor.fetchall()
        
        self.master_profiles = QComboBox() #combo box containing all primary profile usernames
        self.master_profiles.addItems([i[0] for i in masterprofiles])
        self.page4Layout.addRow('Select master profile',self.master_profiles)
        
        self.secondary_profile_button = QPushButton('Enter')
        self.page4Layout.addRow(self.secondary_profile_button)
        self.secondary_profile_button.clicked.connect(self.createSecondaryProfile)
        
        self.page4.setLayout(self.page4Layout) # add stacked layout 2 to page 3 of stacked layout 1
        self.stackedLayout2.addWidget(self.page4)

        self.newProfilePage.setLayout(self.newProfilePageLayout) #add all widgets of top level layout of page 3
        self.newProfilePageLayout.addWidget(self.pageCombo)
        self.newProfilePageLayout.addWidget(self.new_username)
        self.newProfilePageLayout.addWidget(self.new_password)
        self.newProfilePageLayout.addWidget(self.new_alternative_password)
        self.newProfilePageLayout.addWidget(self.isPublic)
        self.newProfilePageLayout.addWidget(self.isMulti)
        self.newProfilePageLayout.addLayout(self.stackedLayout2)
        self.newProfilePageLayout.addWidget(self.cancel_new_profile)
        self.newProfilePageLayout.addWidget(self.error_label)
        self.stackedLayout.addWidget(self.newProfilePage)



        # Create the fourth page (select action page for primary profiles)
        self.page5 = QWidget()
        self.page5Layout = QFormLayout()

        #primary profiles have 4 available actions, manage restriction,use appliances,show consumption and show history, each of these button switches to corresponding action page
        self.manage_restrictions_button = QPushButton('Manage restrictions')
        self.page5Layout.addRow(self.manage_restrictions_button)
        self.manage_restrictions_button.clicked.connect(self.manage_restrictions)

        self.use_appliances_button = QPushButton('Use appliances')
        self.page5Layout.addRow(self.use_appliances_button)
        self.use_appliances_button.clicked.connect(self.use_appliances)

        self.consumption_button = QPushButton('Show consumption')
        self.page5Layout.addRow(self.consumption_button)
        self.consumption_button.clicked.connect(self.show_consumption)

        self.history_button = QPushButton('Show history')
        self.page5Layout.addRow(self.history_button)
        self.history_button.clicked.connect(self.show_history)

        self.delete_primary_button = QPushButton('Delete Profile')
        self.page5Layout.addRow(self.delete_primary_button)
        self.delete_primary_button.clicked.connect(self.delete_profile)

        self.exit_primary = QPushButton('Exit')
        self.page5Layout.addRow(self.exit_primary)
        self.exit_primary.clicked.connect(self.homepage)
        
        
        self.page5.setLayout(self.page5Layout)
        self.stackedLayout.addWidget(self.page5)

        # Create the fifth page (select action page for secondary profiles)
        self.page6 = QWidget() #a secondary profile can only use appliances, each profile has access to different appliances, therefore buttons are added afterwards when the profile is specified
        self.page6Layout = QFormLayout()

        self.page6.setLayout(self.page6Layout)
        self.stackedLayout.addWidget(self.page6)

        # Create the sixth page (manage restrictions page)
        self.page7 = QWidget()
        self.page7Layout = QFormLayout()
        
        self.child_profiles = QComboBox()
        self.page7Layout.addRow('Select child profile',self.child_profiles)
        self.child_profiles.activated.connect(self.child_restrictions)

        for i in self.appliances:
            self.appliance_checkbox = QCheckBox(i[1]+' '+i[2])
            self.page7Layout.addRow(self.appliance_checkbox)

        self.apply_restrictions_button = QPushButton('Apply restrictions')
        self.page7Layout.addRow(self.apply_restrictions_button)
        self.apply_restrictions_button.clicked.connect(self.apply_restrictions)

        self.reset_button = QPushButton('Reset changes')
        self.page7Layout.addRow(self.reset_button)
        self.reset_button.clicked.connect(self.reset_changes)

        self.cancel_restrictions_button = QPushButton('Cancel')
        self.page7Layout.addRow(self.cancel_restrictions_button)
        self.cancel_restrictions_button.clicked.connect(self.cancel_restrictions)
                
        self.page7.setLayout(self.page7Layout)
        self.stackedLayout.addWidget(self.page7)


        # Create the seventh page (primary appliances page)
        self.page8 = QWidget()
        self.page8Layout = QFormLayout()

        for i in self.appliances:
            self.appliance_button = QPushButton(i[1]+' '+i[2])
            self.page8Layout.addRow(self.appliance_button)
            self.appliance_button.clicked.connect(self.show_commands)

        self.exit_button = QPushButton('Exit')
        self.page8Layout.addRow(self.exit_button)
        self.exit_button.clicked.connect(self.cancel_restrictions)
        
        self.page8.setLayout(self.page8Layout)
        self.stackedLayout.addWidget(self.page8)

        # Create the eigth page (select appliance command)
        self.page9 = QWidget()
        self.page9Layout = QFormLayout()

        self.page9.setLayout(self.page9Layout)
        self.stackedLayout.addWidget(self.page9)

        # Create the ninth page (show appliance consumption)
        self.page10 = QWidget()
        self.page10Layout = QFormLayout()

        self.page10.setLayout(self.page10Layout)
        self.stackedLayout.addWidget(self.page10)

        # Create the tenth page (enter command parameters)
        self.page11 = QWidget()
        self.page11Layout = QFormLayout()

        self.page11.setLayout(self.page11Layout)
        self.stackedLayout.addWidget(self.page11)

        # Create the eleventh page (command history page)
        self.page12 = QWidget()
        self.page12Layout = QFormLayout()
        
        self.page12.setLayout(self.page12Layout)
        self.stackedLayout.addWidget(self.page12)
        
        # Add the combo box and the stacked layout to the top-level layout
        layout.addLayout(self.stackedLayout)

    def selectProfile(self):
        self.profile = self.sender().text()
        self.password_field.setPlaceholderText("Enter "+self.profile+" password")
        self.password_field.clear()
        self.stackedLayout.setCurrentIndex(1)

    def newProfile(self):
        self.stackedLayout.setCurrentIndex(2)

    def enterPassword(self):
        password = self.page2Layout.itemAt(0).widget().text()
        cursor.execute(f"SELECT kwdikos,alternative_password,dimosio FROM 'profil_xristi' WHERE username = '{self.profile}' ;")
        correct_password = cursor.fetchall()
        
        if password == correct_password[0][0] or password == correct_password[0][1] or correct_password[0][2]:
            self.label.setText('')
            
            cursor.execute(f"SELECT * FROM 'proteuon_profil' WHERE username_pro = '{self.profile}' ;")
            self.isPrimary = cursor.fetchall()
            if self.isPrimary:
                self.stackedLayout.setCurrentIndex(3)
            else:
                
                sql = f'''select exei_prosvasi.device_id,eidos,dwmatio,energi from exei_prosvasi join syskeyi on syskeyi.device_id=exei_prosvasi.device_id
                and username_prosvasis='{self.profile}';'''
                cursor.execute(sql)
                self.allowed_appliances = cursor.fetchall()

                for i in reversed(range(self.page6Layout.count())): 
                    self.page6Layout.itemAt(i).widget().setParent(None)
    
                if self.allowed_appliances:
                    for i in self.allowed_appliances:
                        self.appliance_button = QPushButton(i[1]+' '+i[2])
                        self.page6Layout.addRow(self.appliance_button)
                        self.appliance_button.clicked.connect(self.show_commands)


                self.delete_secondary_button = QPushButton('Delete Profile')
                self.page6Layout.addRow(self.delete_secondary_button)
                self.delete_secondary_button.clicked.connect(self.delete_profile)
        
                self.exit_secondary = QPushButton('Exit')
                self.page6Layout.addRow(self.exit_secondary)
                self.exit_secondary.clicked.connect(self.homepage)

                
                self.stackedLayout.setCurrentIndex(4)
            
        else:
            self.label.setText('Incorrect, try again or enter 2nd password')

    def switchPage(self):
        self.stackedLayout2.setCurrentIndex(self.pageCombo.currentIndex())

    def cancel_new(self):
        
        self.new_username.clear()
        self.new_password.clear()
        self.new_alternative_password.clear()
        
        self.stackedLayout.setCurrentIndex(0)

    def createPrimaryProfile(self):
        if self.new_username.text()!='' and ((self.new_password.text()!='') ^ self.isPublic.isChecked()):
            try:
                sql=f''' INSERT INTO proteuon_profil(username_pro)
                    VALUES('{self.new_username.text()}') '''
                cursor.execute(sql)

                cursor.execute('''INSERT INTO profil_xristi(username,kwdikos,alternative_password,dimosio,pollaplwn_xriston)
                    VALUES(?,?,?,?,?)''',(self.new_username.text(),self.new_password.text(),None if self.new_alternative_password.text()=='' else self.new_alternative_password.text(),self.isPublic.isChecked(),self.isMulti.isChecked()))

                conn.commit()

                self.button = QPushButton(self.new_username.text())
                self.page1Layout.addRow(self.button)
                self.button.clicked.connect(self.selectProfile)

                self.master_profiles.addItem(self.new_username.text())

                self.cancel_new()
                self.error_label.setText('')
            except Exception as e:
                self.error_label.setText('username already exists')

        else:
            self.error_label.setText('Username,password fields must be filled')


        

    def createSecondaryProfile(self):
        if self.master_profiles.currentText()!='':
            if self.new_username.text()!='' and ((self.new_password.text()!='') ^ self.isPublic.isChecked()):
                try:
                    sql=f''' INSERT INTO deutereuon_profil(username_de)
                        VALUES('{self.new_username.text()}') '''
                    cursor.execute(sql)

                    sql=f''' INSERT INTO parexei_dikaiwmata(primary_username,secondary_username)
                          VALUES('{self.master_profiles.currentText()}','{self.new_username.text()}') '''
                    cursor.execute(sql)

                    cursor.execute('''INSERT INTO profil_xristi(username,kwdikos,alternative_password,dimosio,pollaplwn_xriston)
                    VALUES(?,?,?,?,?)''',(self.new_username.text(),self.new_password.text(),None if self.new_alternative_password.text()=='' else self.new_alternative_password.text(),self.isPublic.isChecked(),self.isMulti.isChecked()))


                    conn.commit()

                    self.button = QPushButton(self.new_username.text())
                    self.page1Layout.addRow(self.button)
                    self.button.clicked.connect(self.selectProfile)
                    self.cancel_new()
                    self.error_label.setText('')
                    
                except Exception as e:
                    print(e)
                    self.error_label.setText('username already exists')
                    
            else:
                self.error_label.setText('Username,password fields must be filled')
        else:
            self.error_label.setText('No primary profile to set as master')
            

    def manage_restrictions(self):
        
        sql = f'''SELECT secondary_username FROM 'parexei_dikaiwmata' 
        WHERE primary_username='{self.profile}';'''
        cursor.execute(sql)
        self.childprofiles = cursor.fetchall()

        self.child_profiles.clear()
        self.child_profiles.addItems([i[0] for i in self.childprofiles])

        if self.childprofiles:
            for i in range(2,2+len(self.appliances)):
                sql = f'''SELECT * FROM exei_prosvasi 
                    WHERE username_prosvasis='{self.childprofiles[0][0]}' and device_id='{self.appliances[i-2][0]}';'''
                cursor.execute(sql)
                has_access = cursor.fetchall()
                if has_access:
                    self.page7Layout.itemAt(i).widget().setChecked(True)
                else:
                    self.page7Layout.itemAt(i).widget().setChecked(False)
                    
        self.stackedLayout.setCurrentIndex(5)

    def child_restrictions(self):
        for i in range(2,2+len(self.appliances)):
                sql = f'''SELECT * FROM exei_prosvasi 
                    WHERE username_prosvasis='{self.child_profiles.currentText()}' and device_id='{self.appliances[i-2][0]}';'''
                cursor.execute(sql)
                has_access = cursor.fetchall()
                if has_access:
                    self.page7Layout.itemAt(i).widget().setChecked(True)
                else:
                    self.page7Layout.itemAt(i).widget().setChecked(False)

    def apply_restrictions(self):
        if self.child_profiles.currentText()!='':
            for i in range(2,2+len(self.appliances)):
                sql = f'''SELECT * FROM exei_prosvasi 
                        WHERE username_prosvasis='{self.child_profiles.currentText()}' and device_id='{self.appliances[i-2][0]}';'''
                cursor.execute(sql)
                has_access = cursor.fetchall()
                if has_access:
                    if not self.page7Layout.itemAt(i).widget().isChecked():
                        sql=f''' DELETE FROM exei_prosvasi
                        WHERE username_prosvasis='{self.child_profiles.currentText()}' and device_id='{self.appliances[i-2][0]}';'''
                        cursor.execute(sql)
                else:
                    if self.page7Layout.itemAt(i).widget().isChecked():
                        sql=f''' INSERT INTO exei_prosvasi(username_prosvasis,device_id)
                        VALUES('{self.child_profiles.currentText()}','{self.appliances[i-2][0]}') '''
                        cursor.execute(sql)

            conn.commit()
        else:
            None

    def reset_changes(self):
        self.child_restrictions()

    def cancel_restrictions(self):
        self.stackedLayout.setCurrentIndex(3)

    def use_appliances(self):
        self.stackedLayout.setCurrentIndex(6)

    def homepage(self):
        self.stackedLayout.setCurrentIndex(0)

    def show_commands(self):
        a = self.sender()
        cntr=0

        if self.isPrimary:
            while True:
                if self.page8Layout.itemAt(cntr).widget() == a:
                    break
                cntr+=1

            self.appliance_id = self.appliances[cntr][0]
            self.appliance_isActive = self.appliances[cntr][3]
            self.entoles = db['appliances'].find({'_id':ObjectId(self.appliance_id)})[0]['entoles']
            
        else:
            while True:
                if self.page6Layout.itemAt(cntr).widget() == a:
                    break
                cntr+=1

            self.appliance_id = self.allowed_appliances[cntr][0]
            self.appliance_isActive = self.allowed_appliances[cntr][3]
            self.entoles = db['appliances'].find({'_id':ObjectId(self.appliance_id)})[0]['entoles']

        if self.appliance_isActive:
            self.entoles = {i:self.entoles[i] for i in self.entoles if i!='anapse'}
        else:
            self.entoles = {i:self.entoles[i] for i in self.entoles if i=='anapse'}
        
        for i in reversed(range(self.page9Layout.count())): 
            self.page9Layout.itemAt(i).widget().setParent(None)
        
        for i in self.entoles.keys():
            self.command_button = QPushButton(i)
            self.page9Layout.addRow(self.command_button)
            self.command_button.clicked.connect(self.save_command)

        self.exit_commands = QPushButton('Exit')
        self.page9Layout.addRow(self.exit_commands)
        self.exit_commands.clicked.connect(self.back_to_appliances)
        
        self.stackedLayout.setCurrentIndex(7)

    def back_to_appliances(self):
        if self.isPrimary:
            self.stackedLayout.setCurrentIndex(6)
        else:
            self.stackedLayout.setCurrentIndex(4)

    def save_command(self):
        a = self.sender()
        cntr=0

        while True:
            if self.page9Layout.itemAt(cntr).widget() == a:
                break
            cntr+=1

        entoli_name = list(self.entoles.keys())[cntr]
        entoli = self.entoles[entoli_name]

        if entoli_name == 'anapse':
            sql=f''' UPDATE syskeyi SET energi=true
                WHERE device_id = '{self.appliance_id}' '''
            cursor.execute(sql)

        elif entoli_name == 'sbhse':
            sql=f''' UPDATE syskeyi SET energi=false
                WHERE device_id = '{self.appliance_id}' '''
            cursor.execute(sql)

            
            
        _id = str(entoli['entolh_id'])
        
        sql=f''' INSERT INTO entoli(command)
              VALUES('{_id}') '''
        cursor.execute(sql)

        sql=f''' INSERT INTO elegxei(command_id_ele,device_id_ele)
              VALUES(last_insert_rowid(),'{self.appliance_id}') '''
        cursor.execute(sql)

        sql=f''' INSERT INTO pragmatopoiei(username_pragma,command_id_pragma,smart_name,date_time,IP_Address)
              VALUES('{self.profile}',last_insert_rowid(),'{socket.gethostname()}',CURRENT_TIMESTAMP,'{socket.gethostbyname(socket.gethostname())}') '''
        cursor.execute(sql)
        
        #reinitialize appliances to reset energi row
        cursor.execute("SELECT * FROM syskeyi")
        self.appliances = cursor.fetchall()

        sql = f'''select exei_prosvasi.device_id,eidos,dwmatio,energi from exei_prosvasi join syskeyi on syskeyi.device_id=exei_prosvasi.device_id
                and username_prosvasis='{self.profile}';'''
        cursor.execute(sql)
        self.allowed_appliances = cursor.fetchall()
        
        cursor.execute(sql)
        conn.commit()
        #
        
        sql = f'''select last_insert_rowid() ;'''
        cursor.execute(sql)
        self.entoli_id = str(cursor.fetchall()[0][0])
        

        if entoli['parametroi']:
            for i in reversed(range(self.page11Layout.count())): 
                self.page11Layout.itemAt(i).widget().setParent(None)
            
            for i in entoli['parametroi'].keys():
                
                self.slider = QSlider()
                self.slider.setOrientation(Qt.Horizontal)
                self.slider.setTickPosition(QSlider.TicksBelow)
                self.slider.setTickInterval(10)
                self.slider.setMinimum(entoli['parametroi'][i][0])
                self.slider.setMaximum(entoli['parametroi'][i][1])
                self.slider.valueChanged.connect(self.changedValue)
                
                self.slider_label = QLabel(i)
                self.slider_value = QLabel(' : ')
                self.page11Layout.addRow(self.slider_label,self.slider_value)
                self.page11Layout.addRow(self.slider)

            self.parameters_button = QPushButton('Enter parameters')
            self.page11Layout.addRow(self.parameters_button)
            self.parameters_button.clicked.connect(self.save_command_mongo)


            self.stackedLayout.setCurrentIndex(9)
                
            
        else:
            db.arxeio_entolwn.insert_one({"_id":ObjectId('0'*(24-len(self.entoli_id))+self.entoli_id),"parametroi":None})
            self.back_to_appliances()

    
    def changedValue(self):
        a = self.sender()
        cntr=0

        while True:
            if self.page11Layout.itemAt(cntr).widget() == a:
                break
            cntr+=1
            
        size = a.value()
        self.page11Layout.itemAt(cntr-1).widget().setText(' : ' + str(size))
        
    def save_command_mongo(self):
        parametroi = {}

        for i in range(0,self.page11Layout.count(),3):
            try:
                parametroi.update({self.page11Layout.itemAt(i).widget().text():self.page11Layout.itemAt(i+2).widget().value()})

            except:
                break

        db.arxeio_entolwn.insert_one({"_id":ObjectId('0'*(24-len(self.entoli_id))+self.entoli_id),"parametroi":parametroi})
        self.stackedLayout.setCurrentIndex(7)
        
    def show_consumption(self):
        
        for i in reversed(range(self.page10Layout.count())): 
                self.page10Layout.itemAt(i).widget().setParent(None)
                
        for i in self.appliances:
            anapse_id = str(db['appliances'].find({'_id':ObjectId(i[0])})[0]['entoles']['anapse']['entolh_id'])
            sbhse_id = str(db['appliances'].find({'_id':ObjectId(i[0])})[0]['entoles']['sbhse']['entolh_id'])
    
            sql =   f'''select device_id_ele,
                        case 
                        when energi=0 then sum(opened_for)*kwh
                        else sum(opened_for)*kwh + (julianday(CURRENT_TIMESTAMP) - julianday(max(opened_on)))* 24*kwh end total_consumption from
                        (select *,(julianday(closed_on) - julianday(opened_on))* 24  as opened_for  from
                        (select command_id,command,date_time as opened_on,device_id_ele,
                        lead (date_time) over(order by date_time) closed_on
                        from
                        (select command_id,command,date_time,device_id_ele from(select * from pragmatopoiei join elegxei on pragmatopoiei.command_id_pragma = elegxei.command_id_ele) e1
                        join entoli on entoli.command_id = e1.command_id_ele
                        where device_id_ele = '{i[0]}' and (command = '{anapse_id}' or command = '{sbhse_id}')))
                        where command = '{anapse_id}') join syskeyi on device_id_ele = syskeyi.device_id
                        group by command'''
            cursor.execute(sql)
            consumption = cursor.fetchall()
            self.clabel = QLabel()
            try:
                self.clabel.setText(i[1]+' : '+str(round(consumption[0][1],3))+' KW')
            except:
                self.clabel.setText(i[1]+' : 0 KW')
            self.page10Layout.addRow(self.clabel)

        self.exit_consumption = QPushButton('Exit')
        self.page10Layout.addRow(self.exit_consumption)
        self.exit_consumption.clicked.connect(self.cancel_restrictions)
        
        self.stackedLayout.setCurrentIndex(8)

    def show_history(self):
        self.w = Window2()
        self.w.show()

    def delete_profile(self):
        conn.execute("PRAGMA foreign_keys = 1") #enforces referential integrity constraints
        cursor.execute(f'''DELETE FROM profil_xristi WHERE username = '{self.profile}' ''')
        conn.execute("PRAGMA foreign_keys = 0")
        conn.commit()
        
        sql = '''UPDATE parexei_dikaiwmata
            SET primary_username=(CASE
                    WHEN (SELECT count(username_pro) 
                            FROM proteuon_profil
                            ORDER BY username_pro )>0 
                            THEN (SELECT username_pro 
                                    FROM proteuon_profil 
                                    ORDER BY username_pro limit 1)
                    ELSE NULL
            END)
            where primary_username IS NULL'''
        conn.execute(sql)

        sql = '''DELETE FROM profil_xristi
                WHERE username  IN 
                  (
                    SELECT secondary_username 
                    FROM parexei_dikaiwmata As B
                    Where B.primary_username IS NULL
                   )'''

        conn.execute("PRAGMA foreign_keys = 1")
        conn.execute(sql)
        conn.execute("PRAGMA foreign_keys = 0")
        conn.commit()

        #reorganize home page buttons
        for i in reversed(range(1,self.page1Layout.count())): 
            self.page1Layout.itemAt(i).widget().setParent(None)

        cursor.execute("SELECT * FROM 'profil_xristi';") 
        self.profiles = cursor.fetchall()
        
        for i in self.profiles: 
            self.button = QPushButton(i[0])
            self.page1Layout.addRow(self.button)
            self.button.clicked.connect(self.selectProfile)
            
        self.stackedLayout.setCurrentIndex(0)
       

if __name__ == "__main__":

    style = r"C:\Users\krist\OneDrive\Υπολογιστής\style.txt"
    app = QApplication(sys.argv)
    with open(style,'r') as fh:
        app.setStyleSheet(fh.read())
        
    window = Window()
    window.show()
    sys.exit(app.exec_())

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
    QHeaderView,
    QScrollArea,
    QGroupBox
)

conn = sqlite3.connect(r"smarthome.db") #connect to local sqlite database
cursor = conn.cursor() #initialize cursor, used to execute queries

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
        sql   = ''' select ημερομηνία_ώρα,username_πραγματοποιεί,είδος,δωμάτιο,εντολή_id,command_id,device_id from 
                    ((Πραγματοποιεί join Ελέγχει on Ελέγχει.command_id_ελέγχει = Πραγματοποιεί.command_id_πραγματοποιεί) a1 
                    join Συσκευή on a1.device_id_ελέγχει = Συσκευή.device_id) a2 
                    join Εντολή on Εντολή.command_id = a2.command_id_ελέγχει
                    order by ημερομηνία_ώρα desc '''#triple join of tables Ελέγχει,Συσκευή,Εντολή,Πραγματοποιεί to include all necessary data

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
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Smarthome")
        
        cursor.execute("SELECT * FROM Συσκευή") #query to get all appliances
        self.appliances = cursor.fetchall() #save them to appliances variable
        
        # Create a top-level layout
        layout = QVBoxLayout() #top level layout structured as a vertical box

        # Create the stacked layout
        self.stackedLayout = QStackedLayout() #rest of the app is structured as a stacked layout, many layouts one on top of the other with the ability to switch between them
        
        # Create the first page (select profile page)
        self.page1 = QWidget() #initialize the first page
        self.page1Layout = QFormLayout() #specify its layout

        self.new_button = QPushButton('Create new profile') #button, when pressed switches to create profile page
        self.page1Layout.addRow(self.new_button)
        self.new_button.clicked.connect(self.newProfile) 
        
        cursor.execute("SELECT * FROM 'Προφίλ_χρήστη';") #query to get all profiles
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

        cursor.execute("SELECT * FROM 'Πρωτεύον_προφίλ';") #query returning all primary profiles
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
        self.manage_restrictions_button.clicked.connect(self.manage_restrictions) #switches to manage restrictions page

        self.use_appliances_button = QPushButton('Use appliances')
        self.page5Layout.addRow(self.use_appliances_button)
        self.use_appliances_button.clicked.connect(self.use_appliances) #switches to appliances page

        self.consumption_button = QPushButton('Show consumption')
        self.page5Layout.addRow(self.consumption_button)
        self.consumption_button.clicked.connect(self.show_consumption) #switches to consumption display page

        self.history_button = QPushButton('Show history')
        self.page5Layout.addRow(self.history_button)
        self.history_button.clicked.connect(self.show_history) #creates a new panel where the commands history is displayed

        self.delete_primary_button = QPushButton('Delete Profile')
        self.page5Layout.addRow(self.delete_primary_button)
        self.delete_primary_button.clicked.connect(self.delete_profile) #deletes current profile and switches to home page

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
        
        self.child_profiles = QComboBox() #create a combo box which will store the child usernames of a specified primary profile
        self.page7Layout.addRow('Select child profile',self.child_profiles)
        self.child_profiles.activated.connect(self.child_restrictions) #for each child profiles this action will check the checkoxes accordingly

        for i in self.appliances: #create a checkbox for each appliance
            self.appliance_checkbox = QCheckBox(i[1]+' '+i[2])
            self.page7Layout.addRow(self.appliance_checkbox)

        self.apply_restrictions_button = QPushButton('Apply restrictions') #button, when pressed will apply the restrictions specified in the checkboxes
        self.page7Layout.addRow(self.apply_restrictions_button)
        self.apply_restrictions_button.clicked.connect(self.apply_restrictions)

        self.reset_button = QPushButton('Reset changes') #button that resets default restrictions
        self.page7Layout.addRow(self.reset_button)
        self.reset_button.clicked.connect(self.reset_changes)

        self.cancel_restrictions_button = QPushButton('Cancel') #button, returns to previous page when pressed
        self.page7Layout.addRow(self.cancel_restrictions_button)
        self.cancel_restrictions_button.clicked.connect(self.cancel_restrictions)
                
        self.page7.setLayout(self.page7Layout)
        self.stackedLayout.addWidget(self.page7)


        # Create the seventh page (primary appliances page)
        self.page8 = QWidget()
        self.page8Layout = QFormLayout()

        for i in self.appliances: #a primary account has access to all devices, therefore create a button for each device
            self.appliance_button = QPushButton(i[1]+' '+i[2])
            self.page8Layout.addRow(self.appliance_button)
            self.appliance_button.clicked.connect(self.show_commands) #when pressed switch to appliance commands page

        self.exit_button = QPushButton('Exit') #switches to previous page
        self.page8Layout.addRow(self.exit_button)
        self.exit_button.clicked.connect(self.cancel_restrictions)
        
        self.page8.setLayout(self.page8Layout)
        self.stackedLayout.addWidget(self.page8)

        # Create the eigth page (select appliance command)
        self.page9 = QWidget() #commands page, initially empty, when the appliance is specified this page is filled accordingly
        self.page9Layout = QFormLayout()

        self.page9.setLayout(self.page9Layout)
        self.stackedLayout.addWidget(self.page9)

        # Create the ninth page (show appliance consumption)
        self.page10 = QWidget() #KW consumption for each appliance, initially empty, widgets are added afterwards so that all commands are taken into account, instead of the old ones
        self.page10Layout = QFormLayout()

        self.page10.setLayout(self.page10Layout)
        self.stackedLayout.addWidget(self.page10)

        # Create the tenth page (enter command parameters)
        self.page11 = QWidget() #page where user can enter command parameters, initially empty, widgets are added after the command is specified
        self.page11Layout = QFormLayout()

        self.page11.setLayout(self.page11Layout)
        self.stackedLayout.addWidget(self.page11)

        
        # Add the combo box and the stacked layout to the top-level layout
        groupBox = QGroupBox() #Create a group box that will contain a scroll area
        groupBox.setFlat(True)
        groupBox.setStyleSheet("QGroupBox{border: 0;}") #remove groupbox border
        layout.addLayout(self.stackedLayout) #add stacked layout to main layout
        groupBox.setLayout(layout) #set groupbox layout as the main layout
        scroll = QScrollArea() #create scroll area
        scroll.setStyleSheet("QScrollArea{border: 0;}") #remove scroll area border
        scroll.setWidget(groupBox) #scroll area conatins the layout
        scroll.setWidgetResizable(True) #scroll area adjusts to contents
        scroll.setFixedHeight(400) #fixed window length
        scroll.setFixedWidth(300) #fixed window width
        layout2 = QVBoxLayout(self) #create a final layout that will contain the scroll area
        layout2.addWidget(scroll) 
        self.show()
        
        

    def selectProfile(self): #binded to profile buttons
        self.profile = self.sender().text() #get the profile button pressed username
        self.password_field.setPlaceholderText("Enter "+self.profile+" password") #enter this username as a placeholder in the enter password text edit
        self.password_field.clear() #clear previous password entered
        self.stackedLayout.setCurrentIndex(1) #swirch to enter password page

    def newProfile(self): #binded to create new profile button
        self.stackedLayout.setCurrentIndex(2) #switch to create new profile page

    def enterPassword(self): #binded to enter button in enter password page
        password = self.page2Layout.itemAt(0).widget().text()
        cursor.execute(f"SELECT password,alternative_password,δημόσιο FROM 'Προφίλ_χρήστη' WHERE username = '{self.profile}' ;") #self.profile contains the profile whom password we want to enter
        correct_password = cursor.fetchall() #with this sql query we get alla the necessary information, such as paswwords and wether it's a public profile
        
        if password == correct_password[0][0] or password == correct_password[0][1] or correct_password[0][2]: #if the user enters the correct password, or if the profile is public proceed
            self.label.setText('') #password is correct, no warnings display
            
            cursor.execute(f"SELECT * FROM 'Πρωτεύον_προφίλ' WHERE username_pro = '{self.profile}' ;") #query to find wether the current profile is primary or secondart
            self.isPrimary = cursor.fetchall()
            
            if self.isPrimary: #if it's primary switch to primary profile actions page
                self.stackedLayout.setCurrentIndex(3)
                
            else:
                sql = f'''select Έχει_πρόσβαση.device_id_πρόσβασης,είδος,δωμάτιο,ενεργή from Έχει_πρόσβαση join Συσκευή on Συσκευή.device_id=Έχει_πρόσβαση.device_id_πρόσβασης
                and username_πρόσβασης='{self.profile}';''' #otherwise the profile is secondary, therefore we switch to secondary profile actions page
                cursor.execute(sql)                         #which contains only the appliances that are allowed on the current profile, this sql query return the allowed appliances
                self.allowed_appliances = cursor.fetchall()

                for i in reversed(range(self.page6Layout.count())): #delete all widgets contained in the secondary profile actions page, existing due to another profile being used previously
                    self.page6Layout.itemAt(i).widget().setParent(None)
    
                if self.allowed_appliances: #for each allowed appliance create a new button
                    for i in self.allowed_appliances:
                        self.appliance_button = QPushButton(i[1]+' '+i[2])
                        self.page6Layout.addRow(self.appliance_button)
                        self.appliance_button.clicked.connect(self.show_commands) #when pressed it shows the commands of the specified appliance


                self.delete_secondary_button = QPushButton('Delete Profile') #delete profile button
                self.page6Layout.addRow(self.delete_secondary_button)
                self.delete_secondary_button.clicked.connect(self.delete_profile)
        
                self.exit_secondary = QPushButton('Exit') #return to previous panel button
                self.page6Layout.addRow(self.exit_secondary)
                self.exit_secondary.clicked.connect(self.homepage)

                self.stackedLayout.setCurrentIndex(4)
        else:
            self.label.setText('Incorrect, try again or enter 2nd password') #if password is incorrect display this message

    def switchPage(self):
        self.stackedLayout2.setCurrentIndex(self.pageCombo.currentIndex()) #switch page in stacked layout 2

    def cancel_new(self): #exit the create profile page, set all text edits to default, switch to home page
        self.new_username.clear()
        self.new_password.clear()
        self.new_alternative_password.clear()
        
        self.stackedLayout.setCurrentIndex(0)

    def createPrimaryProfile(self): #action binded to enter button create primary profile page
        if self.new_username.text()!='' and ((self.new_password.text()!='') ^ self.isPublic.isChecked()): #chech wether text edits are empty, allow password to be empty if the profile is public
            try:
                cursor.execute('''INSERT INTO Προφίλ_χρήστη(username,password,alternative_password,δημόσιο,πολλαπλών_χρηστών)
                    VALUES(?,?,?,?,?)''',(self.new_username.text(),self.new_password.text(),None if self.new_alternative_password.text()=='' else self.new_alternative_password.text(),self.isPublic.isChecked(),self.isMulti.isChecked()))#query to enter new profile in user profiles table, if no alternative password enter NULL instead of empty string

                sql=f''' INSERT INTO Πρωτεύον_προφίλ(username_pro)
                    VALUES('{self.new_username.text()}') '''
                cursor.execute(sql) #sql query to enter new profile in primary profile table

                
                conn.commit() #commit changes to database

                self.button = QPushButton(self.new_username.text()) #add new profile button to home page
                self.page1Layout.addRow(self.button)
                self.button.clicked.connect(self.selectProfile)

                self.master_profiles.addItem(self.new_username.text())

                self.cancel_new() #switch to homepage
                self.error_label.setText('') #clear all error labels
            except Exception as e: #throw exception when unique key constrain is violated
                print(e)
                self.error_label.setText('username already exists')
        else:
            self.error_label.setText('Username,password fields must be filled') #display message when not all fields are filled


        

    def createSecondaryProfile(self):
        if self.master_profiles.currentText()!='': #if no primary profiles exist, user cannot create secondary profile
            if self.new_username.text()!='' and ((self.new_password.text()!='') ^ self.isPublic.isChecked()): #same constraints as primary profiles
                try:
                    cursor.execute('''INSERT INTO Προφίλ_χρήστη(username,password,alternative_password,δημόσιο,πολλαπλών_χρηστών)
                    VALUES(?,?,?,?,?)''',(self.new_username.text(),self.new_password.text(),None if self.new_alternative_password.text()=='' else self.new_alternative_password.text(),self.isPublic.isChecked(),self.isMulti.isChecked()))
                    #insert new profile to user profilew table
                    
                    sql=f''' INSERT INTO Δευτερεύον_προφίλ(username_de)
                        VALUES('{self.new_username.text()}') '''
                    cursor.execute(sql) #insert new profile to secondary profiles table

                    sql=f''' INSERT INTO Παρέχει_δικαιώματα(primary_username,secondary_username)
                          VALUES('{self.master_profiles.currentText()}','{self.new_username.text()}') '''
                    cursor.execute(sql) #insert new profile dependency to parexei dikaiwmata table



                    conn.commit()

                    self.button = QPushButton(self.new_username.text()) #create button in home page for new profile
                    self.page1Layout.addRow(self.button)
                    self.button.clicked.connect(self.selectProfile)
                    
                    self.cancel_new() #switch to home page
                    self.error_label.setText('')
                    
                except Exception as e: #throw exception when unique key constrain is violated
                    self.error_label.setText('username already exists') 
                    
            else:
                self.error_label.setText('Username,password fields must be filled') #display message when not all fields are filled
        else:
            self.error_label.setText('No primary profile to set as master') #display message when no primary profiles exist
            

    def manage_restrictions(self): #binded to manage restrictions button in primary profile actions page
        
        sql = f'''SELECT secondary_username FROM 'Παρέχει_δικαιώματα' 
        WHERE primary_username='{self.profile}';''' #sql query that returns all child profiles of the specified primary profile
        cursor.execute(sql)
        self.childprofiles = cursor.fetchall() #save child profiles to childprofiles variable

        self.child_profiles.clear() #empty combo box containing child profile usernames
        self.child_profiles.addItems([i[0] for i in self.childprofiles]) #add enw child profil usernames

        if self.childprofiles:
            for i in range(2,2+len(self.appliances)): #first 2 widgets in manage restrictions page are label and combobox, followed by a checkbox for each appliance
                sql = f'''SELECT * FROM Έχει_πρόσβαση 
                    WHERE username_πρόσβασης='{self.childprofiles[0][0]}' and device_id_πρόσβασης='{self.appliances[i-2][0]}';'''
                cursor.execute(sql) #sql query that returns non empty if profile has access to specified appliance
                has_access = cursor.fetchall()
                if has_access: #if non empty set checkbox to checked
                    self.page7Layout.itemAt(i).widget().setChecked(True) 
                else: #else do not check
                    self.page7Layout.itemAt(i).widget().setChecked(False)
                    
        self.stackedLayout.setCurrentIndex(5) #switch to manage restrictions page

    def child_restrictions(self): #binded to combo box selection
        for i in range(2,2+len(self.appliances)): #queries restrictions for the new profile and checks checkboxes accordingly
                sql = f'''SELECT * FROM Έχει_πρόσβαση 
                    WHERE username_πρόσβασης='{self.child_profiles.currentText()}' and device_id_πρόσβασης='{self.appliances[i-2][0]}';'''
                cursor.execute(sql)
                has_access = cursor.fetchall()
                if has_access:
                    self.page7Layout.itemAt(i).widget().setChecked(True)
                else:
                    self.page7Layout.itemAt(i).widget().setChecked(False)

    def apply_restrictions(self): #binded to apply restrictions button
        if self.child_profiles.currentText()!='': #if there exist child profiles for current primary profile
            for i in range(2,2+len(self.appliances)):
                sql = f'''SELECT * FROM Έχει_πρόσβαση 
                        WHERE username_πρόσβασης='{self.child_profiles.currentText()}' and device_id_πρόσβασης='{self.appliances[i-2][0]}';'''
                cursor.execute(sql) #query to check if current child profile has access to specified appliance
                has_access = cursor.fetchall()
                if has_access: #if it does
                    if not self.page7Layout.itemAt(i).widget().isChecked(): #if checkbox of this appliance is not checked
                        sql=f''' DELETE FROM Έχει_πρόσβαση
                        WHERE username_πρόσβασης='{self.child_profiles.currentText()}' and device_id_πρόσβασης='{self.appliances[i-2][0]}';'''
                        cursor.execute(sql) #remove the appliance rights from exei prosvasi table
                else:
                    if self.page7Layout.itemAt(i).widget().isChecked(): #otherwise insert it 
                        sql=f''' INSERT INTO Έχει_πρόσβαση(username_πρόσβασης,device_id_πρόσβασης)
                        VALUES('{self.child_profiles.currentText()}','{self.appliances[i-2][0]}') '''
                        cursor.execute(sql)

            conn.commit()
        else:
            None

    def reset_changes(self): #binded to reset button in manage restrictions page
        self.child_restrictions() #sets checkboxes to initial state

    def cancel_restrictions(self): #binded to cancel button in manage restrictions page
        self.stackedLayout.setCurrentIndex(3) #switch to previous page

    def use_appliances(self): #switch to use appliances for primary profiles button
        self.stackedLayout.setCurrentIndex(6)

    def homepage(self): #switch to homepage
        self.stackedLayout.setCurrentIndex(0)

    def show_commands(self): #binded to appliances button in use appliances pages
        a = self.sender() #find the appliance button pressed
        cntr=0 

        if self.isPrimary: #if the current profile is primary
            while True: #iterate over widgets, to find the index of the pressed widget
                if self.page8Layout.itemAt(cntr).widget() == a:
                    break
                cntr+=1

            self.appliance_id = self.appliances[cntr][0] #cntr contains this index, use it to find the appliance id
            self.appliance_isActive = self.appliances[cntr][3] #find wether this appliance is active
            self.entoles = db['appliances'].find({'_id':ObjectId(self.appliance_id)})[0]['entoles'] #mongo query to find alla appliance commands
            
        else: #if the profile is secondary
            while True:
                if self.page6Layout.itemAt(cntr).widget() == a:
                    break
                cntr+=1

            self.appliance_id = self.allowed_appliances[cntr][0] #find the appliance id from the allowed appliances instead of all the appliances
            self.appliance_isActive = self.allowed_appliances[cntr][3]
            self.entoles = db['appliances'].find({'_id':ObjectId(self.appliance_id)})[0]['entoles']

        if self.appliance_isActive: #if the specified appliance is currently active
            self.entoles = {i:self.entoles[i] for i in self.entoles if i!='Turn on'} #self.entoles will contain all commands except for turn on command
        else:
            self.entoles = {i:self.entoles[i] for i in self.entoles if i=='Turn on'} #otherwise, contains only turn on command
        
        for i in reversed(range(self.page9Layout.count())): #delete all previous widgets in appliance commands page, existing due to previously using another device
            self.page9Layout.itemAt(i).widget().setParent(None)
        
        for i in self.entoles.keys(): #for every command create a button in select appliance command page
            self.command_button = QPushButton(i)
            self.page9Layout.addRow(self.command_button)
            self.command_button.clicked.connect(self.save_command)

        self.exit_commands = QPushButton('Exit') #create an exit button in select appliance command page
        self.page9Layout.addRow(self.exit_commands)
        self.exit_commands.clicked.connect(self.back_to_appliances)
        
        self.stackedLayout.setCurrentIndex(7) #switch to select appliance command page

    def back_to_appliances(self): #switches back to appliances page for each profile
        if self.isPrimary:
            self.stackedLayout.setCurrentIndex(6)
        else:
            self.stackedLayout.setCurrentIndex(4)

    def save_command(self):
        a = self.sender() #find which command was selected
        cntr=0

        while True: #find the widget index
            if self.page9Layout.itemAt(cntr).widget() == a:
                break
            cntr+=1

        entoli_name = list(self.entoles.keys())[cntr] #use that index to find theat command
        entoli = self.entoles[entoli_name]

        if entoli_name == 'Turn on': #if the command is turn on
            sql=f''' UPDATE Συσκευή SET ενεργή=true 
                WHERE device_id = '{self.appliance_id}' '''
            cursor.execute(sql) #sql query to set appliance state as on in appliance table

        elif entoli_name == 'Turn off': #otherwise set it to off
            sql=f''' UPDATE Συσκευή SET ενεργή=false
                WHERE device_id = '{self.appliance_id}' '''
            cursor.execute(sql)

            
            
        _id = str(entoli['entolh_id']) #find the command id from mongo db appliances collection
        
        sql=f''' INSERT INTO Εντολή(εντολή_id)
              VALUES('{_id}') '''
        cursor.execute(sql) #sql query to insert εντολή_id in commands table

        sql=f''' INSERT INTO Ελέγχει(command_id_ελέγχει,device_id_ελέγχει)
              VALUES(last_insert_rowid(),'{self.appliance_id}') '''
        cursor.execute(sql) #sql query to insert command and appliance to controls table

        sql=f''' INSERT INTO Πραγματοποιεί(username_πραγματοποιεί,command_id_πραγματοποιεί,όνομα_συσκευής_control,ημερομηνία_ώρα,IP_Address)
              VALUES('{self.profile}',last_insert_rowid(),'{socket.gethostname()}',CURRENT_TIMESTAMP,'{socket.gethostbyname(socket.gethostname())}') '''
        cursor.execute(sql) #insert everything to realize table
        
        #reinitialize appliances to reset appliance state column for both appliances and allowed appliances sets
        cursor.execute("SELECT * FROM Συσκευή")
        self.appliances = cursor.fetchall()

        sql = f'''select Έχει_πρόσβαση.device_id_πρόσβασης,είδος,δωμάτιο,ενεργή from Έχει_πρόσβαση join Συσκευή on Συσκευή.device_id=Έχει_πρόσβαση.device_id_πρόσβασης
                and username_πρόσβασης='{self.profile}';'''
        cursor.execute(sql)
        self.allowed_appliances = cursor.fetchall()
        
        cursor.execute(sql)
        conn.commit()
        
        
        sql = f'''select last_insert_rowid() ;'''
        cursor.execute(sql) #find the id of the last command that was inserted
        self.entoli_id = str(cursor.fetchall()[0][0])
        

        if entoli['parametroi']: #for every command parameter
            for i in reversed(range(self.page11Layout.count())): #delete alla previous widgets from command parameters page, existing duo to different past commands
                self.page11Layout.itemAt(i).widget().setParent(None)
            
            for i in entoli['parametroi'].keys(): #for each parameter
                
                self.slider = QSlider() #create a slider widget, with min and max value specified in the appliance document in the appliances collection
                self.slider.setOrientation(Qt.Horizontal)
                self.slider.setTickPosition(QSlider.TicksBelow)
                self.slider.setTickInterval(10)
                self.slider.setMinimum(entoli['parametroi'][i][0])
                self.slider.setMaximum(entoli['parametroi'][i][1])
                self.slider.valueChanged.connect(self.changedValue) #when the slider is used change the display label value
                
                self.slider_label = QLabel(i) #label that displays the slider value
                self.slider_value = QLabel(' : ')
                self.page11Layout.addRow(self.slider_label,self.slider_value)
                self.page11Layout.addRow(self.slider)

            self.parameters_button = QPushButton('Enter parameters') #button that saves command and parameters to arxeio entolwn collection when pressed
            self.page11Layout.addRow(self.parameters_button)
            self.parameters_button.clicked.connect(self.save_command_mongo)


            self.stackedLayout.setCurrentIndex(9) #switch to set parameters page page
                
            
        else: #if command contains no paramters
            db.arxeio_entolwn.insert_one({"_id":ObjectId('0'*(24-len(self.entoli_id))+self.entoli_id),"parametroi":None}) #add it to arxeio entolwn collection, its id is the ObjectId
            self.back_to_appliances() #switch to appliances page                                                          # representation of the command id 

    
    def changedValue(self): #binded to parameter slider in set parameters page
        a = self.sender()
        cntr=0

        while True: #find the slider being used
            if self.page11Layout.itemAt(cntr).widget() == a:
                break
            cntr+=1
            
        size = a.value()
        self.page11Layout.itemAt(cntr-1).widget().setText(' : ' + str(size)) #set the label text accordingly
        
    def save_command_mongo(self): #binded to enter button in set parameters page
        parametroi = {}

        for i in range(0,self.page11Layout.count(),3): #get the value of each slider
            try:
                parametroi.update({self.page11Layout.itemAt(i).widget().text():self.page11Layout.itemAt(i+2).widget().value()}) #insert parameter:value pair in parametroi dict

            except:#exception to catch getting non slider widget text retrieval exceptions
                break

        db.arxeio_entolwn.insert_one({"_id":ObjectId('0'*(24-len(self.entoli_id))+self.entoli_id),"parametroi":parametroi}) #insert command id an parameters in arxeio entolwn collection
        self.stackedLayout.setCurrentIndex(7) #switch to select appliance command page
        
    def show_consumption(self): #binded to show consumptio button in primary profile actions page
        
        for i in reversed(range(self.page10Layout.count())): #delete all previous widgets in consumption page
                self.page10Layout.itemAt(i).widget().setParent(None)
                
        for i in self.appliances: #for every appliance
            anapse_id = str(db['appliances'].find({'_id':ObjectId(i[0])})[0]['entoles']['Turn on']['entolh_id']) #find turn on and turn off ids
            sbhse_id = str(db['appliances'].find({'_id':ObjectId(i[0])})[0]['entoles']['Turn off']['entolh_id'])
    
            sql =   f'''select device_id_ελέγχει,
                        case 
                        when ενεργή=0 then sum(opened_for)*KWh
                        else sum(opened_for)*KWh + (julianday(CURRENT_TIMESTAMP) - julianday(max(opened_on)))* 24*KWh end total_consumption from
                        (select *,(julianday(closed_on) - julianday(opened_on))* 24  as opened_for  from
                        (select command_id,εντολή_id,ημερομηνία_ώρα as opened_on,device_id_ελέγχει,
                        lead (ημερομηνία_ώρα) over(order by ημερομηνία_ώρα) closed_on
                        from
                        (select command_id,εντολή_id,ημερομηνία_ώρα,device_id_ελέγχει from(select * from Πραγματοποιεί join Ελέγχει on Πραγματοποιεί.command_id_πραγματοποιεί = Ελέγχει.command_id_ελέγχει) e1
                        join Εντολή on Εντολή.command_id = e1.command_id_ελέγχει
                        where device_id_ελέγχει = '{i[0]}' and (εντολή_id = '{anapse_id}' or εντολή_id = '{sbhse_id}')))
                        where εντολή_id = '{anapse_id}') join Συσκευή on device_id_ελέγχει = Συσκευή.device_id
                        group by εντολή_id'''
            cursor.execute(sql) #sql query that returns the KW consumption of the specified appliance
            consumption = cursor.fetchall()
            self.clabel = QLabel() #create a label that will display the appliance's name and consumpion
            try:
                self.clabel.setText(i[1]+' : '+str(round(consumption[0][1],3))+' KW')
            except: #exception due to temporary bug that requires device to be turned on and off once to have its consumption displayed
                self.clabel.setText(i[1]+' : 0 KW') 
            self.page10Layout.addRow(self.clabel)

        self.exit_consumption = QPushButton('Exit') #exit consumption page button
        self.page10Layout.addRow(self.exit_consumption)
        self.exit_consumption.clicked.connect(self.cancel_restrictions)
        
        self.stackedLayout.setCurrentIndex(8) #switch to consumption page

    def show_history(self): #binded to show history button in primary profile actions page
        self.w = Window2() #create a new window containing the table 
        self.w.show()

    def delete_profile(self): #binded to delete profile button in profiles actions pages (both primary and secondary)
        conn.execute("PRAGMA foreign_keys = 1") #enforces referential integrity constraints
        cursor.execute(f'''DELETE FROM Προφίλ_χρήστη WHERE username = '{self.profile}' ''') #delete 
        conn.execute("PRAGMA foreign_keys = 0") #restore default constraints to allow inserts and updates
        conn.commit()
        
        sql = '''UPDATE Παρέχει_δικαιώματα
            SET primary_username=(CASE
                    WHEN (SELECT count(username_pro) 
                            FROM Πρωτεύον_προφίλ
                            ORDER BY username_pro )>0 
                            THEN (SELECT username_pro 
                                    FROM Πρωτεύον_προφίλ 
                                    ORDER BY username_pro limit 1)
                    ELSE NULL
            END)
            where primary_username IS NULL'''#from parexei dikaiwmata table find all rows with NULL primary_username due to primary profile deletion
        try:
            conn.execute(sql)                    #if another primary profile exists transfer secondary profile control to this new primary profile, otherwise None
        except Exception as e:
            print(e)
        sql = '''DELETE FROM Προφίλ_χρήστη
                WHERE username  IN 
                  (
                    SELECT secondary_username 
                    FROM Παρέχει_δικαιώματα As B
                    Where B.primary_username IS NULL
                   )'''
        #if there still exist rows in parexei dikaiwmata table with null primary username, no primary profiles exist anymore, therefore delete secondary profiles as well
        conn.execute("PRAGMA foreign_keys = 1") #enforce integrity cosntraints to allow cascade eletion
        conn.execute(sql)
        conn.execute("PRAGMA foreign_keys = 0") #restore initial constraints
        conn.commit()

        #reorganize home page buttons
        for i in reversed(range(1,self.page1Layout.count())): 
            self.page1Layout.itemAt(i).widget().setParent(None)

        cursor.execute("SELECT * FROM 'Προφίλ_χρήστη';") 
        self.profiles = cursor.fetchall()
        
        for i in self.profiles: 
            self.button = QPushButton(i[0])
            self.page1Layout.addRow(self.button)
            self.button.clicked.connect(self.selectProfile)


        self.master_profiles.clear()
        cursor.execute("SELECT * FROM 'Πρωτεύον_προφίλ';") #query returning all primary profiles
        masterprofiles = cursor.fetchall()

        self.master_profiles.addItems([i[0] for i in masterprofiles])
        self.stackedLayout.setCurrentIndex(0)
       

if __name__ == "__main__":

    style = r"style.txt" #style.txt contains the css used to decorize the app
    app = QApplication(sys.argv)
    with open(style,'r') as fh:
        app.setStyleSheet(fh.read()) #open it and apply the stylesheet
        
    window = Window()
    window.show()
    sys.exit(app.exec_())

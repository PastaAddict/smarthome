import sys
import sqlite3
import pymongo
from bson.objectid import ObjectId

conn = sqlite3.connect(r"C:\Users\krist\OneDrive\Υπολογιστής\smarthome.db")
cursor = conn.cursor()

client = pymongo.MongoClient('localhost', 27017)
db = client['smarthome']

from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QLineEdit,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QCheckBox,
    QLabel
)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smarthome")
        cursor.execute("SELECT * FROM syskeyi")
        self.appliances = cursor.fetchall()
        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Create the stacked layout
        self.stackedLayout = QStackedLayout()
        
        # Create the first page (select profile page)
        self.page1 = QWidget()
        self.page1Layout = QFormLayout()

        self.new_button = QPushButton('Create new profile')
        self.page1Layout.addRow(self.new_button)
        self.new_button.clicked.connect(self.newProfile)
        
        cursor.execute("SELECT * FROM 'profil_xristi';")
        self.profiles = cursor.fetchall()
        
        for i in self.profiles:
            self.button = QPushButton(i[0])
            self.page1Layout.addRow(self.button)
            self.button.clicked.connect(self.selectProfile)

            
        self.page1.setLayout(self.page1Layout)
        self.stackedLayout.addWidget(self.page1)

        
        # Create the second page (enter password page)
        self.page2 = QWidget()
        self.page2Layout = QFormLayout()

        self.password_field = QLineEdit()
        self.page2Layout.addRow(self.password_field)

        self.label = QLabel()
        self.page2Layout.addRow(self.label)
        
        self.button = QPushButton('Enter')
        self.page2Layout.addRow(self.button)
        self.button.clicked.connect(self.enterPassword)
        
        self.page2.setLayout(self.page2Layout)
        self.stackedLayout.addWidget(self.page2)

        # Create the third page as a new stacked layout(create new profile page)
        self.newProfilePage = QWidget()
        self.newProfilePageLayout = QVBoxLayout()
        
        
        self.pageCombo = QComboBox()
        self.pageCombo.addItems(["Primary Profile", "Secondary Profile"])
        self.pageCombo.activated.connect(self.switchPage)

        self.new_username = QLineEdit()
        self.new_username.setPlaceholderText("Enter username")
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Enter password")
        self.new_alternative_password = QLineEdit()
        self.new_alternative_password.setPlaceholderText("Enter alternative password")
        self.isPublic = QCheckBox("Public")
        self.isMulti = QCheckBox("Multiple users")

        self.cancel_new_profile = QPushButton('Cancel')
        self.cancel_new_profile.clicked.connect(self.cancel_new)
        
        self.stackedLayout2 = QStackedLayout()
        
        #page 1
        self.page3 = QWidget()
        self.page3Layout = QFormLayout()

        self.primary_profile_button = QPushButton('Enter')
        self.page3Layout.addRow(self.primary_profile_button)
        self.primary_profile_button.clicked.connect(self.createPrimaryProfile)
        
        
        self.page3.setLayout(self.page3Layout)
        self.stackedLayout2.addWidget(self.page3)

        #page2
        self.page4 = QWidget()
        self.page4Layout = QFormLayout()

        cursor.execute("SELECT * FROM 'proteuon_profil';")
        masterprofiles = cursor.fetchall()
        
        self.master_profiles = QComboBox()
        self.master_profiles.addItems([i[0] for i in masterprofiles])
        self.page4Layout.addRow('Select master profile',self.master_profiles)
        
        self.secondary_profile_button = QPushButton('Enter')
        self.page4Layout.addRow(self.secondary_profile_button)
        self.secondary_profile_button.clicked.connect(self.createSecondaryProfile)
        
        self.page4.setLayout(self.page4Layout)
        self.stackedLayout2.addWidget(self.page4)

        self.newProfilePage.setLayout(self.newProfilePageLayout)
        self.newProfilePageLayout.addWidget(self.pageCombo)
        self.newProfilePageLayout.addWidget(self.new_username)
        self.newProfilePageLayout.addWidget(self.new_password)
        self.newProfilePageLayout.addWidget(self.new_alternative_password)
        self.newProfilePageLayout.addWidget(self.isPublic)
        self.newProfilePageLayout.addWidget(self.isMulti)
        self.newProfilePageLayout.addLayout(self.stackedLayout2)
        self.newProfilePageLayout.addWidget(self.cancel_new_profile)
        self.stackedLayout.addWidget(self.newProfilePage)



        # Create the fourth page (select action page for primary profiles)
        self.page5 = QWidget()
        self.page5Layout = QFormLayout()


        self.manage_restrictions_button = QPushButton('Manage restrictions')
        self.page5Layout.addRow(self.manage_restrictions_button)
        self.manage_restrictions_button.clicked.connect(self.manage_restrictions)

        self.use_appliances_button = QPushButton('Use appliances')
        self.page5Layout.addRow(self.use_appliances_button)
        self.use_appliances_button.clicked.connect(self.use_appliances)

        self.exit_primary = QPushButton('Exit')
        self.page5Layout.addRow(self.exit_primary)
        self.exit_primary.clicked.connect(self.homepage)
        
        
        self.page5.setLayout(self.page5Layout)
        self.stackedLayout.addWidget(self.page5)

        # Create the fifth page (select action page for secondary profiles)
        self.page6 = QWidget()
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
        cursor.execute(f"SELECT kwdikos FROM 'profil_xristi' WHERE username = '{self.profile}' ;")
        correct_password = cursor.fetchall()
        
        if password == correct_password[0][0]:
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

                self.exit_secondary = QPushButton('Exit')
                self.page6Layout.addRow(self.exit_secondary)
                self.exit_secondary.clicked.connect(self.homepage)

                
                self.stackedLayout.setCurrentIndex(4)
            
        else:
            self.label.setText('Incorrect password, try again')

    def switchPage(self):
        self.stackedLayout2.setCurrentIndex(self.pageCombo.currentIndex())

    def cancel_new(self):
        
        self.new_username.clear()
        self.new_password.clear()
        self.new_alternative_password.clear()
        
        self.stackedLayout.setCurrentIndex(0)

    def createPrimaryProfile(self):

        sql=f''' INSERT INTO proteuon_profil(username_pro)
            VALUES('{self.new_username.text()}') '''
        cursor.execute(sql)

        sql=f''' INSERT INTO profil_xristi(username,kwdikos,alternative_password,dimosio,pollaplwn_xriston)
            VALUES('{self.new_username.text()}','{self.new_password.text()}','{self.new_alternative_password.text()}',{self.isPublic.isChecked()},{self.isMulti.isChecked()}) '''
        cursor.execute(sql)

        conn.commit()

        self.button = QPushButton(self.new_username.text())
        self.page1Layout.addRow(self.button)
        self.button.clicked.connect(self.selectProfile)

        self.cancel_new()

        

    def createSecondaryProfile(self):
        
        sql=f''' INSERT INTO deutereuon_profil(username_de)
            VALUES('{self.new_username.text()}') '''
        cursor.execute(sql)

        sql=f''' INSERT INTO parexei_dikaiwmata(primary_username,secondary_username)
              VALUES('{self.master_profiles.currentText()}','{self.new_username.text()}') '''
        cursor.execute(sql)

        sql=f''' INSERT INTO profil_xristi(username,kwdikos,alternative_password,dimosio,pollaplwn_xriston)
            VALUES('{self.new_username.text()}','{self.new_password.text()}','{self.new_alternative_password.text()}',{self.isPublic.isChecked()},{self.isMulti.isChecked()}) '''
        cursor.execute(sql)

        conn.commit()

        self.button = QPushButton(self.new_username.text())
        self.page1Layout.addRow(self.button)
        self.button.clicked.connect(self.selectProfile)

        self.cancel_new()

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

        sql=f''' INSERT INTO pragmatopoiei(username_pragma,command_id_pragma,date_time)
              VALUES('{self.profile}',last_insert_rowid(),CURRENT_TIMESTAMP) '''

        #reinitialize appliances to reset energi row
        cursor.execute("SELECT * FROM syskeyi")
        self.appliances = cursor.fetchall()

        sql = f'''select exei_prosvasi.device_id,eidos,dwmatio,energi from exei_prosvasi join syskeyi on syskeyi.device_id=exei_prosvasi.device_id
                and username_prosvasis='{self.profile}';'''
        cursor.execute(sql)
        self.allowed_appliances = cursor.fetchall()
        
        cursor.execute(sql)
        conn.commit()

        self.back_to_appliances()
        
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

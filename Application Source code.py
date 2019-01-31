#Extended time accommodation calculator
#    Copyright (C) 2018 John Boniello
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import copy
import time as tm
from PyQt5 import QtCore, QtGui, QtWidgets
from app5 import Ui_MainWindow

import sqlite3
db=sqlite3.connect('TimeAccommodations.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS students(name TEXT PRIMARY KEY NOT NULL,
                    elat1 REAL,  matht1 REAL,  sst1 REAL, scit1 REAL, wlt1 REAL, enlt1 REAL) ''')
db.commit()
db.close()
class Accapp(QtWidgets.QMainWindow, Ui_MainWindow, ):
    def __init__(self):
        super().__init__()        
        Ui_MainWindow.__init__(self)
        Ui_MainWindow.__init__(self)        
        self.setupUi(self)
        self.retranslateUi(self)
        self.student={}
        
        
          #ela tab order        
        self.setTabOrder(self.eladate, self.elaname)
        self.setTabOrder(self.elaname, self.elaexp)
        self.setTabOrder(self.elaexp, self.elaact)
        self.setTabOrder(self.elaact, self.elaaddnew)
        self.setTabOrder(self.elaaddnew, self.elacalculate)
        
        #math tab order
        self.setTabOrder(self.mathdate, self.mathname)
        self.setTabOrder(self.mathname, self.mathexp)
        self.setTabOrder(self.mathexp, self.mathact)
        self.setTabOrder(self.mathact, self.mathaddnew)
        self.setTabOrder(self.mathaddnew, self.mathcalculate)
       
        #ss tab order
        self.setTabOrder(self.ssdat, self.ssname)
        self.setTabOrder(self.ssname, self.ssexp)
        self.setTabOrder(self.ssexp, self.ssact)
        self.setTabOrder(self.ssact, self.ssaddnew)
        self.setTabOrder(self.ssaddnew, self.sscalculate)


        #sci tab order
        self.setTabOrder(self.scidate, self.sciname)
        self.setTabOrder(self.sciname, self.sciexp)
        self.setTabOrder(self.sciexp, self.sciact)
        self.setTabOrder(self.sciact, self.sciaddnew)
        self.setTabOrder(self.sciaddnew, self.scicalculate)
   

        #wl tab order
        self.setTabOrder(self.wldate, self.wlname)
        self.setTabOrder(self.wlname, self.wlexp)
        self.setTabOrder(self.wlexp, self.wlact)
        self.setTabOrder(self.wlact, self.wladdnew)
        self.setTabOrder(self.wladdnew, self.wlcalculate)


        #enl tab order
        self.setTabOrder(self.enldate, self.enlname)
        self.setTabOrder(self.enlname, self.enlexp)
        self.setTabOrder(self.enlexp, self.enlact)
        self.setTabOrder(self.enlact, self.enladdnew)
        self.setTabOrder(self.enladdnew, self.enlcalculate)
  
        #ELA buttons and list
        self.elaaddnew.clicked.connect(self.elaaddRow)
        self.elaratio_list=[]
        self.elacalculate.clicked.connect(self.elaresultbox)    

        #Math buttons and list
        self.mathaddnew.clicked.connect(self.mathaddRow)
        self.mathratio_list=[]
        self.mathcalculate.clicked.connect(self.mathresultbox)

#ss buttons
        self.ssaddnew.clicked.connect(self.ssaddRow)
        self.ssratio_list=[]
        self.sscalculate.clicked.connect(self.ssresultbox)


        #Science buttons and list
        self.sciaddnew.clicked.connect(self.sciaddRow)
        self.sciratio_list=[]
        self.scicalculate.clicked.connect(self.sciresultbox)


        #World languages buttons and list
        self.wladdnew.clicked.connect(self.wladdRow)
        self.wlratio_list=[]
        self.wlcalculate.clicked.connect(self.wlresultbox)


        #ENL Buttons and list
        self.enladdnew.clicked.connect(self.enladdRow)
        self.enlratio_list=[]
        self.enlcalculate.clicked.connect(self.enlresultbox)

    #set load, save, and update buttons to false unless lineedit filled
        self.pushButton_2.setEnabled(False)
        self.stunamebox.textChanged.connect(self.setsavenabled)
        self.pushButton.setEnabled(False)
        self.stunameexist.textChanged.connect(self.setloadenabled)
        self.pushButton_3.setEnabled(False)
        self.stunameexist.textChanged.connect(self.setupdateenabled)
        
    # assign save load and update buttons
        self.pushButton.clicked.connect(self.loadfile)
        self.pushButton_2.clicked.connect(self.savefile)
        self.pushButton_3.clicked.connect(self.updatestudent)
    
#enable load and save buttons        
    def setsavenabled(self):
        self.pushButton_2.setEnabled(self.stunamebox.text() != '')
    def setloadenabled(self):
        self.pushButton.setEnabled(self.stunameexist.text() != '')
    def setupdateenabled(self):
        self.pushButton_3.setEnabled(self.stunameexist.text() != '')


#ELA blocks
    def elaaddRow(self):
        # Retrieve text from QLineEdit
        eladate = self.eladate.text()
        elatname = self.elaname.text()
        elaexpect = self.elaexp.text()
        elaactual = self.elaact.text()    	    
     # Create a empty row at bottom of table
        numRows = self.elatable.rowCount()
        self.elatable.insertRow(numRows)
    # Add text to the row
        self.elatable.setItem(numRows, 0, QtWidgets.QTableWidgetItem(eladate))
        self.elatable.setItem(numRows, 1, QtWidgets.QTableWidgetItem(elatname))
        self.elatable.setItem(numRows, 2, QtWidgets.QTableWidgetItem(elaexpect))
        self.elatable.setItem(numRows, 3, QtWidgets.QTableWidgetItem(elaactual))
# calculate ratio and add ratio to list
        try:
            elaratio= float(elaactual)/float(elaexpect)
            self.elaratio_list.append(float(elaratio))
            global elaaverage
            elaaverage=(sum(self.elaratio_list)/len(self.elaratio_list))*100
            global elatime 
            elatime=None
            elatime= round(elaaverage,2)
            self.student["elatime"]=elatime
            el=self.student.get(elatime2)
        except (ValueError, IndexError, ZeroDivisionError, NameError):
            pass
#ela delete 
    def elaremove(self):
        try:
            numRowsrem = self.elatable.rowCount()
            self.elatable.removeRow(numRowsrem-1)            
            global ela_ratioup
            ela_ratioup = self.elaratio_list
            del ela_ratioup[-1]
        except (IndexError,ZeroDivisionError,NameError):
            pass

# List update after update button pressed
    def elalstup(self):
        try:
            global elaaverage2
            elaaverage2=(sum(ela_ratioup)/len(ela_ratioup)*100)
            global elatime2
            elatime2= round(elaaverage2,2)
            eladb2 = elatime2
#print(average)
            self.elaresult.setText(self.calculateela2())
            self.elaaccbox.setText(self.calculateela2())
            self.student["elatime2"]=elatime2

        except (ZeroDivisionError, NameError):
            pass
       

# Results when calculate button pressed              
    def calculateela(self):
        try:                   
            if elatime <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses an average of "+str(elatime)+"%"+" of the expected time.)"
            elif elatime < 150:
                return "This student may or may not need extended time, he/she uses " + str(elatime)+ "%" " of the expected time on exams."
            elif elatime == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(elatime)+"%"+" of the expected time)"
            elif elatime > 150 and elatime < 200:
                return "This student takes "+ str(elatime)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif elatime >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(elatime)+"%"+" of the expected time.)"
            else:
                return none
        except(NameError,ZeroDivisionError,ValueError):
            pass

#Results when update btton pressed
    def calculateela2(self):
        if elatime2 <= 100:
            return "This student does not require extra time for this subject." +" ("+"He/she currently uses "+str(elatime2)+"%"+")"
        elif elatime2 < 150:
            return "This student may or may not need extended time, he/she uses " + str(elatime2)+ "%" " of the expected time on exams."
        elif elatime2 == 150: 
            return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(elatime2)+"%"+" of the expected time)"
        elif elatime2 > 150 and elatime2 < 200:
            return "This student takes "+ str(elatime2)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
        elif elatime2 >=200:
            return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(elatime2)+"%"+" of the expected time.)"
        else:
            return none  
#Output to results and student information tab             
    def elaresultbox(self):
        self.elaresult.setText(self.calculateela())
        self.elaaccbox.setText(self.calculateela())

#Math Blocks
    def mathaddRow(self):
        # Retrieve text from QLineEdit
        mathdate = self.mathdate.text()
        mathtname = self.mathname.text()
        mathexpect = self.mathexp.text()
        mathactual = self.mathact.text()          
        #create a empty row at bottom of table
        numRows = self.mathtable.rowCount()
        self.mathtable.insertRow(numRows)
        #add text to the row
        self.mathtable.setItem(numRows, 0, QtWidgets.QTableWidgetItem(mathdate))
        self.mathtable.setItem(numRows, 1, QtWidgets.QTableWidgetItem(mathtname))
        self.mathtable.setItem(numRows, 2, QtWidgets.QTableWidgetItem(mathexpect))
        self.mathtable.setItem(numRows, 3, QtWidgets.QTableWidgetItem(mathactual))
       # calculate ratio and add ratio to list
        try:
            mathratio= float(mathactual)/float(mathexpect)
            mathratiostr = str(mathratio)
            mathstrsp = mathratiostr.split()
            self.mathratio_list.append(float(mathratio))
            #self.lista=copy.deepcopy(self.ratio_list)
            mathaverage=(sum(self.mathratio_list)/len(self.mathratio_list))*100
            global mathtime 
            mathtime= round(mathaverage,2)
            self.student["mathtime"]=mathtime
        except (ValueError,IndexError,ZeroDivisionError,NameError):
            pass

 # Results when calculate button pressed        
    def calculatemath(self):
        try:  
                
            if mathtime <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(mathtime)+"%"+" of the expected time.)"
            elif mathtime < 150:
                return "This student may or may not need extended time, he/she uses " + str(mathtime)+ "%" " of the expected time on exams."
            elif mathtime == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(mathtime)+"%"+" of the expected time)"
            elif mathtime > 150 and elatime < 200:
                return "This student takes "+ str(mathtime)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif mathtime >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(mathtime)+"%"+" of the expected time.)"
            else:
                return none
        except(NameError,ZeroDivisionError,ValueError):
            pass

    def mathresultbox(self):
        self.mathresult.setText(self.calculatemath())    
        self.mathaccbox.setText(self.calculatemath())

    #ela delete 
    def mathremove(self):
        try:
            numRowsrem = self.mathtable.rowCount()
            self.mathtable.removeRow(numRowsrem-1)
            global math_ratioup
            math_ratioup = self.mathratio_list
            del math_ratioup[-1]
        except(IndexError,ZeroDivisionError,NameError):
            pass

# List update after update button pressed
    def mathlstup(self):
        try:       
            average2=(sum(math_ratioup)/len(math_ratioup)*100)
            global mathtime2
            mathtime2= round(average2,2)
            self.student["mathtime2"]=mathtime2
        except(ZeroDivisionError,NameError):
            pass

#Results when update btton pressed
    def calculatemath2(self):
        if mathtime2 <= 100:
            return "This student does not require extra time for this subject." +" ("+"He/she currently uses "+str(mathtime2)+"%"+")"
        elif mathtime2 < 150:
            return "This student may or may not need extended time, he/she uses " + str(mathtime2)+ "%" " of the expected time on exams."
        elif mathtime2 == 150: 
            return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(mathtime2)+"%"+" of the expected time)"
        elif mathtime2 > 150 and mathtime2 < 200:
            return "This student takes "+ str(mathtime2)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
        elif mathtime2 >=200:
            return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(mathtime2)+"%"+" of the expected time.)"
        else:
            return none 
#print(average)
        self.mathresult.setText(self.calculatemath2())
        self.mathaccbox.setText(self.calculatemath2())

       


    # SS blocks
    def ssaddRow(self):
        # Retrieve text from QLineEdit
        ssdate = self.ssdat.text()
        sstname = self.ssname.text()
        ssexpect = self.ssexp.text()
        ssactual = self.ssact.text()          
     # Create a empty row at bottom of table
        numRows = self.sstable.rowCount()
        self.sstable.insertRow(numRows)
    # Add text to the row
        self.sstable.setItem(numRows, 0, QtWidgets.QTableWidgetItem(ssdate))
        self.sstable.setItem(numRows, 1, QtWidgets.QTableWidgetItem(sstname))
        self.sstable.setItem(numRows, 2, QtWidgets.QTableWidgetItem(ssexpect))
        self.sstable.setItem(numRows, 3, QtWidgets.QTableWidgetItem(ssactual))
# calculate ratio and add ratio to list
        try:
            ssratio= float(ssactual)/float(ssexpect)        
            self.ssratio_list.append(float(ssratio))       
            average=(sum(self.ssratio_list)/len(self.ssratio_list))*100
            global sstime 
            sstime= round(average,2)
            self.student["sstime"]=sstime
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass

        
    def calculatess(self):   
        try:       
            if sstime <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(sstime)+"%"+" of the expected time.)"
            elif sstime < 150:
                return "This student may or may not need extended time, he/she uses " + str(sstime)+ "%" " of the expected time on exams."
            elif sstime == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(sstime)+"%"+" of the expected time)"
            elif sstime > 150 and sstime < 200:
                return "This student takes "+ str(sstime)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif sstime >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(sstime)+"%"+" of the expected time.)"
            else:
                return none
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass
        
    def ssresultbox(self):
        self.ssreult.setText(self.calculatess())
        self.ssacbox.setText(self.calculatess())

#ela delete 
    def ssremove(self):
        try:
            numRowsrem = self.sstable.rowCount()
            self.sstable.removeRow(numRowsrem-1)
            global ss_ratioup
            ss_ratioup = self.ssratio_list
            del ss_ratioup[-1]
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass


# List update after update button pressed
    def sslstup(self):
        try:      
            average2=(sum(ela_ratioup)/len(ss_ratioup)*100)
            global sstime2
            sstime2= round(average2,2)
            self.student["sstime2"]=sstime2
            #print(average)
            self.ssresult.setText(self.calculatess2())
            self.ssacbox.setText(self.calculatess2())
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass


#Results when update btton pressed
    def calculatess2(self):
        if sstime2 <= 100:
            return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(sstime2)+"%"+" of the expected time.)"
        elif sstime2 < 150:
            return "This student may or may not need extended time, he/she uses " + str(sstime2)+ "%" " of the expected time on exams."
        elif sstime2 == 150: 
            return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(sstime2)+"%"+" of the expected time)"
        elif sstime2 > 150 and sstime2 < 200:
            return "This student takes "+ str(sstime2)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
        elif sstime2 >=200:
            return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(sstime2)+"%"+" of the expected time.)"
        else:
            return none  

    #Science Blocks
    def sciaddRow(self):
        # Retrieve text from QLineEdit
        scidate = self.scidate.text()
        scitname = self.sciname.text()
        sciexpect = self.sciexp.text()
        sciactual = self.sciact.text()          
     # Create a empty row at bottom of table
        numRows = self.scitable.rowCount()
        self.scitable.insertRow(numRows)
    # Add text to the row
        self.scitable.setItem(numRows, 0, QtWidgets.QTableWidgetItem(scidate))
        self.scitable.setItem(numRows, 1, QtWidgets.QTableWidgetItem(scitname))
        self.scitable.setItem(numRows, 2, QtWidgets.QTableWidgetItem(sciexpect))
        self.scitable.setItem(numRows, 3, QtWidgets.QTableWidgetItem(sciactual))
        
# calculate ratio and add ratio to list
        try:
            sciratio= float(sciactual)/float(sciexpect)        
            self.sciratio_list.append(float(sciratio))      
            average=(sum(self.sciratio_list)/len(self.sciratio_list))*100
            global scitime 
           
            scitime= round(average,2)
            self.student["scitime"]=scitime
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass
        
    def calculatesci(self):   
        try:        
            if scitime <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(scitime)+"%"+" of the expected time.)"
            elif scitime < 150:
                return "This student may or may not need extended time, he/she uses " + str(scitime)+ "%" " of the expected time on exams."
            elif scitime == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(scitime)+"%"+" of the expected time)"
            elif scitime > 150 and scitime < 200:
                return "This student takes "+ str(scitime)+ "%"+ " of the expected time on exams in this subject.  This suggests that the student may need time and a half or double time."
            elif scitime >=200:
                return "This student may need double time on exams for this subject."+" ("+"He/she currently uses "+str(scitime)+"%"+" of the expected time.)"
            else:
                return none
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass

    def sciresultbox(self):
        self.sciresult.setText(self.calculatesci())
        self.sciaccbox.setText(self.calculatesci())

#ela delete 
    def sciremove(self):
        try:
            numRowsrem = self.scitable.rowCount()
            self.scitable.removeRow(numRowsrem-1)
            global sci_ratioup
            sci_ratioup = self.sciratio_list
            del sci_ratioup[-1]
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass


# List update after update button pressed
    def scilstup(self):
        try:        
            average2=(sum(sci_ratioup)/len(sci_ratioup)*100)
            global scitime2
            scitime2= round(average2,2)
            self.student["scitime2"]=scitime2
#print(average)
            self.sciresult.setText(self.calculatesci2())
            self.sciaccbox.setText(self.calculatesci2())
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass
       


#Results when update btton pressed
    def calculatesci2(self):
        if scitime2 <= 100:
            return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(scitime2)+"%"+" of the expected time.)"
        elif scitime2 < 150:
            return "This student may or may not need extended time, he/she uses " + str(scitime2)+ "%" " of the expected time on exams."
        elif scitime2 == 150: 
            return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(scitime2)+"%"+" of the expected time)"
        elif scitime2 > 150 and scitime2 < 200:
            return "This student takes "+ str(scitime2)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
        elif scitime2 >=200:
            return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(scitime2)+"%"+" of the expected time.)"
        else:
            return none  

    #wl Blocks
    def wladdRow(self):
        # Retrieve text from QLineEdit
        wldate = self.wldate.text()
        wltname = self.wlname.text()
        wlexpect = self.wlexp.text()
        wlactual = self.wlact.text()          
     # Create a empty row at bottom of table
        numRows = self.wltable.rowCount()
        self.wltable.insertRow(numRows)
    # Add text to the row
        self.wltable.setItem(numRows, 0, QtWidgets.QTableWidgetItem(wldate))
        self.wltable.setItem(numRows, 1, QtWidgets.QTableWidgetItem(wltname))
        self.wltable.setItem(numRows, 2, QtWidgets.QTableWidgetItem(wlexpect))
        self.wltable.setItem(numRows, 3, QtWidgets.QTableWidgetItem(wlactual))
# calculate ratio and add ratio to list
        try:
            wlratio= float(wlactual)/float(wlexpect)      
            self.wlratio_list.append(float(wlratio))     
            average=(sum(self.wlratio_list)/len(self.wlratio_list))*100
            global wltime 
           
            wltime= round(average,2)
            self.student["wltime"]=wltime
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass

        
    def calculatewl(self):   
        try:        
            if wltime <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(wltime)+"%"+" of the expected time.)"
            elif wltime < 150:
                return "This student may or may not need extended time, he/she uses " + str(wltime)+ "%" " of the expected time on exams."
            elif wltime == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(wltime)+"%"+" of the expected time)"
            elif wltime > 150 and wltime < 200:
                return "This student takes "+ str(wltime)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif wltime >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(wltime)+"%"+" of the expected time.)"
            else:
                return none
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass
    def wlresultbox(self):
        self.wlresult.setText(self.calculatewl())
        self.wlaccbox.setText(self.calculatewl())

#ela delete 
    def wlremove(self):
        try:
            numRowsrem = self.wltable.rowCount()
            self.wltable.removeRow(numRowsrem-1)
            global wl_ratioup
            wl_ratioup = self.wlratio_list
            del wl_ratioup[-1]
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass

# List update after update button pressed
    def wllstup(self): 
        try:       
            average2=(sum(wl_ratioup)/len(wl_ratioup)*100)
            global wltime2
            wltime2= round(average2,2)
            self.student["wltime2"]=wltime2
#print(average)
            self.wlresult.setText(self.calculatewl2())
            self.wlaccbox.setText(self.calculatewl2())
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass


#Results when update btton pressed
    def calculatewl2(self):
        if wltime2 <= 100:
            return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(wltime2)+"%"+" of the expected time.)"
        elif wltime2 < 150:
            return "This student may or may not need extended time, he/she uses " + str(wltime2)+ "%" " of the expected time on exams."
        elif wltime2 == 150: 
            return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(wltime2)+"%"+" of the expected time)"
        elif wltime2 > 150 and wltime2 < 200:
            return "This student takes "+ str(wltime2)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
        elif wltime2 >=200:
            return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(wltime2)+"%"+" of the expected time.)"
        else:
            return none  

    #enl Blocks
    def enladdRow(self):
        # Retrieve text from QLineEdit
        enldate = self.enldate.text()
        enltname = self.enlname.text()
        enlexpect = self.enlexp.text()
        enlactual = self.enlact.text()          
     # Create a empty row at bottom of table
        numRows = self.enltable.rowCount()
        self.enltable.insertRow(numRows)
    # Add text to the row
        self.enltable.setItem(numRows, 0, QtWidgets.QTableWidgetItem(enldate))
        self.enltable.setItem(numRows, 1, QtWidgets.QTableWidgetItem(enltname))
        self.enltable.setItem(numRows, 2, QtWidgets.QTableWidgetItem(enlexpect))
        self.enltable.setItem(numRows, 3, QtWidgets.QTableWidgetItem(enlactual))
# calculate ratio and add ratio to list
        try:
            enlratio= float(enlactual)/float(enlexpect)       
            self.enlratio_list.append(float(enlratio))       
            average=(sum(self.enlratio_list)/len(self.enlratio_list))*100
            global enltime 
         
            enltime= round(average,2)
            self.student["enltime"]=enltime
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass

        
    def calculateenl(self):   
        try:        
            if enltime <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(enltime)+"%"+" of the expected time.)"
            elif enltime < 150:
                return "This student may or may not need extended time, he/she uses " + str(enltime)+ "%" " of the expected time on exams."
            elif enltime == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(enltime)+"%"+" of the expected time)"
            elif enltime > 150 and enltime < 200:
                return "This student takes "+ str(enltime)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif enltime >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(enltime)+"%"+" of the expected time.)"
            else:
                return none
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass
        
    def enlresultbox(self):
        self.enlresult.setText(self.calculateenl())    
        self.enlaccbox.setText(self.calculateenl())
   
#ela delete 
    def enlremove(self):
        try:
            numRowsrem = self.enltable.rowCount()
            self.enltable.removeRow(numRowsrem-1)
            global enl_ratioup
            enl_ratioup = self.enlratio_list
            del enl_ratioup[-1]
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass

# List update after update button pressed
    def enllstup(self): 
        try:       
            average2=(sum(enl_ratioup)/len(enl_ratioup)*100)
            global enltime2
            enltime2= round(average2,2)
            self.student["enltime2"]=enltime2
#print(average)
            self.enlresult.setText(self.calculatenl2())
            self.enlaccbox.setText(self.calculateenl2())
        except(ValueError, IndexError, ZeroDivisionError, NameError):
            pass


#Results when update btton pressed
    def calculateenl2(self):
        if enltime2 <= 100:
            return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(enltime2)+"%"+" of the expected time.)"
        elif enltime2 < 150:
            return "This student may or may not need extended time, he/she uses " + str(enltime2)+ "%" " of the expected time on exams."
        elif enltime2 == 150: 
            return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(enltime2)+"%"+" of the expected time)"
        elif enltime2 > 150 and enltime2 < 200:
            return "This student takes "+ str(enltime2)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
        elif enltime2 >=200:
            return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(enltime2)+"%"+" of the expected time.)"
        else:
            return none      
    
    def savefile (self):
        
        global elaent1       
        global mathent1        
        global ssent1      
        global scient1       
        global enlent1       
        global wlent1      

        elaent1=None
        mathent1=None
        ssent1=None
        scient1=None
        enlent1=None
        wlent1=None
        try:
            elaent1 = elatime
        except (ValueError, NameError):
            pass
        try:
            mathent1 = mathtime
        except (ValueError, NameError):
            pass        
        try:
            scient1 = scitime
        except (ValueError, NameError):
            pass       
        try:    
            ssent1 = sstime
        except (ValueError, NameError):
            pass        
        try:
            enlent1 = enltime
        except (ValueError, NameError):
            pass       
        try:
            wlent1 = wltime
        except (ValueError, NameError):
            pass
                   
        db = sqlite3.connect('TimeAccommodations.db')
        cursor=db.cursor()

        stname=self.stunamebox.text()

        cursor.execute('''INSERT INTO students(name, elat1, matht1, sst1, scit1, wlt1, enlt1)VALUES(?,?,?,?,?,?,?)''', (stname,elaent1,mathent1,ssent1,scient1,wlent1,enlent1,))
        db.commit()
        db.close()
        f= open('student_names.txt','a')
        f.write('; '+ stname)
        f.close


    def loadfile(self):
        db = sqlite3.connect('TimeAccommodations.db')
        cursor=db.cursor()
        global stdntinfo
        try:
            stname1=self.stunameexist.text()        
            cursor.execute('''SELECT elat1, matht1, sst1, scit1, wlt1, enlt1 FROM students WHERE name=?''', (stname1,))            
            stdntinfo=cursor.fetchone()
          
            tuple(stdntinfo)
            
           
            
        except (TypeError,NameError):
            pass
        self.elaaccbox.setText(self.calculateela4())
        self.mathaccbox.setText(self.calculatemath4())
        self.ssacbox.setText(self.calculatess4())
        self.sciaccbox.setText(self.calculatesci4())
        self.wlaccbox.setText(self.calculatewl4())
        self.enlaccbox.setText(self.calculateenl4())
        


    def updatestudent(self):
        db = sqlite3.connect('TimeAccommodations.db')
        cursor=db.cursor()
        global elati1
        global mathti1
        global ssti1
        global sciti1
        global wlti1
        global enlti1

        elati1 = None
        mathti1 = None
        ssti1 = None
        sciti1 = None
        wlti1 = None
        enlti1 = None

        try:
            if stdntinfo[0] is not None:
                elati1=stdntinfo[0]
            else:
                try:
                    elati1 = elatime
                except (TypeError,NameError):
                    pass
    
            if stdntinfo[1] is not None:
                mathti1=stdntinfo[1]
            else:
                try:
                    mathti1=mathtime
                except (TypeError,NameError):
                    pass
        
            if stdntinfo[2] is not None:
                ssti1=stdntinfo[2]
            else:
                try:
                    ssti1=sstime
                except (TypeError,NameError):
                    pass
        
            if stdntinfo[3] is not None:
                sciti1=stdntinfo[3]
            else:
                try:
                    sciti1 = scitime
                except (TypeError,NameError):
                    pass
        
            if stdntinfo[4] is not None:
                wlti1=stdntinfo[4]
            else:
                try:
                    wlti1 = wltime
                except (TypeError,NameError):
                    pass
    
            if stdntinfo[5] is not None:
                enlti1=stdntinfo[5]
            else:
                try:
                    enlti1 = enltime
                except (TypeError,NameError):
                    pass
        except (NameError,TypeError):
            pass


        global new_ela1
        global new_math1
        global new_ss1
        global new_sci1
        global new_wl1
        global new_enl1
        
        new_ela1 =None
        new_math1 =None
        new_ss1 =None
        new_sci1 =None
        new_wl1 =None
        new_enl1 =None
        stname2=self.stunameexist.text()
        
        try:
            if elati1 is not None:
                try:
                    new_ela1 = round((elatime+elati1)/2,2)                
                except (NameError):                
                    pass
            else:
                new_ela1=elatime
            
            if mathti1 is not None:             
                try:                
                    new_math1 = round((mathtime + mathti1)/2,2)                
                except(NameError):                
                    pass
            else:
                new_math1=mathtime    
                
            if ssti1 is not None: 
                try:                    
                    new_ss1 = round(( sstime+ssti1 )/2,2)                
                except(NameError):                
                    pass    
                else: new_ss1=sstime 
                
            if sciti1 is not None:
                try:                
                    new_sci1 = round((scitime+sciti1)/2,2)            
                except(NameError):            
                    pass    
            
            if wlti1 is not None:    
                try:                
                    new_wl1 = round(( wltime+wlti1 )/2,2)            
                except(NameError):            
                    pass    
                
            if enlti1 is not None:    
                try:                
                    new_enl1 = round((enltime + enlti1)/2,2)            
                except(NameError):            
                    pass 
        except (TypeError, NameError):
            pass

        if new_ela1 is not None:
            cursor.execute('''UPDATE students SET elat1 = ? WHERE name= ?''',(new_ela1,stname2))
        else:
            pass
        if new_math1 is not None:
            cursor.execute('''UPDATE students SET matht1 = ? WHERE name= ?''',(new_math1,stname2))
        else:
            pass
        if new_ss1 is not None:            
            cursor.execute('''UPDATE students SET sst1 = ? WHERE name= ?''',(new_ss1,stname2))
        else:
            pass
        if new_sci1 is not None:
            cursor.execute('''UPDATE students SET scit1 = ? WHERE name= ?''',(new_sci1,stname2))
        else:
            pass
        if new_wl1 is not None:              
            cursor.execute('''UPDATE students SET wlt1  =? WHERE name= ?''',(new_wl1,stname2))
        else:
            pass
        if new_enl1 is not None:                
            cursor.execute('''UPDATE students SET enlt1 = ? WHERE name= ?''',(new_enl1,stname2))
        else:
            pass
          
        
        db.commit()
        db.close()
     

        if new_ela1 is not None:
            self.elaaccbox.setText(self.calculateela3())
        else: 
            pass
        if new_math1 is not None:
            self.mathaccbox.setText(self.calculatemath3())
        else: 
            pass
        if new_sci1 is not None:
            self.sciaccbox.setText(self.calculatesci3())
        else: 
            pass
        if new_ss1 is not None:
            self.ssacbox.setText(self.calculatess3())
        else: 
            pass
        if new_wl1 is not None:
            self.wlaccbox.setText(self.calculatewl3())
        else: 
            pass
        if new_enl1 is not None:
            self.enlaccbox.setText(self.calculateenl3())
        else: 
            pass
        




    def calculateela3(self):
        try:    
            if new_ela1 <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(new_ela1)+"%"+" of the expected time.)"
            elif new_ela1 < 150:
                return "This student may or may not need extended time, he/she uses " + str(new_ela1)+ "%" " of the expected time on exams."
            elif new_ela1 == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(new_ela1)+"%"+" of the expected time)"
            elif new_ela1 > 150 and new_ela1 < 200:
                return "This student takes "+ str(new_ela1)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif new_ela1 >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(new_ela1)+"%"+" of the expected time.)"
            else:
                return none 
        except(TypeError):
            pass

    def calculateela4(self):
        try:
            if stdntinfo[0] <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(stdntinfo[0])+"%"+" of the expected time.)"
            elif stdntinfo[0] < 150:
                return "This student may or may not need extended time, he/she uses " + str(stdntinfo[0])+ "%" " of the expected time on exams."
            elif stdntinfo[0] == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(stdntinfo[0])+"%"+" of the expected time)"
            elif stdntinfo[0] > 150 and stdntinfo[0] < 200:
                return "This student takes "+ str(stdntinfo[0])+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif stdntinfo[0] >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(stdntinfo[0])+"%"+" of the expected time.)"
            else:
                return none 
        except(TypeError):
            pass

    def calculatemath3(self):
        try:
            if new_math1 <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(new_math1)+"%"+" of the expected time.)"
            elif new_math1 < 150:
                return "This student may or may not need extended time, he/she uses " + str(new_math1)+ "%" " of the expected time on exams."
            elif new_math1 == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(new_math1)+"%"+" of the expected time)"
            elif new_math1 > 150 and new_math1 < 200:
                return "This student takes "+ str(new_math1)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif new_math1 >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(new_math1)+"%"+" of the expected time.)"
            else:
                return none 
        except TypeError:
            pass

    def calculatemath4(self):
        try:
            if stdntinfo[1] <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(stdntinfo[1])+"%"+" of the expected time.)"
            elif stdntinfo[1] < 150:
                return "This student may or may not need extended time, he/she uses " + str(stdntinfo[1])+ "%" " of the expected time on exams."
            elif stdntinfo[1] == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(stdntinfo[1])+"%"+" of the expected time)"
            elif stdntinfo[1] > 150 and stdntinfo[1] < 200:
                return "This student takes "+ str(stdntinfo[1])+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif stdntinfo[1] >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(stdntinfo[1])+"%"+" of the expected time.)"
            else:
                return none 
        except TypeError:
            pass

    def calculatess3(self):
        try:
            if new_ss1 <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(new_ss1)+"%"+" of the expected time.)"
            elif new_ss1 < 150:
                return "This student may or may not need extended time, he/she uses " + str(new_ss1)+ "%" " of the expected time on exams."
            elif new_ss1 == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(new_ss1)+"%"+" of the expected time)"
            elif new_ss1 > 150 and new_ss1 < 200:
                return "This student takes "+ str(new_ss1)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif new_ss1 >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(new_ss1)+"%"+" of the expected time.)"
            else:
                return none 
        except TypeError:
            pass

    def calculatess4(self):
        try:
            if stdntinfo[2] <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(stdntinfo[2])+"%"+" of the expected time.)"
            elif stdntinfo[2] < 150:
                return "This student may or may not need extended time, he/she uses " + str(stdntinfo[2])+ "%" " of the expected time on exams."
            elif stdntinfo[2] == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(stdntinfo[2])+"%"+" of the expected time)"
            elif stdntinfo[2] > 150 and(stdntinfo[2]) < 200:
                return "This student takes "+ str(stdntinfo[2])+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif stdntinfo[2] >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(stdntinfo[2])+"%"+" of the expected time.)"
            else:
                return none 
        except TypeError:
            pass

    def calculatesci3(self):
        try:
            if new_sci1 <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(new_sci1)+"%"+" of the expected time.)"
            elif new_sci1 < 150:
                return "This student may or may not need extended time, he/she uses " + str(new_sci1)+ "%" " of the expected time on exams."
            elif new_sci1 == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(new_sci1)+"%"+" of the expected time)"
            elif new_sci1 > 150 and new_sci1 < 200:
                return "This student takes "+ str(new_sci1)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif new_sci1 >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(new_sci1)+"%"+" of the expected time.)"
            else:
                return none
        except TypeError:
            pass 

    def calculatesci4(self):
        try:
            if stdntinfo[3] <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(stdntinfo[3])+"%"+" of the expected time.)"
            elif stdntinfo[3] < 150:
                return "This student may or may not need extended time, he/she uses " + str(stdntinfo[3])+ "%" " of the expected time on exams."
            elif stdntinfo[3] == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(stdntinfo[3])+"%"+" of the expected time)"
            elif stdntinfo[3] > 150 and stdntinfo[3] < 200:
                return "This student takes "+ str(stdntinfo[3])+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif stdntinfo[3] >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(stdntinfo[3])+"%"+" of the expected time.)"
            else:
                return none
        except TypeError:
            pass 

    def calculatewl3(self):
        try:
            if new_wl1 <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(new_wl1)+"%"+" of the expected time.)"
            elif new_wl1 < 150:
                return "This student may or may not need extended time, he/she uses " + str(new_wl1)+ "%" " of the expected time on exams."
            elif new_wl1 == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(new_wl1)+"%"+" of the expected time)"
            elif new_wl1 > 150 and new_ss2 < 200:
                return "This student takes "+ str(new_wl1)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif new_wl1 >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(new_wl1)+"%"+" of the expected time.)"
            else:
                return none
        except TypeError:
            pass 

    def calculatewl4(self):
        try:
            if stdntinfo[4] <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(stdntinfo[4])+"%"+" of the expected time.)"
            elif stdntinfo[4] < 150:
                return "This student may or may not need extended time, he/she uses " + str(stdntinfo[4])+ "%" " of the expected time on exams."
            elif stdntinfo[4] == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(stdntinfo[4])+"%"+" of the expected time)"
            elif stdntinfo[4] > 150 and stdntinfo[4] < 200:
                return "This student takes "+ str(stdntinfo[4])+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif stdntinfo[4] >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(stdntinfo[4])+"%"+" of the expected time.)"
            else:
                return none
        except TypeError:
            pass 

    def calculateenl3(self):
        try:
            if new_enl1 <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(new_enl1)+"%"+" of the expected time.)"
            elif new_enl1 < 150:
                return "This student may or may not need extended time, he/she uses " + str(new_enl1)+ "%" " of the expected time on exams."
            elif new_enl1 == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(new_enl1)+"%"+" of the expected time)"
            elif new_enl1 > 150 and new_enl1 < 200:
                return "This student takes "+ str(new_enl1)+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif new_enl1 >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(new_enl1)+"%"+" of the expected time.)"
            else:
                return none
        except TypeError:
            pass 

    def calculateenl4(self):
        try:
            if stdntinfo[5] <= 100:
                return "This student may not require extra time for this subject." +" ("+"He/she currently uses "+str(stdntinfo[5])+"%"+" of the expected time.)"
            elif stdntinfo[5] < 150:
                return "This student may or may not need extended time, he/she uses " + str(stdntinfo[5])+ "%" " of the expected time on exams."
            elif stdntinfo[5] == 150: 
                return "This student may need time and a half on exams for this subject." + " ("+"He/she currently uses an average of "+str(stdntinfo[5])+"%"+" of the expected time)"
            elif stdntinfo[5] > 150 and stdntinfo[5] < 200:
                return "This student takes "+ str(stdntinfo[5])+ "%"+ " of the expected time on exams in this subject. This suggests that the student may need time and a half or double time"
            elif stdntinfo[5] >=200:
                return "This student may need double time on exams for this subject ."+" ("+"He/she currently uses "+str(stdntinfo[5])+"%"+" of the expected time.)"
            else:
                return none
        except TypeError:
            pass 


if __name__ == '__main__':
   
    app = QtWidgets.QApplication(sys.argv)
    splash_pix = QtGui.QPixmap('disclaimer.png')
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    #splash.showMessage('Hello!',)
    splash.show()
    tm.sleep(0)
    app.processEvents()
    window = Accapp()
    window.show()   
    sys.exit(app.exec_())

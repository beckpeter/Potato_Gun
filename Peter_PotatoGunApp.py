# Generated from reading ui file 'PotatoGunApp.ui'
from __future__ import unicode_literals
from PyQt4 import QtCore, QtGui
import sys

#imports for interface with DAQ and with excel
import ExcelTools
from MultiChannelAnalogInput import *
import numpy as np
import time

#imports for matplotlib
import os
from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#The channels for each type of sensor
PTChan=[]
for number in range(2):
    PTChan.append('Dev1/ai'+str(number))
PRChan=[]
for number in range(6):
    PRChan.append('Dev1/ai'+str(number+2))


AnimateRefreshTime=1000 #ms

#All the global variables I was too lazy to make local
global sheetnames
sheetnames=[]
global sheet
sheet = 'Sheet'
global name
name = ''
global animateFlag
animateFlag=False
global StaticData
global AnimateData
global ChanList
StaticData={'time':[0,1]}
AnimateData={'time':[0,1]}
ChanList=[]
for n in range(8):
    ChanList.append('Dev1/ai'+str(n))
    StaticData[ChanList[n]]=[0,0]
    AnimateData[ChanList[n]]=[0,0]
global PTList
global PRList
PTList = ChanList[0:1]
PRList = ChanList[2:7]

#Access DAQ
global MCAI
MCAI=MultiChannelAnalogInput(ChanList)


def PTCalib(voltage):
    m=1
    offset=-.47
    pressure = m*(voltage - offset)
    return pressure
    
class SheetList(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)        
        self.widget = QtGui.QWidget()
        self.setCentralWidget(self.widget)
        self.setWindowTitle("Win2")
        self.gridLayout = QtGui.QGridLayout()      
        self.listWidget = QtGui.QListWidget()
        global sheetnames
        for n in range(len(sheetnames)):
            item = QtGui.QListWidgetItem()
            item.setText(sheetnames[n])
            self.listWidget.addItem(item)
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)
        ##
        #the buttonBox
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Open)
        self.buttonBox.accepted.connect(self.get_sheet)
        ##
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.widget.setLayout(self.gridLayout)
    def get_sheet(self):
        n=0
        while True:
            if self.listWidget.item(n).isSelected() == True:
                global sheet
                sheet = sheetnames[n]
            n+=1
            if self.listWidget.item(n) == None:
                break
        global StaticData
        StaticData=ExcelTools.readData(name,sheet)
        
class MPLCanvas(FigureCanvas):
    '''Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.).'''
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    def compute_initial_figure(self):
        pass
class StaticPRMPL(MPLCanvas):
    """A canvas that updates itself every .5 second with a new plot."""
    def __init__(self, *args, **kwargs):
        MPLCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)
    def compute_initial_figure(self):
        global StaticData
        self.axes.plot(StaticData['time'],StaticData['Dev1/ai0'], 'r')
        self.axes.set_title('PR')
    def update_figure(self):
        global StaticData
        self.axes.cla()
        for key in PRChan:
            self.axes.plot(StaticData['time'],StaticData[key],'r')
        self.axes.set_title('PR')
        self.draw()

class StaticPTMPL(MPLCanvas):
    """A canvas that updates itself every .5 second with a new plot."""
    def __init__(self, *args, **kwargs):
        MPLCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)
    def compute_initial_figure(self):
        self.axes.plot([0, 1], [0,0], 'b')
        self.axes.set_title('PT')
    def update_figure(self):
        global StaticData
        self.axes.cla()
        for key in PTChan:
            self.axes.plot(StaticData['time'],StaticData[key],'b')
        self.axes.set_title('PT')
        self.draw()    
class DynamicPRMPL(MPLCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MPLCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(AnimateRefreshTime)
    def compute_initial_figure(self):
        self.axes.plot([0, 1], [0,0], 'r')
        self.axes.set_title('PR')
    global animateFlag  
    def update_figure(self):
        self.axes.cla()
        if animateFlag==True:
            global AnimateData
            self.axes.cla()
            for key in PRChan:
                self.axes.plot(AnimateData['time'],AnimateData[key],'r')
            self.axes.set_title('PR')
            self.draw()
        else:
            pass
        
        
class DynamicPTMPL(MPLCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MPLCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(AnimateRefreshTime)
    def compute_initial_figure(self):
        self.axes.plot([0, 1], [0,0], 'b')
        self.axes.set_title('PT')
    def update_figure(self):
        self.axes.cla()
        if animateFlag==True:
            global AnimateData
            self.axes.cla()
            for key in PTChan:
                self.axes.plot(AnimateData['time'],AnimateData[key],'b')
            self.axes.set_title('PT')
            self.draw()
        else:
            pass


class Ui_PotatoGunTestingApp(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(Ui_PotatoGunTestingApp, self).__init__(parent)
        PotatoGunTestingApp.resize(1000, 800)
        self.centralwidget = QtGui.QWidget(PotatoGunTestingApp)
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)

        #All graph widgets are here
        self.staticPRGraph = StaticPRMPL(self.centralwidget)
        self.staticPTGraph = StaticPTMPL(self.centralwidget)
        self.animatedPRGraph = DynamicPRMPL(self.centralwidget)
        self.animatedPTGraph = DynamicPTMPL(self.centralwidget)

        self.gridLayout.addWidget(self.staticPRGraph, 11, 1, 1, 1)
        self.gridLayout.addWidget(self.animatedPRGraph, 11, 0, 1, 1)
        self.gridLayout.addWidget(self.staticPTGraph, 8, 1, 1, 1)
        self.gridLayout.addWidget(self.animatedPTGraph, 8, 0, 1, 1)
        ##
        
        self.formLayout = QtGui.QFormLayout()
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        
        #All buttons are here
        #definitions
        self.startButton = QtGui.QPushButton(self)
        self.startButton.setText('Start Mointoring Signals')
        self.startButton.clicked.connect(self.animate_start)
        self.stopButton = QtGui.QPushButton(self)
        self.stopButton.setText('Stop Mointoring Signals')
        self.stopButton.clicked.connect(self.animate_stop)
        self.runButton = QtGui.QPushButton(self)
        self.runButton.setText('Run Test')
        self.runButton.clicked.connect(self.run_test)
        #placement
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.startButton)        
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.stopButton)
        self.gridLayout.addLayout(self.formLayout, 4, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.runButton)

        ##
        #All titles and labesl
        font = QtGui.QFont()
        font.setPointSize(10)
        self.animateTitle = QtGui.QLabel(self.centralwidget)
        self.animateTitle.setFont(font)
        self.animateTitle.setText('Animated Graphs')
        self.staticTitle = QtGui.QLabel(self.centralwidget)
        self.staticTitle.setFont(font)
        self.staticTitle.setText('Static Graphs')
        self.titleLabel = QtGui.QLabel(self.centralwidget)        
        font.setPointSize(13)
        self.titleLabel.setFont(font)
        self.titleLabel.setText('Graph of ______')
        self.gridLayout.addWidget(self.animateTitle, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.animateTitle, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.staticTitle, 6, 1, 1, 1)
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 2, QtCore.Qt.AlignHCenter)
        ##
        
        #Progress Bar def
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        
        self.verticalLayout_2.addWidget(self.progressBar)
        self.gridLayout.addLayout(self.verticalLayout_2, 4, 1, 1, 1)
        
        PotatoGunTestingApp.setCentralWidget(self.centralwidget)
        
        self.statusbar = QtGui.QStatusBar(PotatoGunTestingApp)
        PotatoGunTestingApp.setStatusBar(self.statusbar)

        #All menu items are below
        self.menubar = QtGui.QMenuBar(PotatoGunTestingApp)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 773, 26))
        self.menuFile = QtGui.QMenu('&File', self)
        self.menuEdit = QtGui.QMenu('&Edit',self)
        self.menuRun = QtGui.QMenu('&Run',self)
        PotatoGunTestingApp.setMenuBar(self.menubar)
        self.menuFile.addAction('&Open',self.file_open,QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        self.menuFile.addAction('&Save',self.file_save,QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.menuFile.addSeparator()
        self.menuFile.addAction('&Exit',self.close_app,QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuEdit.addAction('&Assign Channels',self.assign_channels,QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.menuRun.addAction('&Run Test',self.run_test,QtCore.Qt.CTRL + QtCore.Qt.Key_R)
        self.menuRun.addAction('&Progress Bar',self.progress_bar,QtCore.Qt.CTRL + QtCore.Qt.Key_T)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        ##

        #two different styles, both are good
        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))

        QtGui.QApplication.setWindowIcon(QtGui.QIcon('potato.ico'))
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.get_animate_data)
        timer.start(AnimateRefreshTime)

        QtCore.QMetaObject.connectSlotsByName(PotatoGunTestingApp)
    #definitions of button and menu button methods
    def close_app(self):
        choice = QtGui.QMessageBox.question(self, 'Quit!',"Do you really want to quit?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass
    def file_open(self):
        global name
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        sheetnames = ExcelTools.getSheetNames(name)
        choice = QtGui.QMessageBox.question(self, 'Open File',
                                            '''Opening this file will overwrite any data you currently have.
                                            Are you sure you want to do this?''',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            global sheetnames
            sheetnames = ExcelTools.getSheetNames(name)
            self.w = SheetList()
            self.w.show()
        else:
            pass
    def file_save(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        if '' == name:
            pass
        else:
            name=name+'.xlsx'
            global StaticData
            ExcelTools.saveData(StaticData,name)
    def run_test(self):
        global animateFlag
        animateFlag=False        
        global StaticData
        global MCAI
        StaticData = MCAI.readMulti(timelength=10,samplerate=1000)
        for key in StaticData:
            if key in PTChan:
                for n in range(len(StaticData[key])):
                    StaticData[key][n]=PTCalib(StaticData[key][n])
        self.file_save()
    def progress_bar(self):
        self.completed = 0
        while self.completed <100:
            self.completed +=0.0001
            self.progressBar.setValue(self.completed)

    def animate_start(self):
        global animateFlag
        animateFlag = True
    def animate_stop(self):
        global animateFlag
        animateFlag=False
    def assign_channels(self):
        pass
    def get_animate_data(self):
        if animateFlag:
            global AnimateData
            global MCAI
            temp_data=MCAI.readMulti(timelength=.002)
            for n in range(1):
                for key in AnimateData:
                    if key in PTChan:
                        temp_data[key][n]=PTCalib(temp_data[key][n])
                    AnimateData[key].append(temp_data[key][n])
            if len(AnimateData['time'])>20:
                for key in AnimateData:
                    my_list = AnimateData[key]
                    AnimateData[key]=my_list[-19:]            
        pass

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PotatoGunTestingApp = QtGui.QMainWindow()
    ui = Ui_PotatoGunTestingApp()
    PotatoGunTestingApp.show()
    sys.exit(app.exec_())


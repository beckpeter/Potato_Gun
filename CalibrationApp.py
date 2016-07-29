from PyQt4 import QtCore, QtGui
#imports for matplotlib
import os
from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#custom imports for the DAQ and excel
from MultiChannelAnalogInput import *
import ExcelTools
import time


AnimateRefreshTime=1000#ms
global AnimateData
AnimateData={'pressure':[0,1]}
ChanList=[]
for n in range(2):
    ChanList.append('Dev1/ai'+str(n))
    AnimateData[ChanList[n]]=[0,0]
PTChan=ChanList

global Started
Started = False

#Access DAQ
global MCAI
MCAI = MultiChannelAnalogInput(ChanList)

####NEED MCAI MODULE
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
class DynamicPTMPL(MPLCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MPLCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(AnimateRefreshTime)
    def compute_initial_figure(self):
        self.axes.plot([0, 1], [0,0], 'or')
        self.axes.set_title('PT')
    def update_figure(self):
        self.axes.cla()
        global AnimateData
        self.axes.cla()
        for key in PTChan:
            self.axes.plot(AnimateData['pressure'],AnimateData[key],'or')
        self.axes.set_title('PT')
        self.draw()

class AskPressure(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.widget = QtGui.QWidget()
        self.setCentralWidget(self.widget)
        self.setWindowTitle('Pressure?')
        self.verticalLayout = QtGui.QVBoxLayout()
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.getText)
        self.lineEdit = QtGui.QLineEdit()
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addWidget(self.lineEdit)
        self.widget.setLayout(self.verticalLayout)
    def getText(self):
        myanswer=float(self.lineEdit.text())
        for n in range(100):
            myvoltagedict=MCAI.readSingle()
            myvoltagedict['pressure']=myanswer
            global AnimateData
            global Started
            if Started: 
                for key in AnimateData:
                    AnimateData[key].append(myvoltagedict[key])
            else:
                Started=True
                for key in myvoltagedict:
                    if key != 'time':
                        AnimateData[key]=[myvoltagedict[key]]

class Ui_PotatoGunTestingApp(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(Ui_PotatoGunTestingApp,self).__init__(parent)
        PotatoGunTestingApp.resize(1000, 800)
        self.centralwidget = QtGui.QWidget(PotatoGunTestingApp)
        PotatoGunTestingApp.setCentralWidget(self.centralwidget)
        
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        ###
        self.startButton = QtGui.QPushButton(self)
        self.startButton.setText('Get Voltage')
        self.startButton.clicked.connect(self.get_pressure)

        self.stopButton = QtGui.QPushButton(self)
        self.stopButton.setText('Save')
        self.stopButton.clicked.connect(self.save)

        self.animatedPTGraph = DynamicPTMPL(self.centralwidget)
        self.gridLayout.addWidget(self.startButton,0,0,2,1)
        self.gridLayout.addWidget(self.stopButton,0,1,2,1)
        self.gridLayout.addWidget(self.animatedPTGraph,1,0,2,1)
        
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
        QtGui.QApplication.setWindowIcon(QtGui.QIcon('potato.ico'))
        QtCore.QMetaObject.connectSlotsByName(PotatoGunTestingApp)
    def get_pressure(self):
          self.w = AskPressure()
          self.w.show()
    def save(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        if '' == name:
            pass
        else:
            name=name+'.xlsx'
            global AnimateData
            ExcelTools.saveData(AnimateData,name)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PotatoGunTestingApp = QtGui.QMainWindow()
    ui = Ui_PotatoGunTestingApp()
    PotatoGunTestingApp.show()
    sys.exit(app.exec_())


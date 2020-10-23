from functools import partial

import run
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QMessageBox


class MyMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initWinUI()

    def initWinUI(self):

        ### Set the central widget ###
        ma = run.MyApp()
        self.setCentralWidget(ma)

        ### Set the Actions for the menu bar and the tool bar ###
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        saveAction = QAction(QIcon('save.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save Search Results')
        saveAction.triggered.connect(partial(ma.file_btn_click_event, clicked_btn='save'))

        printAction = QAction(QIcon('print.png'), 'Print', self)
        printAction.setShortcut('Ctrl+P')
        printAction.setStatusTip('Print Search Results')
        printAction.triggered.connect(partial(ma.file_btn_click_event, clicked_btn='print'))

        self.statusBar()

        ### Set the menu bar ###
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)
        filemenu.addAction(saveAction)
        filemenu.addAction(printAction)

        aboutmenu = menubar.addMenu('About')
        aboutAction = QAction('About',self)
        aboutAction.setStatusTip('About')
        aboutAction.triggered.connect(self.aboutdialog)
        aboutmenu.addAction(aboutAction)

        ### Set the tool bar ####
#        self.toolbar = self.addToolBar('Exit')
#        self.toolbar.addAction(exitAction)
#        self.toolbar = self.addToolBar('Save')
#        self.toolbar.addAction(saveAction)
#        self.toolbar = self.addToolBar('Print')
#        self.toolbar.addAction(printAction)

#        self.setWindowTitle('Toxicity-Mass Database')
        self.setGeometry(300, 300, 500, 500)
#        self.setMinimumSize(self,1100, 697.5)
        self.resize(2100,1100)


        self.setWindowTitle('TOXMASS 1.0')
        self.show()


    def aboutdialog(self):
        aboutmsg = "This is a software with both toxicity database and MS spectrum database. \n\nThe toxicity DB is obtained from PubChem.\n\nThe current version is 1.0\n"
        QMessageBox.information(self, "QMessageBox.information()", aboutmsg)

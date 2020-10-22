import os
import utils
import matplotlib.pyplot as plt
from functools import partial
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QGroupBox, QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QTextEdit, QRadioButton, QPushButton,
                             QTableWidget, QTableWidgetItem, QCheckBox, QComboBox, QMessageBox,
                             QFileDialog)
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QTextCursor
from PyQt5.Qt import QFileInfo
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.loadDB()
        self.initUI()
    
    ### 1. DB load ###
    def loadDB(self):
        self.toxic_db, self.msms_db = utils.load_db()
        
    ### 2. UI initialization ###
    def initUI(self):
        grid = QGridLayout()
        
        left_grid = QGridLayout()
        self.search_grid = self._create_search_grid()
        self.info_grid = self._create_info_grid()
        self.action_grid = self._create_action_grid()
        left_grid.addWidget(self.search_grid)
        left_grid.addWidget(self.info_grid)
        left_grid.addWidget(self.action_grid)

        right_grid = QGridLayout()
        self.poison_grid = self._create_poison_grid()
        self.mass_grid, self.mass_layout = self._create_mass_grid()
        right_grid.addWidget(self.poison_grid)
        right_grid.addWidget(self.mass_grid)
                
        grid.addLayout(left_grid, 0, 0, 1, 1)
        grid.addLayout(right_grid, 0, 1, 1, 3)

        ## (Added) Fix the left grid #################
        grid.setColumnStretch(0, 0.1)
        grid.setColumnStretch(1, 2)
        ##############################################

        self.setWindowTitle('TOXMASS 1.0')
        self.setLayout(grid)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 2.1 Create search grid
    def _create_search_grid(self):
        groupbox = QGroupBox('')
        
        # Search layout
        search_group = QGroupBox('Search')
        search_layout = QHBoxLayout()
        
        self.search_type_list = QComboBox()
        self.search_type_list.addItem('CAS')
        self.search_type_list.addItem('IUPAC')
        self.search_type_list.addItem('SMILES')
        
        search_btn = QPushButton('Search')
        search_btn.clicked.connect(self.search_btn_click_event)  # Refer to 2.1.3 function

        self.search_line = QLineEdit('')
        self.search_line.resize(self.search_line.sizeHint())
        self.search_line.returnPressed.connect(search_btn.click)  # Refer to 2.1.3 function

        search_layout.addWidget(self.search_type_list)
        search_layout.addWidget(self.search_line)
        search_layout.addWidget(search_btn)
        search_group.setLayout(search_layout)
        
        # Species layout
        species_group = QGroupBox('Species')
        species_layout = QVBoxLayout()
        
        self.species_all = QCheckBox('all')
        self.species_all.stateChanged.connect(self.species_all_btn_click_event)  # Refer to 2.1.1 function
        self.species_btn1 = QCheckBox('zebra fish')
        self.species_btn2 = QCheckBox('fathead minnow')
        self.species_btn3 = QCheckBox('medaka')
        self.species_btn4 = QCheckBox('daphnia')
        self.species_others = QCheckBox('others')
        
        species_layout.addWidget(self.species_all)
        species_layout.addWidget(self.species_btn1)
        species_layout.addWidget(self.species_btn2)
        species_layout.addWidget(self.species_btn3)
        species_layout.addWidget(self.species_btn4)
        species_layout.addWidget(self.species_others)
        species_group.setLayout(species_layout)
        
        # Endpoint layout
        endpoint_group = QGroupBox('End point')
        endpoint_layout = QVBoxLayout()

        self.ep_all = QCheckBox('all')
        self.ep_all.stateChanged.connect(self.endpoint_all_btn_click_event)  # Refer to 2.1.2 function
        self.ep_lc_btn = QCheckBox('LC50')
        self.ep_ec_btn = QCheckBox('EC50')
        self.ep_others = QCheckBox('others')
        
        endpoint_layout.addWidget(self.ep_all)
        endpoint_layout.addWidget(self.ep_lc_btn)
        endpoint_layout.addWidget(self.ep_ec_btn)
        endpoint_layout.addWidget(self.ep_others)
        endpoint_group.setLayout(endpoint_layout)
                
        vbox = QVBoxLayout()
        vbox.addWidget(search_group)
        vbox.addWidget(species_group)
        vbox.addWidget(endpoint_group)
        groupbox.setLayout(vbox)

        return groupbox
    
    # 2.2 Create info grid
    def _create_info_grid(self):
        groupbox = QGroupBox('Chemical Information')
       
        self.info_table = QTableWidget()
        self.info_table.setColumnCount(1)
        self.info_table.horizontalHeader().setVisible(False)
        self.info_table.setRowCount(4)
        self.info_table.setVerticalHeaderLabels(["Name", "IUPAC name", "CAS number", "SMILES"])
        self.info_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.info_table)
        groupbox.setLayout(vbox)
#        QTableWidget.setMinimumSize(self.info_table, 357, 120)
        self.info_table.setRowHeight(0,groupbox.height()/16)
        self.info_table.setRowHeight(1,groupbox.height()/16)
        self.info_table.setRowHeight(2,groupbox.height()/16)
        self.info_table.setRowHeight(3,groupbox.height()/16)
#        self.info_table.setColumnWidth(0, 300)
        QTableWidget.setMinimumSize(self.info_table, 357, groupbox.height()/4)
        QTableWidget.setFixedSize(self.info_table,357,groupbox.height()/4)

        vbox.addStretch(0.001)

        return groupbox

    def _create_action_grid(self):
        groupbox = QGroupBox(' ')

        action_layout = QHBoxLayout()
#
        save_btn = QPushButton('Save')
        save_btn.clicked.connect(partial(self.file_btn_click_event, clicked_btn='save'))  # Refer to 2.4.1 function
#
        print_btn = QPushButton('Print')
        print_btn.clicked.connect(partial(self.file_btn_click_event, clicked_btn='print'))  # Refer to 2.4.1 function
#
        action_layout.addWidget(save_btn)
        action_layout.addWidget(print_btn)
        groupbox.setLayout(action_layout)
        return groupbox
    
    # 2.3 Create poison grid
    def _create_poison_grid(self):
        groupbox = QGroupBox('')
        
        self.poison_text = QTextEdit('')
        self.poison_text.setReadOnly(True)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.poison_text)
        groupbox.setLayout(vbox)

        return groupbox

    # (Added) Create mass metadata grid
    def _create_mass_metadata_grid(self):
        groupbox = QGroupBox('')
        self.msinfo_table = QTableWidget()
        self.msinfo_table.setColumnCount(1)
        self.msinfo_table.horizontalHeader().setVisible(False)
        self.msinfo_table.setRowCount(4)

        self.msinfo_table.setVerticalHeaderLabels(["        ", "        ", " ", " "])

        self.header_list = []
#        self.msinfo_table.setVerticalHeaderLabels(["              ", " ", " ", " "])
        self.msinfo_table.setEditTriggers(QTableWidget.NoEditTriggers)


        self.msinfo_table.setColumnWidth(0, 250)

        vbox = QVBoxLayout()
        vbox.addWidget(self.msinfo_table)
        groupbox.setLayout(vbox)

        return groupbox
    
    # 2.4 Create mass grid
    def _create_mass_grid(self):
        groupbox = QGroupBox('')
        
        mass_layout = QVBoxLayout()
                
        self.mass_fig = plt.Figure()
        self.mass_canvas = FigureCanvas(self.mass_fig)
        
        self.mass_fig.clear()
        ax = self.mass_fig.add_subplot(111)
        ax.set_yticks([0, 20, 40, 60, 80, 100])
        ax.set_xlabel('m/z')
        ax.set_ylabel('Intensity')
        plt.tight_layout()
        self.mass_canvas.draw()
        
        # Create reference line
        self.reference_line = QLineEdit('')
        self.reference_line.setReadOnly(True)

        # (Added) Create mass info
        self.mass_info_group = QGroupBox('')
        mass_info_layout = QHBoxLayout()

        # Create save and print button
#        self.save_print_group = QGroupBox('')
#        save_print_layout = QHBoxLayout()

#        info_btn = QPushButton('Info')
#        info_btn.clicked.connect(partial(self.file_btn_click_event, clicked_btn='info'))

#        save_btn = QPushButton('Save')
#        save_btn.clicked.connect(partial(self.file_btn_click_event, clicked_btn='save'))  # Refer to 2.4.1 function

#        print_btn = QPushButton('Print')
#        print_btn.clicked.connect(partial(self.file_btn_click_event, clicked_btn='print'))  # Refer to 2.4.1 function

#        save_print_layout.addWidget(info_btn)
#        save_print_layout.addWidget(save_btn)
#        save_print_layout.addWidget(print_btn)
#        self.save_print_group.setLayout(save_print_layout)

        self.mass_info_grid = self._create_mass_metadata_grid()
        mass_info_layout.addWidget(self.mass_info_grid)

        self.mass_info_group.setLayout(mass_info_layout)

        mass_layout.addWidget(self.mass_canvas)
        mass_layout.addWidget(self.reference_line)
        mass_layout.addWidget(self.mass_info_group)
 #       mass_layout.addWidget(self.save_print_group)
        groupbox.setLayout(mass_layout)
        
        return groupbox, mass_layout
    
    # 2.1.1 Connect species all button click event
    def species_all_btn_click_event(self):
        if self.species_all.isChecked():
            self.species_btn1.setChecked(True)
            self.species_btn2.setChecked(True)
            self.species_btn3.setChecked(True)
            self.species_btn4.setChecked(True)
            self.species_others.setChecked(True)
            
            self.species_btn1.setEnabled(False)
            self.species_btn2.setEnabled(False)
            self.species_btn3.setEnabled(False)
            self.species_btn4.setEnabled(False)
            self.species_others.setEnabled(False)
            
        else:
            self.species_btn1.setChecked(False)
            self.species_btn2.setChecked(False)
            self.species_btn3.setChecked(False)
            self.species_btn4.setChecked(False)
            self.species_others.setChecked(False)
            
            self.species_btn1.setEnabled(True)
            self.species_btn2.setEnabled(True)
            self.species_btn3.setEnabled(True)
            self.species_btn4.setEnabled(True)
            self.species_others.setEnabled(True)
            
    # 2.1.2 Connect endpoint all button click event
    def endpoint_all_btn_click_event(self):
        if self.ep_all.isChecked():
            self.ep_lc_btn.setChecked(True)
            self.ep_ec_btn.setChecked(True)
            self.ep_others.setChecked(True)
            
            self.ep_lc_btn.setEnabled(False)
            self.ep_ec_btn.setEnabled(False)
            self.ep_others.setEnabled(False)
            
        else:
            self.ep_lc_btn.setChecked(False)
            self.ep_ec_btn.setChecked(False)
            self.ep_others.setChecked(False)
            
            self.ep_lc_btn.setEnabled(True)
            self.ep_ec_btn.setEnabled(True)
            self.ep_others.setEnabled(True)
    
    # 2.1.3 Connect species all button click event
    def search_btn_click_event(self):
        ### related to search grid ###
        df = self.toxic_db
        searched_type = str(self.search_type_list.currentText())
        searched_input = self.search_line.text()
        
        if searched_type == 'CAS':
            try:
                searched_input = searched_input.replace(' ','')
                searched_result=list(map(lambda f: searched_input in f, df['CAS']))

                # if there are more than one results , print first "True" cid number 
                searched_result=np.array(searched_result)
                print(searched_result)
                if len(np.where(searched_result==True)[0])!= 1:
                    print("Searche results > 1")
                    #searched_cid = df.values[np.where(searched_result==True)[0][1]][0]
                    searched_cid = df.values[np.where(searched_result==True)[0][0]][0]
                else:
                    #searched_cid = df[list(map(lambda f: searched_input in f, df['CAS']))]['cid'].item()
                    searched_cid = df[searched_result]['cid'].item()
            except:
                QMessageBox.about(self, "No results found.", "We do not have any datas for \"{}\"".format(searched_input))
                return
        elif searched_type == 'IUPAC':
            try:
                searched_input = searched_input.strip()
                searched_result= df['IUPAC']==searched_input
                if len(np.where(searched_result==True)[0]) != 1:
                    print("Searche results > 1")
                    searched_cid = df.values[np.where(searched_result==True)[0][0]][0]
                else:
                    searched_cid = df[df['IUPAC']==searched_input]['cid'].item()
                #searched_cid = df[df['IUPAC']==searched_input]['cid'].item()
            except:
                QMessageBox.about(self, "No results found.", "We do not have any datas for \"{}\"".format(searched_input))
                return
        elif searched_type == 'SMILES':
            try:
                searched_input = searched_input.replace(' ','')
                searched_result= df['SMILES']==searched_input
                if len(np.where(searched_result==True)[0]) != 1:
                    print("Searche results > 1")
                    searched_cid = df.values[np.where(searched_result==True)[0][0]][0]
                else:
                    searched_cid = df[df['SMILES']==searched_input]['cid'].item()
                #searched_cid = df[df['SMILES']==searched_input]['cid'].item()
            except:
                QMessageBox.about(self, "No results found.", "We do not have any datas for \"{}\"".format(searched_input))
                return
        else:
            QMessageBox.about(self, "Error", "Please select search type (CAS, IUPAC, or SMILES)")
            return
        
        ### related to info grid ###
        searched_data = df[df['cid']==searched_cid]
        cas = searched_data['CAS'].item()
        iupac_name = searched_data['IUPAC'].item()
        smiles = searched_data['SMILES'].item()

        ##########################set poison text module start###################################
        DBid = 1
        name, all_poison_list = utils.load_poison_info(searched_cid,DBid)
                
        self.info_table.setItem(0, 0, QTableWidgetItem(name))
        self.info_table.setItem(1, 0, QTableWidgetItem(iupac_name))
        self.info_table.setItem(2, 0, QTableWidgetItem(', '.join(cas)))
        self.info_table.setItem(3, 0, QTableWidgetItem(smiles))
        self.info_table.resizeColumnsToContents()
        
        ### related to poison grid ###
        if not self.species_all.isChecked() \
        and not self.species_btn1.isChecked() \
        and not self.species_btn2.isChecked() \
        and not self.species_btn3.isChecked() \
        and not self.species_btn4.isChecked() \
        and not self.species_others.isChecked():
            self.species_all.setChecked(True)
            
        if not self.ep_all.isChecked() \
        and not self.ep_lc_btn.isChecked() \
        and not self.ep_ec_btn.isChecked() \
        and not self.ep_others.isChecked():
            self.ep_all.setChecked(True)
        
        filtered_poison_list = []
        
        if self.species_all.isChecked() and self.ep_all.isChecked():
            filtered_poison_list = all_poison_list
        elif self.species_all.isChecked() and not self.ep_all.isChecked():
            if self.ep_lc_btn.isChecked():
                filtered_poison_list += [p for p in all_poison_list if 'LC50' in p]
            if self.ep_ec_btn.isChecked():
                filtered_poison_list += [p for p in all_poison_list if 'EC50' in p]
            if self.ep_others.isChecked():
                filtered_poison_list += [p for p in all_poison_list if not 'LC50' in p and not 'EC50' in p]
        elif not self.species_all.isChecked() and self.ep_all.isChecked():
            if self.species_btn1.isChecked():
                filtered_poison_list += [p for p in all_poison_list if 'zebra fish' in p.lower() or \
                                                                       'zebrafish' in p.lower() or \
                                                                       'danio rerio' in p.lower()]
            if self.species_btn2.isChecked():
                filtered_poison_list += [p for p in all_poison_list if 'fathead minnow' in p.lower() or \
                                                                       'pimephales promelas' in p.lower()]
            if self.species_btn3.isChecked():
                filtered_poison_list += [p for p in all_poison_list if 'medaka' in p.lower() or \
                                                                       'oryzias latipes' in p.lower()]
            if self.species_btn4.isChecked():
                filtered_poison_list += [p for p in all_poison_list if 'daphnia' in p.lower()]
            if self.species_others.isChecked():
                filtered_poison_list += [p for p in all_poison_list if 'zebra fish' not in p.lower() and \
                                                                       'zebrafish' not in p.lower() and \
                                                                       'danio rerio' not in p.lower() and \
                                                                       'fathead minnow' not in p.lower() and \
                                                                       'pimephales promelas' not in p.lower() and \
                                                                       'medaka' not in p.lower() and \
                                                                       'oryzias latipes' not in p.lower() and \
                                                                       'daphnia' not in p.lower()]
        else:
            ep_filtered_poison_list = []
            if self.ep_lc_btn.isChecked():
                ep_filtered_poison_list += [p for p in all_poison_list if 'LC50' in p]
            if self.ep_ec_btn.isChecked():
                ep_filtered_poison_list += [p for p in all_poison_list if 'EC50' in p]
            if self.ep_others.isChecked():
                ep_filtered_poison_list += [p for p in all_poison_list if not 'LC50' in p and not 'EC50' in p]
                
            if self.species_btn1.isChecked():
                filtered_poison_list += [p for p in ep_filtered_poison_list if 'zebra fish' in p.lower() or \
                                                                               'zebrafish' in p.lower() or \
                                                                               'danio rerio' in p.lower()]
            if self.species_btn2.isChecked():
                filtered_poison_list += [p for p in ep_filtered_poison_list if 'fathead minnow' in p.lower() or \
                                                                               'pimephales promelas' in p.lower()]
            if self.species_btn3.isChecked():
                filtered_poison_list += [p for p in ep_filtered_poison_list if 'medaka' in p.lower() or \
                                                                               'oryzias latipes' in p.lower()]
            if self.species_btn4.isChecked():
                filtered_poison_list += [p for p in ep_filtered_poison_list if 'daphnia' in p.lower()]
            if self.species_others.isChecked():
                filtered_poison_list += [p for p in ep_filtered_poison_list if 'zebra fish' not in p.lower() and \
                                                                               'zebrafish' not in p.lower() and \
                                                                               'danio rerio' not in p.lower() and \
                                                                               'fathead minnow' not in p.lower() and \
                                                                               'pimephales promelas' not in p.lower() and \
                                                                               'medaka' not in p.lower() and \
                                                                               'oryzias latipes' not in p.lower() and \
                                                                               'daphnia' not in p.lower()]
        
        filtered_poison_list = ['&nbsp; &nbsp; &nbsp; &nbsp;     ▶︎  '+ f for f in filtered_poison_list]
        poison_text = '<p style="font-size: 15px"><b>Ecotoxicity data form pubchem</b></p>' + '<br>' + '<br><br>'.join(filtered_poison_list)

        ##########################set poison text module end###################################

        ##########################set poison text module start###################################
        DBid = 2
        all_poison_list = utils.load_poison_info(searched_cid, DBid)

        self.info_table.setItem(0, 0, QTableWidgetItem(name))
        self.info_table.setItem(1, 0, QTableWidgetItem(iupac_name))
        self.info_table.setItem(2, 0, QTableWidgetItem(', '.join(cas)))
        self.info_table.setItem(3, 0, QTableWidgetItem(smiles))
        self.info_table.resizeColumnsToContents()

        ### related to poison grid ###
        if not self.species_all.isChecked() \
                and not self.species_btn1.isChecked() \
                and not self.species_btn2.isChecked() \
                and not self.species_btn3.isChecked() \
                and not self.species_btn4.isChecked() \
                and not self.species_others.isChecked():
            self.species_all.setChecked(True)

        if not self.ep_all.isChecked() \
                and not self.ep_lc_btn.isChecked() \
                and not self.ep_ec_btn.isChecked() \
                and not self.ep_others.isChecked():
            self.ep_all.setChecked(True)

        filtered_poison_list = []

        if self.species_all.isChecked() and self.ep_all.isChecked():
            filtered_poison_list = all_poison_list
        elif self.species_all.isChecked() and not self.ep_all.isChecked():
            if self.ep_lc_btn.isChecked():
                filtered_poison_list += [p for p in all_poison_list if 'LC50' in p]
            if self.ep_ec_btn.isChecked():
                filtered_poison_list += [p for p in all_poison_list if 'EC50' in p]
            if self.ep_others.isChecked():
                filtered_poison_list += [p for p in all_poison_list if not 'LC50' in p and not 'EC50' in p]
        elif not self.species_all.isChecked() and self.ep_all.isChecked():
            if self.species_btn1.isChecked():
                filtered_poison_list += [p for p in all_poison_list if 'zebra fish' in p.lower() or \
                                         'zebrafish' in p.lower() or \
                                         'danio rerio' in p.lower()]
            if self.species_btn2.isChecked():
                filtered_poison_list += [p for p in all_poison_list if 'fathead minnow' in p.lower() or \
                                         'pimephales promelas' in p.lower()]
            if self.species_btn3.isChecked():
                filtered_poison_list += [p for p in all_poison_list if 'medaka' in p.lower() or \
                                         'oryzias latipes' in p.lower()]
            if self.species_btn4.isChecked():
                filtered_poison_list += [p for p in all_poison_list if 'daphnia' in p.lower()]
            if self.species_others.isChecked():
                filtered_poison_list += [p for p in all_poison_list if 'zebra fish' not in p.lower() and \
                                         'zebrafish' not in p.lower() and \
                                         'danio rerio' not in p.lower() and \
                                         'fathead minnow' not in p.lower() and \
                                         'pimephales promelas' not in p.lower() and \
                                         'medaka' not in p.lower() and \
                                         'oryzias latipes' not in p.lower() and \
                                         'daphnia' not in p.lower()]
        else:
            ep_filtered_poison_list = []
            if self.ep_lc_btn.isChecked():
                ep_filtered_poison_list += [p for p in all_poison_list if 'LC50' in p]
            if self.ep_ec_btn.isChecked():
                ep_filtered_poison_list += [p for p in all_poison_list if 'EC50' in p]
            if self.ep_others.isChecked():
                ep_filtered_poison_list += [p for p in all_poison_list if not 'LC50' in p and not 'EC50' in p]

            if self.species_btn1.isChecked():
                filtered_poison_list += [p for p in ep_filtered_poison_list if 'zebra fish' in p.lower() or \
                                         'zebrafish' in p.lower() or \
                                         'danio rerio' in p.lower()]
            if self.species_btn2.isChecked():
                filtered_poison_list += [p for p in ep_filtered_poison_list if 'fathead minnow' in p.lower() or \
                                         'pimephales promelas' in p.lower()]
            if self.species_btn3.isChecked():
                filtered_poison_list += [p for p in ep_filtered_poison_list if 'medaka' in p.lower() or \
                                         'oryzias latipes' in p.lower()]
            if self.species_btn4.isChecked():
                filtered_poison_list += [p for p in ep_filtered_poison_list if 'daphnia' in p.lower()]
            if self.species_others.isChecked():
                filtered_poison_list += [p for p in ep_filtered_poison_list if 'zebra fish' not in p.lower() and \
                                         'zebrafish' not in p.lower() and \
                                         'danio rerio' not in p.lower() and \
                                         'fathead minnow' not in p.lower() and \
                                         'pimephales promelas' not in p.lower() and \
                                         'medaka' not in p.lower() and \
                                         'oryzias latipes' not in p.lower() and \
                                         'daphnia' not in p.lower()]

        filtered_poison_list = ['&nbsp; &nbsp; &nbsp; &nbsp;     ▶︎  '+ f for f in filtered_poison_list]
        poison_text = poison_text+ '<br><br>'+ '<p style="font-size: 15px"><b>Ecotoxicity data of 생활화학제품 from various DBs</b></p>' + '<br>' + '<br><br>'.join(filtered_poison_list)

        ##########################set poison text module end###################################
        self.poison_text.setText(poison_text)
        
        ### related to mass grid ###
        try:
            searched_msms_data = self.msms_db[smiles][0]['spectrum']
            self.mz_array = [float(d.split(':')[0]) for d in searched_msms_data.split(' ')]
            self.intensity_array = [float(d.split(':')[1]) for d in searched_msms_data.split(' ')]
            
            self.mass_fig.clear()
            ax = self.mass_fig.add_subplot(111)
            ax = utils.plot_mass(ax, self.mz_array, self.intensity_array)
            self.mass_canvas.draw()
            
            reference = self.msms_db[smiles][0]['library']['link']
            self.reference_line.setText(reference)

            # (Added) Set Item and Label of msinfo_table
            idx_ms = 0
            self.msinfo_table.setRowCount(len(self.msms_db[smiles][0]['metaData']))

            for ms_dict in self.msms_db[smiles][0]['metaData']:
                self.header_list.append(ms_dict['name'])
                self.msinfo_table.setItem(idx_ms, 0, QTableWidgetItem(str(ms_dict['value'])))
                idx_ms += 1
            self.msinfo_table.setVerticalHeaderLabels(self.header_list)

            self.mass_canvas.draw()
            self.mass_layout.addWidget(self.mass_canvas)
            self.mass_layout.addWidget(self.reference_line)
            self.mass_layout.addWidget(self.mass_info_group)
            self.mass_grid.setLayout(self.mass_layout)
            self.mass_canvas.show()

        except:
            self.mass_fig.clear()
            ax = self.mass_fig.add_subplot(111)
            ax.set_yticks([0, 20, 40, 60, 80, 100])
            ax.set_xlabel('m/z')
            ax.set_ylabel('Intensity')
            plt.tight_layout()
            self.mass_canvas.draw()

            # (Added) Clear Table
            self.msinfo_table.clear()
            self.msinfo_table.setRowCount(4)
            self.msinfo_table.setVerticalHeaderLabels(["              ", " ", " ", " "])

            self.mass_canvas = FigureCanvas(self.mass_fig)
            self.reference_line.setText('')

            self.mass_canvas.draw()
            self.mass_layout.addWidget(self.mass_canvas)
            self.mass_layout.addWidget(self.reference_line)
            self.mass_layout.addWidget(self.save_print_group)
            
            self.reference_line.setText('')            
            QMessageBox.about(self, "Error", "There is no database corresponding to the {} in the mass spectrum DB".format(smiles))
            return
    
    # 2.4.1 Connect save/print button click event
    def file_btn_click_event(self, clicked_btn):
        name = self.info_table.item(0, 0)
        if name is None:
            QMessageBox.about(self, "Error", "There is no searching history")
            return
        
        # search information
        searched_type = str(self.search_type_list.currentText())
        searched_input = self.search_line.text()
        
        selected_species = []
        if self.species_all.isChecked():
            selected_species.append('all')
        else:
            if self.species_btn1.isChecked():
                selected_species.append('zebra fish')
            if self.species_btn2.isChecked():
                selected_species.append('fathead minnow')
            if self.species_btn3.isChecked():
                selected_species.append('medaka')
            if self.species_btn4.isChecked():
                selected_species.append('daphnia')
            if self.species_others.isChecked():
                selected_species.append('others')
        selected_species = ', '.join(selected_species)
        
        selected_ep = []
        if self.ep_all.isChecked():
            selected_ep.append('all')
        else:
            if self.ep_lc_btn.isChecked():
                selected_ep.append('LC50')
            if self.ep_ec_btn.isChecked():
                selected_ep.append('EC50')
            if self.ep_others.isChecked():
                selected_ep.append('others')
        selected_ep = ', '.join(selected_ep)
        
        # chemical information
        name = self.info_table.item(0, 0).text()
        iupac_name = self.info_table.item(1, 0).text()
        cas = self.info_table.item(2, 0).text()
        smiles = self.info_table.item(3, 0).text()
        
        # toxic information
        poison_text = self.poison_text.toPlainText()
        
        # mass spectrum
        try:
            self.msms_db[smiles]
            self.mass_fig.savefig('mass_fig.png',
                                  dpi=100,
                                  bbox_inches='tight')
            reference = self.reference_line.text()
        except:
            pass
        
        # Make the entire text edit for save/print
        entire_text = QTextEdit('')
        entire_text.append('\n' + '='*10 + 'Search Information' + '='*10 + '\n')
        entire_text.append('Searched type: {}'.format(searched_type))
        entire_text.append('Searched input: {}'.format(searched_input))
        entire_text.append('Selected species: {}'.format(selected_species))
        entire_text.append('Selected end point: {}'.format(selected_ep))
        entire_text.append('\n' + '='*10 + 'Chemical Information' + '='*10 + '\n')
        entire_text.append('Name: {}'.format(name))
        entire_text.append('IUPAC name: {}'.format(iupac_name))
        entire_text.append('CAS number: {}'.format(cas))
        entire_text.append('SMILES: {}'.format(smiles))
        entire_text.append('\n' + '='*10 + 'Toxic Information' + '='*10 + '\n')
        entire_text.append(poison_text)
        
        try:
            self.msms_db[smiles]
            entire_text.append('\n' + '='*10 + 'Mass Spectrum' + '='*10 + '\n')
            entire_text.append('reference: {}'.format(reference) + '\n')
            
            cursor = entire_text.textCursor()
            entire_text.moveCursor(QTextCursor.End)
            cursor.insertImage('mass_fig.png')
        except:
            pass
        
        if clicked_btn == 'save':
            fn, _ = QFileDialog.getSaveFileName(self, 'Export PDF', None, 'PDF files (.pdf);;All Files()')
            if fn != '':
                if QFileInfo(fn).suffix() == "" : fn += '.pdf'
                printer = QPrinter(QPrinter.HighResolution)
                #printer = QPrinter(QPrinter.ScreenResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(fn)
                entire_text.document().print_(printer)
            try:
                os.remove('mass_fig.png')
            except:
                pass
                
        elif clicked_btn == 'print':
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                entire_text.print_(printer)
            try:
                os.remove('mass_fig.png')
            except:
                pass

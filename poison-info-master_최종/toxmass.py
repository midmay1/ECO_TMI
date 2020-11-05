import mainwin
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = mainwin.MyMain()
   sys.exit(app.exec_())

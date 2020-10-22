import mainwin
#import run
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = mainwin.MyMain()
#  ex = run.MyApp()
   sys.exit(app.exec_())
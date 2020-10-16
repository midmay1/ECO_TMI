import run
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
ex = run.MyApp()
sys.exit(app.exec_())

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

def main():
  app = QApplication([])
  window = QWidget()
  window.setGeometry(660, 300, 700, 400)
  
  label = QLabel(window)
  label.setText("Hello")
  label.setFont(QFont("Arial", 16))
  label.move(50, 100)
  
  window.show()
  app.exec()
  
if __name__ == "__main__":
  main()
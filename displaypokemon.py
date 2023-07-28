import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton,QHBoxLayout
from PySide6.QtGui import QPixmap

import os

class Displaypokemon(QWidget):
    def __init__(self, image_paths):
        super().__init__()
        self.setStyleSheet("""
            QPushButton {
                background-color: dark-grey;
                color: white;
                border: 1px solid #BA263E;
                font: bold 16px;
                text-align: center;
                border-radius: 10px;
            }
            QMainWindow {
                background-color: black;
            }
            QLabel {
                font-size: 32px;
            }
            QPushButton:hover {
                background-color: #BA263E;
                color: dark-grey;
            }
        """)
        self.setWindowTitle("Pokemon")
        self.image_paths = image_paths
        self.current_image_index = 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

     
        self.labelpic = QLabel(self)
        layout.addWidget(self.labelpic)

      
        self.labelname = QLabel(self)
        layout.addWidget(self.labelname)

      
        nav_layout = QHBoxLayout()
        prev_button = QPushButton("Previous", self)
        prev_button.clicked.connect(self.show_previous_image)
        nav_layout.addWidget(prev_button)

        next_button = QPushButton("Next", self)
        next_button.clicked.connect(self.show_next_image)
        nav_layout.addWidget(next_button)

        layout.addLayout(nav_layout)
        self.setLayout(layout)

    
        self.update_image_label()

    def show_previous_image(self):
        self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
        self.update_image_label()

    def show_next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        self.update_image_label()

    def update_image_label(self):
        pixmap = QPixmap(self.image_paths[self.current_image_index])
        self.labelpic.setPixmap(pixmap)

       
        filename = os.path.basename(self.image_paths[self.current_image_index])
        pokemon_name = os.path.splitext(filename)[0]
        self.labelname.setText(pokemon_name)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    folder_name = "IMAGE"
    image_paths = []
    window = Displaypokemon(image_paths)
    window.show()
    sys.exit(app.exec())

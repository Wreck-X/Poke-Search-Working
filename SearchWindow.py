import requests
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton,QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

from displaypokemon import Displaypokemon


class SearchWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
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
        self.w = None
        self.image_paths=[]


        
        self.setFixedSize(850, 500)
 
        labelmov = QLabel(self)
        labelmov.setPixmap(QPixmap("assets/landing.jpg"))
        labelmov.setScaledContents(True)
        labelmov.setGeometry(0, 0, 850, 478)
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        
        self.textbox.setGeometry(50, 50, 280, 40)
      
        
        label1 = QLabel("Enter the name", self)
        label1.setStyleSheet("color: white; font-size: 16px; font-weight: medium;")
        label1.setGeometry(50, 5, 600, 70)

        enter_button = QPushButton("Search", self)
        enter_button.setGeometry(50, 300, 160, 43)
        enter_button.clicked.connect(self.fetch_and_display)
        
        capture_button = QPushButton("Capture", self)
        capture_button.setGeometry(50, 350, 160, 43)
        capture_button.clicked.connect(self.download_image)
        display_button = QPushButton("Display", self)
        display_button.setGeometry(50, 400, 160, 43)
        display_button.clicked.connect(self.open_display_window)
       


        self.pokemon_artwork_label = QLabel(self)
        self.pokemon_artwork_label.setGeometry(400, 20, 200, 200)
        self.pokemon_artwork_label.setAlignment(Qt.AlignCenter)   

        self.info_label = QLabel(self)
        self.info_label.setGeometry(400, 240, 300, 100)  
        self.info_label.setStyleSheet("color: white; font-size: 18px; font-weight: medium;")

        self.stats_label = QLabel(self)
        self.stats_label.setGeometry(400, 310, 200, 200) 
        self.stats_label.setStyleSheet("color: white; font-size: 18px; font-weight: medium;")

    def fetch_and_display(self):
        pokemon_name = self.textbox.text()
        if not pokemon_name:
            return

        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")

        if response.status_code == 200:
            name = response.json()["name"]
            abilities = [i["ability"]["name"] for i in response.json()["abilities"]]
            artwork = response.json()["sprites"]["other"]["official-artwork"]["front_default"]
            types = [i["type"]["name"] for i in response.json()["types"]]
            stats = [(i["stat"]["name"], i["base_stat"]) for i in response.json()["stats"]]
            print("name- ", name)
            print("abilities- ", abilities)
            print("artwork- ", artwork)
            print("types- ", types)
            print("stats", stats)
            self.artwork = artwork
            self.pokemon_name=name
            print(self.artwork)
            self.display_artwork(artwork)
            self.display_info(name, abilities, types)
            self.display_stats(stats)
            self.remove_background_image()



        else:
            print("Unable to fetch data for the Pokemon:", pokemon_name)
    
    def remove_background_image(self):
        labelmov = self.findChild(QLabel)
        if labelmov:
            labelmov.hide()

    def display_artwork(self, url):
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(url).content)
        pixmap = pixmap.scaled(200, 200)
        self.pokemon_artwork_label.setPixmap(pixmap)
    
    def display_info(self, name, abilities, types):
        info_text = f"Name: {name}\nAbilities: {', '.join(abilities)}\nTypes: {', '.join(types)}"
        self.info_label.setText(info_text)
    def display_stats(self, stats):
        stats_text = "Stats:\n"
        for stat_name, stat_value in stats:
            stats_text += f"{stat_name}: {stat_value}\n"
        self.stats_label.setText(stats_text)
    def download_image(self):
        if self.artwork:
            folder_name = "IMAGE"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            response = requests.get(self.artwork)
            if response.status_code == 200:
                with open(f"{folder_name}/{self.pokemon_name}.JPG", 'wb') as f:
                    f.write(response.content)
                    QMessageBox.information(self, "Image Downloaded", f"Image successfully downloaded to")
            else:
                    QMessageBox.warning(self, "No Image", "No artwork to download. Search for a Pokemon first.")
            
    def get_image_paths(self,folder_name):
        self.image_paths = []
        folder_path = os.path.join(os.getcwd(), folder_name)

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            valid_extensions = (".jpg", ".png", ".bmp")
            for filename in os.listdir(folder_path):
                _, extension = os.path.splitext(filename)
                if extension.lower() in valid_extensions:
                    self.image_path = os.path.join(folder_name, filename)
                    self.image_paths.append(self.image_path)

        return self.image_paths
    def open_display_window(self, checked):
        if self.w is None:
            folder_name = "IMAGE"
            self.image_paths = self.get_image_paths(folder_name)
            self.w = Displaypokemon(self.image_paths)
        self.w.show()
                
    


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SearchWindow()
    window.show()
    sys.exit(app.exec())

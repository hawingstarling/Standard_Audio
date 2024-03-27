from PyQt5.QtGui import QFont, QFontDatabase

class FontApple():
    def __init__(self, font_path) -> None:
        self.font_path = font_path
        self.id = QFontDatabase.addApplicationFont(font_path)
        if self.id < 0:
            print("Error")
        self.families = QFontDatabase.applicationFontFamilies(self.id)

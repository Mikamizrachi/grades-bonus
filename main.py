from PySide6.QtWidgets import QApplication, QWidget



class GradesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.students_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ""
        self.header = []

        self.setWindowTitle("Grades Bonus")
        




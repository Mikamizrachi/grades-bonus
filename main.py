from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, 



class GradesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ""
        self.header = []

        self.setWindowTitle("Grades Bonus")

        self.open_btn = QPushButton("Choose File")
        self.open_btn.clicked.connect(self.choose_file)


    def choose_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose grades file", "", "CSV Files (*.csv)")
        if not file_name:
            return
        else:
            self.selected_file = file_name 

        self.student_ids.clear()
        self.original_grades.clear()
        with open(self.selected_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            self.header = next(reader)
            for row in reader:
                self.student_ids.append(row[0])  
                self.original_grades.append(int(row[1]))
        self.corrected_grades = self.original_grades.copy()
        self.update_table()






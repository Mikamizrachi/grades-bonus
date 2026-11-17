from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QTableWidget, QSpinBox



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

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])

        self.bonus_spin = QSpinBox()
        self.bonus_spin.setRange(0, 100)
        self.bonus_spin.lineEdit().returnPressed.connect(self.apply_bonus)





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

    def apply_bonus(self):
        bonus = self.bonus_spin.value()
        for i in range(len(self.original_grades)):
            self.corrected_grades[i] = min(self.original_grades[i] + bonus, 100)
        self.update_table()





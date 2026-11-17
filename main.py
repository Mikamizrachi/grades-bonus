import sys, os, csv, subprocess, platform
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QTableWidget, QVBoxLayout,QSpinBox, QHBoxLayout, QLabel, QTableWidgetItem,QMessageBox
from About import About


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

        self.update_btn =QPushButton("Update File")
        self.update_btn.clicked.connect(self.update_file)

        self.about_btn = QPushButton("About")
        self.about_btn.clicked.connect(self.show_about)

        bonus_row = QHBoxLayout()
        bonus_row.addWidget(QLabel("Bonus:"))
        bonus_row.addWidget(self.bonus_spin)

        buttons_row = QHBoxLayout()
        buttons_row.addWidget(self.update_btn)
        buttons_row.addWidget(self.about_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(self.open_btn)
        layout.addWidget(self.table)
        layout.addLayout(bonus_row)
        layout.addLayout(buttons_row)







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


    def update_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please choose a file first")
            return
        with open(self.selected_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.header)
            for sid, grade in zip(self.student_ids, self.corrected_grades):
                writer.writerow([sid, grade])
        self.open_file(self.selected_file)


    def show_about(self):
        self.about = About()
        self.about.show()

    def update_table(self):
        self.table.clearContents()
        for i in range(len(self.student_ids)):
            self.table.setItem(i, 0, QTableWidgetItem(self.student_ids[i]))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.original_grades[i])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.corrected_grades[i])))

    def open_file(self, path):
        system = platform.system()
        if system == "Windows":
            os.startfile(path)
        elif system == "Darwin":
            subprocess.call(["open", path])
        else:
            subprocess.call(["xdg-open", path])



if __name__ == "__main__":
    app = QApplication(sys.argv)
    qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
    with open(qss_path, encoding="utf-8") as f:
        app.setStyleSheet(f.read())
    window = GradesWindow()
    window.resize(500, 600)
    window.show()
    sys.exit(app.exec())
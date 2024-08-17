import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic
import os

class TextFileEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)  # Load the .ui file directly
        
        # Define the path to the file
        self.file_path = 'manhwa.txt'
        
        # Ensure the file exists
        self.ensure_file_exists()
        
        # Connect buttons to functions
        self.actionButton.clicked.connect(self.perform_action)

        # Display the file content initially
        self.display_file_content()

    def ensure_file_exists(self):
        if not os.path.isfile(self.file_path):
            # Create the file if it does not exist
            open(self.file_path, 'w').close()

    def display_file_content(self):
        try:
            with open(self.file_path, 'r') as file:
                self.fileContent.setPlainText(file.read())
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"The file '{self.file_path}' was not found.")

    def perform_action(self):
        action = self.actionComboBox.currentText()

        if action == "Find":
            search_term = self.searchInput.text()
            self.search_file(search_term)
        elif action == "Add":
            lines_to_add = self.addInput.toPlainText().splitlines()
            self.add_lines(lines_to_add)
        elif action == "Edit":
            search_term = self.searchInput.text()
            new_content = self.editInput.text()
            self.edit_lines_with_term(search_term, new_content)

    def search_file(self, search_term):
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
            matching_lines = [line.strip() for line in lines if search_term.lower() in line.lower()]
            self.resultOutput.setPlainText('\n'.join(matching_lines) if matching_lines else "No matching lines found.")
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"The file '{self.file_path}' was not found.")

    def add_lines(self, lines_to_add):
        try:
            with open(self.file_path, 'a') as file:
                for line in lines_to_add:
                    file.write(line + '\n')
            self.display_file_content()
            QMessageBox.information(self, "Success", "Lines added successfully.")
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"The file '{self.file_path}' was not found.")

    def edit_lines_with_term(self, search_term, new_content):
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()

            updated = False
            for i in range(len(lines)):
                line = lines[i].strip()
                if search_term.lower() in line.lower():
                    # Split the line into parts based on 3 or more spaces
                    parts = line.split('   ', 1)
                    if len(parts) > 1:
                        # Update the last part only
                        lines[i] = parts[0] + '   ' + new_content + '\n'
                        updated = True

            if updated:
                with open(self.file_path, 'w') as file:
                    file.writelines(lines)
                self.display_file_content()
                QMessageBox.information(self, "Success", "Lines containing the search term have been updated.")
            else:
                QMessageBox.warning(self, "Error", "No lines containing the search term were found.")
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"The file '{self.file_path}' was not found.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TextFileEditor()
    window.show()
    sys.exit(app.exec_())

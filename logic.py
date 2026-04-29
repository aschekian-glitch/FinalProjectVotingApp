import csv

import os

from PyQt6.QtWidgets import *

from gui import *


class Logic(QMainWindow, Ui_MainWindow):
    """
    This houses the main logic for the voting system application.

    This Application takes user input, validates it, and submits the vote to a csv file.
    """

    def __init__(self) -> None:
        """
        This method initializes the GUI, connects the submit button to the GUI, and groups the voting buttons together.
        """
        super().__init__()
        self.setupUi(self)

        self.submit_button.clicked.connect(self.submit)

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.canidate1_button)
        self.button_group.addButton(self.canidate2_button)

    def submit(self) -> None:
        """
        This method handles the voting submission.

        Makes sure ID input is a valid number and each ID only votes once.

        Makes sure a canidate is selected.

        Saves vote to CSV file.
        """

        id = self.id_input.text().strip()
        vote = ''
        existing_ids = []

        if self.canidate1_button.isChecked():
            vote = 'Canidate 1'
        elif self.canidate2_button.isChecked():
            vote = 'Canidate 2'
        else:
            self.instruction_label.setText("Please select a canidate")
            self.instruction_label.move(240,60)
            self.instruction_label.setStyleSheet("color : red;")



        try:
            id = int(id)
        except ValueError:
            self.instruction_label.setText("Please enter a valid ID")
            self.instruction_label.move(240,60)
            self.instruction_label.setStyleSheet("color : red;")
            return

        ids_voted = set()

        if os.path.exists('vote_data.csv'):
            with open('vote_data.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    ids_voted.add(int(row[0]))

        if id in ids_voted:
            self.instruction_label.setText("ID has already cast a vote")
            self.instruction_label.move(240,60)
            self.instruction_label.setStyleSheet("color : red;")


        with open('vote_data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([id, vote])

        self.instruction_label.setText("Vote Submitted Succesfully!")
        self.id_input.clear()
        if self.button_group.checkedButton() != 0:
            self.button_group.setExclusive(False)
            self.button_group.checkedButton().setChecked(False)
            self.button_group.setExclusive(True)
        self.id_input.setFocus()
        self.instruction_label.setStyleSheet("color : green;")
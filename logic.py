import csv
from PyQt6.QtWidgets import *
from gui import *

class Logic(QMainWindow, Ui_Grade_Window):
    def __init__(self)->None:
        """
        Method that sets up grade window and creates grades.csv file
        """
        super().__init__()
        self.setupUi(self)
        self.validate_attempts()
        self.input_attempts.textChanged.connect(lambda: self.validate_input())
        self.input_score1.textChanged.connect(lambda: self.validate_input())
        self.input_score2.textChanged.connect(lambda: self.validate_input())
        self.input_score3.textChanged.connect(lambda: self.validate_input())
        self.input_score4.textChanged.connect(lambda: self.validate_input())
        self.input_student_name.textChanged.connect(lambda: self.validate_input())
        self.button_submit.clicked.connect(lambda: self.submit())
        with open('grades.csv', 'w', newline='') as csvfile: # overwrite or append
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Name', 'Score 1', 'Score 2', 'Score 3', 'Score 4', 'Average'])

    def validate_input(self)->None:
        """
        Method that makes sure all the inputs are valid, if they are the submit button turns green
        """
        self.label_error.setText('')
        self.validate_attempts()
        self.validate_scores()
        self.validate_name()
        if self.label_error.text() == '':
            self.button_submit.setStyleSheet("background-color: green; color: white;")
        else:
            self.button_submit.setStyleSheet("color: black;")

    def validate_attempts(self)->None:
        """
        Method that validates the attempts input
        """
        if self.input_attempts.text() == '':
            self.hide_scores()
            # should this be accepted as all zeros?
        elif self.input_attempts.text() == '1':
            self.show_scores(1)
        elif self.input_attempts.text() == '2':
            self.show_scores(2)
        elif self.input_attempts.text() == '3':
            self.show_scores(3)
        elif self.input_attempts.text() == '4':
            self.show_scores(4)
        else:
            self.label_error.setStyleSheet("color: red;")
            self.label_error.setText("Number of attempts should be an\ninteger between 1 and 4")
            self.hide_scores()

    def validate_scores(self)->None:
        """
        Method that validates the scores input
        """
        input_list = [self.input_score1.text(), self.input_score2.text(), self.input_score3.text(),self.input_score4.text()]
        try:
            for score in input_list:
                if score == '':
                    pass
                elif int(score) < 0 or int(score) > 100:
                    raise IndexError
        except ValueError:
            self.label_error.setStyleSheet("color: red;")
            self.label_error.setText(f'Strings not accepted\n\nScores should be an \ninteger between 0 and 100')
        except IndexError:
            self.label_error.setStyleSheet("color: red;")
            self.label_error.setText(f'Grade out of range\n\nScores should to be an \ninteger between 0 and 100')

    def validate_name(self)->None:
        """
        Method that makes sure the name input is not empty
        """
        if self.input_student_name.text() == '':
            self.label_error.setStyleSheet("color: red;")
            self.label_error.setText('Student Name cannot be empty')

    def show_scores(self, attempts)->None:
        """
        Method that shows the scores input labels and boxes
        :param attempts: indicates how many of the score labels/boxes should be shown
        """
        if attempts >= 1:
            self.label_score1.show()
            self.input_score1.show()
        if attempts >= 2:
            self.label_score2.show()
            self.input_score2.show()
        if attempts >= 3:
            self.label_score3.show()
            self.input_score3.show()
        if attempts >= 4:
            self.label_score4.show()
            self.input_score4.show()

    def hide_scores(self)->None:
        """
        Method that clears and hides the scores input labels and boxes
        """
        self.label_score1.hide()
        self.input_score1.hide()
        self.label_score2.hide()
        self.input_score2.hide()
        self.label_score3.hide()
        self.input_score3.hide()
        self.label_score4.hide()
        self.input_score4.hide()
        self.input_score1.setText('')
        self.input_score2.setText('')
        self.input_score3.setText('')
        self.input_score4.setText('')

    def submit(self)->None:
        """
        Method that writes the grades to the csv file and resets the user interface
        """
        self.validate_input()
        if self.label_error.text() == '':
            input_list = [self.input_score1.text(), self.input_score2.text(), self.input_score3.text(),
                          self.input_score4.text()]
            for num in range(4):
                if input_list[num] == '':
                    input_list[num] = 0
                else:
                    input_list[num] = int(input_list[num])
            with open('grades.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([self.input_student_name.text(), input_list[0], input_list[1], input_list[2], input_list[3], sum(input_list)/len(input_list)])
            self.hide_scores()
            self.input_student_name.setText('')
            self.input_attempts.setText('')
            self.label_error.setStyleSheet("color: green;")
            self.label_error.setText('Submitted successfully!')
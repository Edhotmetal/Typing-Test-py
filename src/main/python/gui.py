# import widgets: buttons, labels, etc
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QFont

import sys

class Test_UI(QWidget):

    test_in_progress = False
    test_complete = False # Record whether the test was completed or interrupted

    input_field = None
    sample_text = None
    toggle_button = None

    def __init__(self):
        super().__init__()

        self.init_UI()

    def init_UI(self):
        print("Initializing UI")
        palette = QPalette()
        #TODO: Set palette colors here!

        #TODO: set stylesheets
        # app.setStyleSheet("QPushButton { margin: 10ex; }")

        # Create a vertical layout with 2 rows
        # the top will contain the test and bottom will contain the buttons
        main_layout = QVBoxLayout()

        # Create a grid layout for the test
        test_layout = QGridLayout()

        # Create a title on the top left of the grid layout
        title_font = QFont("Source Code Pro", 24, 1, True)
        title_label = QLabel("Typing Test")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignTop)
        title_label.setFrameStyle(QFrame.Box)
        title_label.setFrameShadow(QFrame.Shadow.Raised)
        title_label.setLineWidth(4)
        test_layout.addWidget(title_label)

        # Display the sample text at the top
        # TODO: Make a nice font
        global sample_text
        sample_text = QLabel("Sample Text Goes Here!😎")
        sample_text.setWordWrap(True)
        test_layout.addWidget(sample_text, 0, 1)

        # Display the test status at the top right
        # TODO nice font for status
        status_label = QLabel("Test Status Goes Here!😀")
        status_label.setWordWrap(True)
        test_layout.addWidget(status_label, 0, 2)

        # Create an input area for the user to type
        global input_field
        input_field = QTextEdit()
        input_field.setPlaceholderText("Start typing here!")
        input_field.setAcceptRichText(False)
        input_field.setAutoFormatting(QTextEdit.AutoNone)
        input_field.textChanged.connect(self.input_text_changed)
        input_field.cursorPositionChanged.connect(self.input_cursor_position_changed)
        test_layout.addWidget(input_field, 1, 1)

        # Create a layout for the buttons on the bottom
        button_layout = QHBoxLayout()

        # Create test toggle button
        # This button displays Restart or Finish depending on the test status
        global toggle_button
        toggle_button = QPushButton("Toggle")
        # connect the toggle button to its method
        toggle_button.clicked.connect(self.toggle_button_clicked)
        # Add the toggle button to its layout
        button_layout.addWidget(toggle_button)

        # Create the stats button
        # this button creates a new window with the user's overall stats
        stats_button = QPushButton("&Stats")
        # connect the stats button to its method
        stats_button.clicked.connect(self.stats_button_clicked)
        # Add the stats button to its layout
        button_layout.addWidget(stats_button)

        # Create the help button
        # Creates a new window displaying useful information!
        help_button = QPushButton("&Help")
        # connect the help button to its method
        help_button.clicked.connect(self.help_button_clicked)
        # add the help button to its layout
        button_layout.addWidget(help_button)
        
        # display the window
        self.setGeometry(500,500,700,250)
        self.setWindowTitle("Typing Test")
        main_layout.addLayout(test_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        self.show()
        print("Finished initializing UI")

    def toggle_button_clicked(self):
        # Called when the user activates the toggle button
        # When the test is in progress, end the test
        # If the test is not in progress, restart the test
        print("You clicked the toggle button!!!!")
        global test_in_progress

        if(test_in_progress):
            self.end_test()
        else:
            self.restart_test()

    def stats_button_clicked(self):
        #TODO
        # Called when the user activates the stats button
        # It opens a new window displaying the user's overall statistics
        print("You clicked the stats button!!!")

    def help_button_clicked(self):
        #TODO
        # Called when the user activates the help button
        # Opens a new window displaying helpful information
        print("You clicked the help button!!!!")

    def input_text_changed(self):
        # TODO
        # Called when the user changes the text in the input field
        # I need this to check if the user has completed the test
        print("You entered a character!")
        global test_in_progress
        # TODO SCOPE SHENANIGANS
        print("The test is in progress: {0}".format(test_in_progress))
        if(not test_in_progress):
            self.begin_test()
        else:
            global input_field
            global sample_text
            print("input: {0}\nsample: {0}".format(len(input_field.toPlainText()), len(sample_text.text())))
            if(len(input_field.toPlainText()) >= len(sample_text.text())):
                global test_complete
                test_complete = True
                self.end_test()

    def input_cursor_position_changed(self):
        #TODO
        # Called when the cursor position in the input field changes
        # Hopefully I can prevent cheating??
        print("Are you trying to cheat??")

    def begin_test(self):
        # TODO
        # Called when the user begins typing
        # Starts the timer
        print("Beginning test!")
        global test_in_progress
        test_in_progress = True

    def end_test(self):
        # Called when the user activates the toggle button when the test is running
        # Stops the test
        #TODO: do something with the timer
        print("Ending the test")
        global test_in_progress
        test_in_progress = False
        self.toggle_button.setText("Restart") 

    def restart_test(self):
        # Called when the user activates the toggle button when the test is not running
        # Refreshes the sample text and resets the statistics
        #TODO: Actually restart the test
        print("Restarting the test")
        global test_complete
        test_complete = False
        

# if this file has been executed
# This is only for testing
if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = Test_UI()
    sys.exit(app.exec_())

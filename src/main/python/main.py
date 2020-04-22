# import widgets: buttons, labels, etc
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtGui import QPalette, QFont

import sys, random

class Test_UI(QWidget):

    test_in_progress = False
    test_complete = False # Record whether the test was completed or interrupted
    wpm = 0
    num_words = 0 # The number of words the user typed
    accuracy = 0

    input_field = None
    sample_text = None
    toggle_button = None

    wpm_label = None
    words_typed = None
    accuracy_label = None

    timer = None
    start_time = None
    timer_display = None

    status_label = None
    def __init__(self):
        super().__init__()

        self.init_UI()
        self.get_new_sample()

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
        # Prevent the center column from expanding
        test_layout.setColumnStretch(1, 0)

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
        global status_label
        status_label = QLabel("Test Status Goes Here!😀")
        status_label.setWordWrap(True)
        test_layout.addWidget(status_label, 0, 2)

        # Create a timer display on the left
        # Create a label for the timer
        # TODO font!
        timer_label = QLabel("TIMER")
        timer_label.setAlignment(Qt.AlignCenter)

        # Create a display for the timer
        # TODO font!
        global timer_display
        timer_display = QLabel("0.0")
        timer_display.setAlignment(Qt.AlignCenter)
        timer_font = QFont("Source Code Pro", 32, 0, True)
        timer_display.setFont(timer_font)

        # Layout for the two timer labels
        timer_layout = QVBoxLayout()
        timer_layout.addWidget(timer_label)
        timer_layout.addWidget(timer_display)
        test_layout.addLayout(timer_layout, 1, 0)

        # Create an input area for the user to type
        global input_field
        input_field = QTextEdit()
        input_field.setPlaceholderText("Start typing here!")
        input_field.setAcceptRichText(False)
        input_field.setAutoFormatting(QTextEdit.AutoNone)
        input_field.setTextInteractionFlags(Qt.TextEditable)
        input_field.textChanged.connect(self.input_text_changed)
        test_layout.addWidget(input_field, 1, 1)

        # Create a layout for the users's statistics on the right
        stats_layout = QGridLayout()
        global wpm_label, words_typed, accuracy_label
        wpm_label = QLabel("WPM: 0")

        words_typed = QLabel("Words Typed: 0")

        accuracy_label = QLabel("Accuracy: N/A")

        stats_layout.addWidget(wpm_label)
        stats_layout.addWidget(words_typed, 0, 1)
        stats_layout.addWidget(accuracy_label, 1, 0)

        test_layout.addLayout(stats_layout, 1, 2)

        # Create a layout for the buttons on the bottom
        button_layout = QHBoxLayout()

        # Create test toggle button
        # This button displays Restart or Finish depending on the test status
        global toggle_button
        toggle_button = QPushButton("&Restart")
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
        self.setGeometry(500,500,700,300)
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

        if(self.test_in_progress):
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
        global input_field, words_typed, sample_text
        text = input_field.toPlainText()
        sample = sample_text.text()
        # Display how many words the user has typed compared to the sample text
        words_typed.setText("Words Typed: {0}/{1}".format(str(len(text.split())),
            str(len(sample.split()))))

        # Make sure the test starts only when the user starts typing
        # because this method is also called when restart_test() clears the input field
        if(not self.test_in_progress and len(text) != 0):
            self.begin_test()
        else:
            # Check if the user has typed enough words
            if(len(text.split()) == len(sample.split())):
                # check if the last word is complete
                if(len(text.split()[-1]) >= len(sample.split()[-1])):
                    self.test_complete = True
                    self.end_test()
            # If the user has typed too many words, end the test
            elif(len(text.split()) > len(sample.split())):
                self.test_complete = True
                self.end_test()

    def begin_test(self):
        # Called when the user begins typing
        # Starts the timer
        # TODO Make a progress bar in the status pane

        print("Beginning test!")
        self.test_in_progress = True
        global toggle_button
        toggle_button.setText("&End Test")

        # Start the timer
        global timer, start_time
        start_time = QTime.currentTime()
        timer = QTimer()
        timer.timeout.connect(self.update_timer)
        timer.start(10)
        status_label.setText("Test in progress!🤨")

    def end_test(self):
        # Called when the user activates the toggle button when the test is running
        # Or when the user completes the test
        # Stops the test

        print("Ending the test")
        self.test_in_progress = False
        global toggle_button
        toggle_button.setText("&Restart") 
        global input_field
        input_field.setTextInteractionFlags(Qt.NoTextInteraction)
        global timer
        timer.stop()
        self.calc_stats()
        # TODO Change the test status message according to the user's performance
        global status_label
        if(len(input_field.toPlainText().split()) > len(sample_text.text().split())):
            status_label.setText("Too many words! Try again!")
        elif(self.wpm > 88.0):
            status_label.setText("You went over 88 WPM!!!")
        elif(self.accuracy == 100):
            status_label.setText("PERFECT!🎉")
        else:
            status_label.setText("Test Complete!")

    def restart_test(self):
        # Called when the user activates the toggle button when the test is not running
        # Refreshes the sample text and resets the statistics
        #TODO: Serve a new sample to the user
        print("Restarting the test")
        self.test_complete = False
        global input_field, timer_display
        input_field.clear()
        input_field.setTextInteractionFlags(Qt.TextEditable)
        timer_display.setText("0")
        status_label.setText("Get ready for the test!")
        self.get_new_sample()

    def update_timer(self):
        # Called each time the timer fires
        # updates the timer display
        
        # Calculate difference between now and the start of the test
        # and update the timer display
        now = QTime.currentTime()
        msecs_elapsed = start_time.msecsTo(now)
        global timer_display
        timer_display.setText("{:.1f}".format(msecs_elapsed/1000))

    def calc_stats(self):
        # Calculate the user's statistics at the end of the test
        # Also calculate overall statistics for display in the stats window
        #TODO
        # Calculate accuracy
        # Calculate overall statistics
        print("Calculating statistics")

        # Calculate wpm
        # Get the # of words typed by the user
        global input_field
        self.num_words = len(input_field.toPlainText().split())
        global timer_display
        time_elapsed = float(timer_display.text())
        global wpm_label
        self.wpm = self.num_words/(time_elapsed / 60.0)
        wpm_label.setText("WPM: {:.2f}".format(self.wpm))

    def get_new_sample(self):
        # Get a new sample text for the user when the test is restarted
        # This method gets a random line of text from samples.txt
        sample_file = open("./samples.txt", 'r')
        samples = sample_file.readlines()
        lines=[]
        for line in samples:
            lines.append(line[:-1])
        sample_text.setText(random.choice(lines))
        sample_file.close()


# if this file has been executed
# This is only for testing
if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = Test_UI()
    sys.exit(app.exec_())

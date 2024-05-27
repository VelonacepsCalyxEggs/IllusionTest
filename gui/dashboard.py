import tkinter as tk
from tkinter import messagebox
from gui import testsPage
from PIL import Image, ImageTk
from database import databaseManager
from functions import exit

db = databaseManager.Manager()

class dashboardGUI(tk.Frame):

    def clearTestResults(self):
        # Remove all the test result widgets
        for widget in self.testResultWidgets:
            widget.destroy()
        self.testResultWidgets = []

    def displayUserResults(self, user_id, test):
        # Clear any existing test results first
        self.clearTestResults()

        # Find the next available row index to start displaying the test results
        # This should be one greater than the row index of the last widget before the test results
        start_row_index = self.chooseButton.grid_info()['row'] + 1

        # Fetch user test results from the database
        test = test.get()
        if test == "Poggendorph":
            testResults = db.getPoggendorffResults(user_id)
        elif test == "Muller":
            testResults = db.getMullerLyerResults(user_id)
        elif test == "Vertical-Horizontal":
            testResults = db.getVertHorzResults(user_id)
        else:
             return
        
        self.testResultWidgets = []

        # Create a label to display the test results header
        resultsLabel = tk.Label(self, text="Your Test Results")
        resultsLabel.grid(row=start_row_index, columnspan=3)
        self.testResultWidgets.append(resultsLabel)
        # Display each test result in a separate row
        for i, result in enumerate(testResults, start=start_row_index + 1):
            # Calculate the accuracy percentage
            # 'max_error' vrode is the maximum possible error in pixels
            maxError = 100  
            accuracyPercentage = max(0, ((maxError - result[9]) / maxError) * 100)  # result[9] is vrode 'absolute_error_pixels'

            tk.Label(self, text=f"Test {i-1}:").grid(row=i, column=0)
            tk.Label(self, text=f"Width of Wall: {result[1]}").grid(row=i, column=1)  # w_param

            tk.Label(self, text=f"Accuracy: {accuracyPercentage:.2f}%").grid(row=i, column=3)  # Display accuracy

            # Add the created widgets to the list for tracking
            testLabel = tk.Label(self, text=f"Test {i-4}:")
            testLabel.grid(row=i, column=0)
            self.testResultWidgets.append(testLabel)

            widthLabel = tk.Label(self, text=f"Width of Wall: {result[1]}")
            widthLabel.grid(row=i, column=1)
            self.testResultWidgets.append(widthLabel)

            accuracyLabel = tk.Label(self, text=f"Accuracy: {accuracyPercentage:.2f}%")
            accuracyLabel.grid(row=i, column=3)
            self.testResultWidgets.append(accuracyLabel)


        # Update the layout to ensure the new widgets are displayed correctly
        self.update_idletasks()


    def switchPage(self, user_id):
            # Hide the current frame
            self.grid_forget()
            # Create and show a new frame or page using the grid manager
            newPage = testsPage.testsGUI(self.master, user_id, False, "Dashboard")
            newPage.grid(row=0, column=0, sticky="nsew")

    def __init__(self, master, user_id: int):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        user = db.getTestSubject(user_id)
        self.testResultWidgets = []

        # Configure the master grid to center the frame
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Center the frame within the master
        self.grid(padx=10, pady=10)

        # Label for the tests page, centered at the top
        header_label = tk.Label(self, text="This is the dashboard page")
        header_label.grid(row=0, columnspan=3)
        # Tests Dropdown
        tk.Label(self, text="Choose the test you want to view data for").grid(row=1, columnspan=2)
        self.testVar = tk.StringVar()
        self.testVar.set("Select Test")  # default value
        self.testDropdown = tk.OptionMenu(self, self.testVar, "Poggendorph", "Muller", "Vertical-Horizontal")
        self.testDropdown.grid(row=2, columnspan=2)
        # Call the function to display user results
        self.chooseButton = tk.Button(self, text='Choose', command=lambda: self.displayUserResults(user_id, self.testVar))
        self.chooseButton.grid(row=3, columnspan=3)

        self.grid_rowconfigure(99, weight=1)

        # Add a button to go back to tests
        backButton = tk.Button(self, text="Go to Tests Page", command=lambda: self.switchPage(user_id))
        backButton.grid(row=99, columnspan=3, sticky='s')


        

    
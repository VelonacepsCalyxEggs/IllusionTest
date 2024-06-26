import tkinter as tk
from tkinter import messagebox
from gui import testsPage
from database import databaseManager

db = databaseManager.Manager()

#
# ЗАКРЫВАЙТЕ ЭТО ГОВНО НА КАРАНТИН, ОНО ЗАРАЗНО
# TODO: Переписать к хуям
class dashboardGUI(tk.Frame):

    def calcErrorPrecentage(self, maxError, actualError):
            actualError = min(actualError, maxError)
            # Calculate the accuracy percentage
            accuracyPercentage = (1 - (actualError / maxError)) * 100
            return accuracyPercentage
          

    def clearTestResults(self):
        # Remove all the test result widgets
        for widget in self.testResultWidgets:
            widget.destroy()
        self.testResultWidgets = []

    def displayUserResults(self, user_id, test):
        # Clear any existing test results first
        self.clearTestResults()

        # Find the next available row index to start displaying the test results
        start_row_index = self.chooseButton.grid_info()['row'] + 1

        # Fetch user test results from the database
        test = test.get()
        testResults = []
        if test == "Poggendorph":
            testResults = db.getPoggendorffResults(user_id)
        elif test == "Muller":
            testResults = db.getMullerLyerResults(user_id)
        elif test == "Vertical-Horizontal":
            testResults = db.getVertHorzResults(user_id)
        else:
            return
        
        if len(testResults) == 0:
            messagebox.showwarning('Hmm...', f'No results found for {test}.')
            return

        self.testResultWidgets = []

        # Create a label to display the test results header
        resultsLabel = tk.Label(self, text="Your Test Results")
        resultsLabel.grid(row=start_row_index, sticky="nsew")
        self.testResultWidgets.append(resultsLabel)
        j = 0
        # Display each test result in a separate row
        for i, result in enumerate(testResults, start=start_row_index + 1):
            j = j + 1
            # Display the test-specific parameters
            if test == "Poggendorph":
                maxError = result[11]  # This should be the maximum error possible 
                actualError = result[9]  # The absolute error in pixels from the database
                accuracyPercentage = self.calcErrorPrecentage(maxError, actualError)
                tk.Label(self, text=f"Test {j}: Accuracy: {accuracyPercentage}% ").grid(row=i, column=0)
            elif test == "Muller":
                maxError = result[10]  # This should be the maximum error possible 
                actualError = result[8]  # The absolute error in pixels from the database
                accuracyPercentage = self.calcErrorPrecentage(maxError, actualError)
                tk.Label(self, text=f"Test {j}: Accuracy: {accuracyPercentage}% ").grid(row=i, column=0)
            elif test == "Vertical-Horizontal":
                maxError = result[12]  # This should be the maximum error possible 
                actualError = result[10]  # The absolute error in pixels from the database
                accuracyPercentage = self.calcErrorPrecentage(maxError, actualError)
                tk.Label(self, text=f"Test {j}: Accuracy: {accuracyPercentage}% ").grid(row=i, column=0)


            # Add the created widgets to the list for tracking
            self.testResultWidgets.extend([
                tk.Label(self, text=f"Test {j}: Accuracy: {accuracyPercentage}% "),
            ])

        # Update the layout to ensure the new widgets are displayed correctly
        self.update_idletasks()


    def switchPage(self, user_id):
            # Hide the current frame
            self.grid_forget()
            # Create and show a new frame or page using the grid manager
            newPage = testsPage.testsGUI(self.master, user_id, False, "Dashboard")
            newPage.grid(row=0, column=0, sticky="nsew")

    def __init__(self, user_id: int):
        super().__init__()
        self.testResultWidgets = []
        self.grid(row=0, column=0, sticky="nsew")

        # Configure the master grid to center the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=200)

        # Center the frame within the master
        self.grid(padx=10, pady=10)

        # Label for the tests page, centered at the top
        header_label = tk.Label(self, text="This is the dashboard page")
        header_label.grid(row=0, column=0)

        # Tests Dropdown
        tk.Label(self, text="Choose the test you want to view data for").grid(row=1, column=0, sticky="ew")

                # Tests Dropdown
        tk.Label(self, text="Choose the test you want to view data for").grid(row=1, sticky="ew")
        self.testVar = tk.StringVar()
        self.testVar.set("Select Test")  # default value
        self.testDropdown = tk.OptionMenu(self, self.testVar, "Poggendorph", "Muller", "Vertical-Horizontal")
        self.testDropdown.grid(row=2)
        # Call the function to display user results
        self.chooseButton = tk.Button(self, text='Choose', command=lambda: self.displayUserResults(user_id, self.testVar))
        self.chooseButton.grid(row=3, sticky="ew")

        # Ensure that the 'backButton' is placed at the bottom of the grid
        backButton = tk.Button(self, text="Go to Tests Page", command=lambda: self.switchPage(user_id))
        backButton.grid(row=100, column=0, sticky='s')

        # Add empty rows to push the backButton to the bottom
        for i in range(2, 99):
            self.grid_rowconfigure(i, weight=1)

        

    
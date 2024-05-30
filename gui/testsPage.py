import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from database import databaseManager
from functions import exit
from gui import poggendorphIllusion, mullerLyerIllusion, verticalHorizontalIllusion, dashboard, adminPage
import json

db = databaseManager.Manager()

class testsGUI(tk.Frame):

    def __init__(self, master, user_id: int, redirected: bool, redFrom: str):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        user = db.getTestSubject(user_id)
        with open('./resources/config/config.json', 'r') as f:
            # Read the file
            file_content = f.read()
            config = json.loads(file_content)
            self.debug = config["Debug"]
            print(self.debug)

        print(user)
        # Configure the master grid to center the frame
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Center the frame within the master
        self.grid(padx=10, pady=10)

        # Label for the tests page, centered at the top
        header_label = tk.Label(self, text="This is the tests page")
        header_label.grid(row=0, columnspan=3)

        # welcoming label
        testsPassed = 0
        try:
            pgres = db.getPoggendorffResults(user[0])
            mulres = db.getMullerLyerResults(user[0])
            vhres = db.getVertHorzResults(user[0])
        except Exception as e:
                messagebox.showerror(
                    "Database Error", 
                    f"An error occurred while trying to retrieve data.\n{e}"
                    )
                exit.closeWindow()
        if len(pgres) > 0:
            testsPassed = testsPassed + 1
        if len(mulres) > 0:
            testsPassed = testsPassed + 1
        if len(vhres) > 0:
            testsPassed = testsPassed + 1

        welcome_label = tk.Label(self, text=f'Welcome {user[1]}! You have passed {testsPassed} out of 3 tests!')
        welcome_label.grid(row=1, columnspan=3)

        # List of image paths for each test
        image_paths = [
            "./gui/res/pogandorph.png",
            "./gui/res/muller.png",
            "./gui/res/verticalhorizontal.png",
            # ... add paths for all tests
        ]
        tests = [
            "Poggendorff illusion",
            "Müller-Lyer illusion",
            "Vertical–horizontal illusion"
        ]
        if len(pgres) > 0:
            tests.remove('Poggendorff illusion')
            image_paths.remove('./gui/res/pogandorph.png')
        if len(mulres) > 0:
            tests.remove('Müller-Lyer illusion')
            image_paths.remove('./gui/res/muller.png')
        if len(vhres) > 0:
            tests.remove('Vertical–horizontal illusion')
            image_paths.remove('./gui/res/verticalhorizontal.png')


        # Keep a list to store the image references
        self.image_references = []

        # Create labels for the images and center them
        for col, test in enumerate(tests):
            image = Image.open(image_paths[col])
            resized_image = image.resize((256, 256))
            photo = ImageTk.PhotoImage(resized_image)
            self.image_references.append(photo)
            image_label = tk.Label(self, image=photo)
            image_label.grid(row=2, column=col, padx=10, pady=10, sticky="ew")

        # Create labels for the test names and center them
        for col, test_name in enumerate(tests):
            test_label = tk.Label(self, text=test_name)
            test_label.grid(row=3, column=col, padx=10, pady=10, sticky="ew")

        # Create buttons for the tests and center them

        for col in range(len(tests)):
            def create_button_callback(page):
                return lambda: switchPage(self=self, test_name=page, user_id=user_id)
            test_button = tk.Button(self, text="Start", command=create_button_callback(tests[col]))
            test_button.grid(row=4, column=col, padx=10, pady=13, sticky="ew")

            # Expand the columns so that they take up equal space
            for col in range(len(tests)):
                self.grid_columnconfigure(col, weight=1)

                # Label for the tests page, centered at the top
        dashboard_button = tk.Button(self, text="Dashboard", command=lambda: switchPage(self=self, test_name="Dashboard", user_id=user_id))
        dashboard_button.grid(row=5, columnspan=3)
        if self.debug:
            debug_settings = tk.Button(self, text="Debug Settings", command=lambda: switchPage(self=self, test_name="Debug", user_id=user_id))
            debug_settings.grid(row=6, columnspan=3)
        exit_button = tk.Button(self, text="Exit", command=lambda:exit.closeWindow(self))
        exit_button.grid(row=7, columnspan=3)

        if redirected:
            messagebox.showinfo("Good work!", f"You have passed the {redFrom} test!" )
        


def switchPage(self, test_name, user_id: int):
    # Mapping of test names to their respective page numbers
    test_pages = {
        "Poggendorff illusion": 1,
        "Müller-Lyer illusion": 2,
        "Vertical–horizontal illusion": 3,
        "Dashboard": 4,
        "Debug": 5
    }

    # Update the mapping if tests are passed
    pgres = db.getPoggendorffResults(user_id)
    mulres = db.getMullerLyerResults(user_id)
    vhres = db.getVertHorzResults(user_id)
    if len(pgres) > 0:
        del test_pages["Poggendorff illusion"]
    if len(mulres) > 0:
        del test_pages["Müller-Lyer illusion"]
    if len(vhres) > 0:
        del test_pages["Vertical–horizontal illusion"]

    # Get the page number from the updated mapping
    page = test_pages.get(test_name)

    # Create and show a new frame or page using the grid manager
    if page is not None:
        self.grid_forget()
        if page == 1:
            illusion_frame = poggendorphIllusion.PoggendorffIllusion(user_id=user_id)
            illusion_frame.grid()
        elif page == 2:
            illusion_frame = mullerLyerIllusion.MullerLyerIllusion(user_id=user_id)
            illusion_frame.grid()
        elif page == 3:
            illusion_frame = verticalHorizontalIllusion.verticalHorizontalIllusion(user_id=user_id)
            illusion_frame.grid()
        elif page == 4:
            dashboard_frame = dashboard.dashboardGUI(self.master, user_id=user_id)
            dashboard_frame.grid()
        elif page == 5:
            debug_frame = adminPage.adminGUI(self.master, user_id=user_id)
            debug_frame.grid()
    else:
        messagebox.showerror("Error", "The selected test is not available.")
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from database import databaseManager
from functions import exit
from gui import poggendorphIllusion, mullerLyerIllusion, verticalHorizontalIllusion, dashboard

db = databaseManager.Manager()

class testsGUI(tk.Frame):

    def __init__(self, master, user_id: int, redirected: bool, redFrom: str):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        user = db.getTestSubject(user_id)
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
        i = 0
        for col in range(len(tests)):
            i += 1
            def create_button_callback(page):
                return lambda: switchPage(self=self, page=page, user_id=user_id)
            test_button = tk.Button(self, text="Start", command=create_button_callback(i))
            test_button.grid(row=4, column=col, padx=10, pady=13, sticky="ew")

            # Expand the columns so that they take up equal space
            for col in range(len(tests)):
                self.grid_columnconfigure(col, weight=1)

                # Label for the tests page, centered at the top
        dashboard_button = tk.Button(self, text="Dashboard", command=lambda: switchPage(self=self, page=4, user_id=user_id))
        dashboard_button.grid(row=5, columnspan=3)

        if redirected:
            messagebox.showinfo("Good work!", f"You have passed the {redFrom} test!" )
        


def switchPage(self, page, user_id: int):
    # Create and show a new frame or page using the grid manager
    print(page)
    if (page == 1):
        # Hide the current frame
        self.grid_forget()
        illusion_frame = poggendorphIllusion.PoggendorffIllusion(user_id=user_id)
        illusion_frame.grid()
    elif (page == 2):
        # Hide the current frame
        self.grid_forget()
        illusion_frame = mullerLyerIllusion.MullerLyerIllusion(user_id=user_id)
        illusion_frame.grid()
    elif (page == 3):
        # Hide the current frame
        self.grid_forget()
        illusion_frame = verticalHorizontalIllusion.verticalHorizontalIllusion(user_id=user_id)
        illusion_frame.grid()
    
    elif (page == 4):
                # Hide the current frame
        self.grid_forget()
        dashboard_frame = dashboard.dashboardGUI(self.master, user_id=user_id)
        dashboard_frame.grid()
    else:
        return

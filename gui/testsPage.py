import tkinter as tk
from PIL import Image, ImageTk
from database import databaseManager
from gui import poggendorphIllusion, mullerLyerIllusion

db = databaseManager.Manager()

class testsGUI(tk.Frame):
    def __init__(self, master, user_id: int):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        
        # Configure the master grid to center the frame
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Center the frame within the master
        self.grid(padx=10, pady=10)

        # Label for the tests page, centered at the top
        header_label = tk.Label(self, text="This is the tests page")
        header_label.grid(row=0, columnspan=3)

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

        # Keep a list to store the image references
        self.image_references = []

        # Create labels for the images and center them
        for col, image_path in enumerate(image_paths):
            image = Image.open(image_path)
            resized_image = image.resize((256, 256))
            photo = ImageTk.PhotoImage(resized_image)
            self.image_references.append(photo)
            image_label = tk.Label(self, image=photo)
            image_label.grid(row=1, column=col, padx=10, pady=10, sticky="ew")

        # Create labels for the test names and center them
        for col, test_name in enumerate(tests):
            test_label = tk.Label(self, text=test_name)
            test_label.grid(row=2, column=col, padx=10, pady=10, sticky="ew")

        # Create buttons for the tests and center them
        i = 0
        for col in range(len(tests)):
            i += 1
            def create_button_callback(page):
                return lambda: switchPage(self=self, page=page, user_id=user_id)
            
            test_button = tk.Button(self, text="Start", command=create_button_callback(i))
            test_button.grid(row=3, column=col, padx=10, pady=13, sticky="ew")

            # Expand the columns so that they take up equal space
            for col in range(len(tests)):
                self.grid_columnconfigure(col, weight=1)

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
    else:
        return

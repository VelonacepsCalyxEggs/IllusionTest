import tkinter as tk
from tkinter import messagebox
from gui import testsPage
from functions import register
from database import databaseManager
class registerGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        
        # Configure the master grid to center the frame
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        # Center the frame within the master
        self.grid(padx=10, pady=10)

        # Widgets
        tk.Label(self, text="This is a register page").grid(row=0, columnspan=2)
        tk.Label(self, text="Name").grid(row=1, columnspan=2)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=2, columnspan=2)
        tk.Label(self, text="Age").grid(row=3, columnspan=2)
        self.age_entry = tk.Entry(self)
        self.age_entry.grid(row=4, columnspan=2)

        # Gender Dropdown
        tk.Label(self, text="Gender").grid(row=5, columnspan=2)
        self.gender_var = tk.StringVar()
        self.gender_var.set("Select Gender")  # default value
        self.gender_dropdown = tk.OptionMenu(self, self.gender_var, "Male", "Female", "Other")
        self.gender_dropdown.grid(row=6, columnspan=2)

        # Register Button
        self.register_button = tk.Button(self, text="Register", command=self.register)
        self.register_button.grid(row=7, columnspan=2)

        # Register Button
        self.register_button = tk.Button(self, text="Register", command=lambda: attemptRegistration(self))
        self.register_button.grid(row=7, columnspan=2)

        # Center the widgets by expanding the column configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


def attemptRegistration(self):
        # Get the values from the entry fields and the gender variable
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_var.get()

        # Call the imported register function and capture the return message
        registrationStatus, regMessage = register.register(name, age, gender)

        # Check the message and display the appropriate messagebox
        if registrationStatus == "Registration Failed":
            messagebox.showerror("Registration Failed", regMessage)
        else:
            messagebox.showinfo("Registration Successful", regMessage)
            user_id = None
            try: 
                db = databaseManager.Manager()
                user_id = db.getTestSubjectId(name, age)
            except Exception as e:
                messagebox.showerror(
                    "Database Error", 
                    f"An error occurred while trying to retrieve the user ID\n{e}"
                    )
            
            switchPage(self, user_id)

def switchPage(self, user_id):
    # Hide the current frame
    self.grid_forget()
    # Create and show a new frame or page using the grid manager
    newPage = testsPage.testsGUI(self.master, user_id)
    newPage.grid(row=0, column=0, sticky="nsew")
    # Configure the master grid to center the new frame
    self.master.grid_rowconfigure(0, weight=1)
    self.master.grid_columnconfigure(0, weight=1)
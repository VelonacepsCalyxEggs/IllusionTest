import tkinter as tk
from tkinter import messagebox, Label, Button, IntVar, Radiobutton
from gui import testsPage
import json

class adminGUI(tk.Frame):

    def __init__(self, master, user_id: int):
        super().__init__(master)
        self.user_id = user_id
        self.load_config()
        self.create_widgets()
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(padx=10, pady=10)
        
    def load_config(self):
        with open('./resources/config/config.json', 'r') as f:
            self.config = json.load(f)

    def save_config(self):
        with open('./resources/config/config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def create_widgets(self):
        # Debug setting
        self.debug_var = IntVar(value=self.config["Debug"])
        Label(self, text="Debug:").grid(row=1, column=0)
        Radiobutton(self, text="True", variable=self.debug_var, value=True).grid(row=1, column=1)
        Radiobutton(self, text="False", variable=self.debug_var, value=False).grid(row=1, column=2)

        # Dark Mode setting
        self.theme_var = IntVar(value=self.config["DarkTheme"])
        Label(self, text="Dark Theme:").grid(row=2, column=0)
        Radiobutton(self, text="True", variable=self.theme_var, value=True).grid(row=2, column=1)
        Radiobutton(self, text="False", variable=self.theme_var, value=False).grid(row=2, column=2)

        # Timer setting
        self.timer_var = IntVar(value=self.config["Timer"])
        Label(self, text="Timer:").grid(row=3, column=0)
        Radiobutton(self, text="True", variable=self.timer_var, value=True).grid(row=3, column=1)
        Radiobutton(self, text="False", variable=self.timer_var, value=False).grid(row=3, column=2)

        # Show timer?
        self.showTimer_var = IntVar(value=self.config["ShowTimer"])
        Label(self, text="Show Timer:").grid(row=4, column=0)
        Radiobutton(self, text="True", variable=self.showTimer_var, value=True).grid(row=4, column=1)
        Radiobutton(self, text="False", variable=self.showTimer_var, value=False).grid(row=4, column=2)

        # Timer sound setting
        self.timerSnd_var = IntVar(value=self.config["TimerSnd"])
        Label(self, text="Timer Snd:").grid(row=5, column=0)
        Radiobutton(self, text="True", variable=self.timerSnd_var, value=True).grid(row=5, column=1)
        Radiobutton(self, text="False", variable=self.timerSnd_var, value=False).grid(row=5, column=2)

        Button(self, text="Save", command=self.update_config).grid(row=10, columnspan=3)
        Button(self, text="Back", command=lambda: self.switchPage(user_id=self.user_id)).grid(row=11, columnspan=3)


    def update_config(self):
        self.config["Debug"] = bool(self.debug_var.get())
        self.config["DarkTheme"] = bool(self.theme_var.get())
        self.config["Timer"] = bool(self.timer_var.get())
        self.config["ShowTimer"] = bool(self.showTimer_var.get())
        self.config["TimerSnd"] = bool(self.timerSnd_var.get())

        self.save_config()
        messagebox.showinfo("Info", "Configuration updated successfully!")

    def switchPage(self, user_id):
            # Hide the current frame
            self.grid_forget()
            # Create and show a new frame or page using the grid manager
            newPage = testsPage.testsGUI(self.master, user_id, False, "Dashboard")
            newPage.grid(row=0, column=0, sticky="nsew")
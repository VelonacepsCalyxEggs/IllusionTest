import tkinter as tk
class registerGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="This is a register page").pack()
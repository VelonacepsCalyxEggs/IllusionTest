import tkinter as tk
class testsGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="This is the test page").pack()
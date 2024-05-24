import tkinter as tk

class PoggendorffIllusion(tk.Tk):
    def __init__(self):
        super().__init__()

        # Create canvas
        self.canvas = tk.Canvas(self, width=400, height=300)
        self.canvas.grid()



        # Vertical lines (drawn after the diagonal)
        self.canvas.create_line(150, 50, 150, 250, fill='black')
        self.canvas.create_line(100, 50, 100, 250, fill='black')
        # Diagonal (thicker line)
        self.canvas.create_line(75, 100, 175, 200, fill='black', width=2)
        # Create a rectangular shape (wall) between the vertical lines
        self.canvas.create_rectangle(100, 50, 150, 250, fill='gray')
        # Wall, invisible
        self.canvas.create_rectangle(150, 50, 200, 250, fill='white')
        # Continuous line with the same angle as the diagonal line
        # Starting at x0=100, y0=75 and ending at x1=150, y1=125
        self.continuous_line = self.canvas.create_line(150, 75, 200, 125, fill='black', width=2)


        # Create slider
        self.slider = tk.Scale(self, from_=50, to=250, orient='horizontal', command=self.adjust_line)
        self.slider.grid()

    def adjust_line(self, value):
        # Calculate the original slope of the diagonal line
        x0, y0, x1, y1_diagonal = self.canvas.coords(self.continuous_line)
        slope_diagonal = (y1_diagonal - y0) / (x1 - x0)

        # Calculate the new y0 and y1 based on the slider value and original slope
        y0_new = int(value)
        y1_new = y0_new + slope_diagonal * (x1 - x0)

        # Adjust the line coordinates
        self.canvas.coords(self.continuous_line, x0, y0_new, x1, y1_new)

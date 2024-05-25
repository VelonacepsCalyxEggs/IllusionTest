import tkinter as tk
import sys

if __name__ == '__main__':
    current_absolute_path = sys.path[0][:sys.path[0].rfind('\\')]
    sys.path.append(current_absolute_path)

from utils.geometry_utils import Vector2D, Line

class PoggendorffIllusion(tk.Frame):
    w_param = 10 # width of the wall
    h_param = 0 # offest of second line
    alpha = 45 # angle of the diagonal line
    beta = 0 # angle of illusion itself

    def __init__(self):
        super().__init__()

        # Create canvas
        self.canvas = tk.Canvas(self, width=512, height=512)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Configure the row and column weights where the canvas is placed
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.draw_illusion()

        # Create slider to adjust the line position
        self.slider = tk.Scale(self, from_=0, to=384, orient='horizontal', command=self.adjust_line)
        self.slider.grid()

        # system buttons to redraw the illusion and sliders to adjast values
        self.debug_lables_title = tk.Label(self, text='Debug controls')
        self.debug_lables_title.grid()

        # Create a button to redraw the illusion
        self.redraw_button = tk.Button(self, text='Redraw', command=self.draw_illusion)
        self.redraw_button.grid()

        # Create sliders to adjust the parameters of the illusion
        
        # Width of the wall
        self.debug_lables_widht = tk.Label(self, text='Width of the wall')
        self.debug_lables_widht.grid()
        
        self.slider_w = tk.Scale(self, from_=10, to=100, orient='horizontal', command=self.adjust_w)
        self.slider_w.set(self.w_param)
        self.slider_w.grid()

        # Height of secondary line
        self.debug_lables_height = tk.Label(self, text='Height of secondary line')
        self.debug_lables_height.grid()

        self.slider_h = tk.Scale(self, from_=-75, to=125, orient='horizontal', command=self.adjust_h)
        self.slider_h.set(self.h_param)
        self.slider_h.grid()

        # Angle of the diagonal line
        self.debug_lables_alpha = tk.Label(self, text='Angle of the diagonal line')
        self.debug_lables_alpha.grid()

        self.slider_alpha = tk.Scale(self, from_=-90, to=90, orient='horizontal', command=self.adjust_alpha)
        self.slider_alpha.set(self.alpha)
        self.slider_alpha.grid()

        # Angle of the illusion
        self.debug_lables_beta = tk.Label(self, text='Angle of the illusion NOT WORKING YET')
        self.debug_lables_beta.grid()
        
        self.slider_beta = tk.Scale(self, from_=0, to=360, orient='horizontal', command=self.adjust_beta)
        self.slider_beta.set(self.beta)
        self.slider_beta.grid()

    def draw_illusion(self):

        # Clear the canvas
        self.canvas.delete('all')
        print(self.w_param, self.h_param, self.alpha, self.beta)

        #Vertical lines using the Line class
        line1 = Line(Vector2D(128, 0), Vector2D(0,1), 200)
        line1.swap_origin()
        line1.rotate(self.beta)
        self.canvas.create_line(line1.org.x, line1.org.y, line1.secn.x, line1.secn.y, fill='black', width=1)
        
        line2 = Line(Vector2D(128+self.w_param, 0), Vector2D(0,1), 200)
        line2.swap_origin()
        line2.rotate(self.beta)
        self.canvas.create_line(line2.org.x, line2.org.y, line2.secn.x, line2.secn.y, fill='black', width=1)

        # Diagonal line using the Line class
        main_line = Line(Vector2D(128, 75), Vector2D(-1,0), 50)
        main_line.rotate(self.alpha)
        self.canvas.create_line(main_line.org.x, main_line.org.y, main_line.secn.x, main_line.secn.y, fill='red', width=2)

        addional_line = Line(Vector2D(128+self.w_param, 75 + self.h_param), Vector2D(1,0), 50)
        addional_line.rotate(self.alpha)
        self.canvas.create_line(addional_line.org.x, addional_line.org.y, addional_line.secn.x, addional_line.secn.y, fill='blue', width=2)

        # Continuous line with the same angle as the diagonal line using the Line class
        continuous_line = Line(Vector2D(128+self.w_param, 70), Vector2D(1,0), 50)
        continuous_line.rotate(self.alpha)
        
        self.continuous_line = self.canvas.create_line(continuous_line.org.x, continuous_line.org.y, 
                                                       continuous_line.secn.x, continuous_line.secn.y, 
                                                       fill='red', width=2)
        self.canvas.scale('all', 0, 0, 2, 2) # TODO: Look into how the elements are positioned, currently this is causing problems.


    def adjust_alpha(self, value):
        self.alpha = int(value)
    
    def adjust_beta(self, value):
        self.beta = int(value)
    
    def adjust_h(self, value):
        self.h_param = int(value)
    
    def adjust_w(self, value):
        self.w_param = int(value)

    def adjust_line(self, value):
        # Calculate the original slope of the diagonal line
        x0, y0, x1, y1_diagonal = self.canvas.coords(self.continuous_line)
        slope_diagonal = (y1_diagonal - y0) / (x1 - x0)

        # Calculate the new y0 and y1 based on the slider value and original slope
        y0_new = int(value)
        y1_new = y0_new + slope_diagonal * (x1 - x0)

        # Adjust the line coordinates
        self.canvas.coords(self.continuous_line, x0, y0_new, x1, y1_new)

if __name__ == '__main__':
    app = PoggendorffIllusion()
    app.mainloop()
import tkinter as tk
from tkinter import messagebox
from gui import testsPage
import random
from utils.geometry_utils import Vector2D, Line, pixel_to_mm
from database import databaseManager
from pygame import mixer  # Cross-platform solution
import json

class PoggendorffIllusion(tk.Frame):
    w_param = 10 # width of the wall
    h_param = 0 # offset of second line
    alpha = 45 # angle of the diagonal line
    beta = 0 # angle of illusion itself
    illNum = 0 # number of the generated illusion
    intersection = Vector2D(0, 0)
    subject_response = Vector2D(0, 0)
    user_id = None

    line_colours = [
        'red',
        'blue',
    ]

    mixer.init()
    tick_sound = mixer.Sound('./resources/sounds/tick.wav')  # Load your sound file here

    def __init__(self, user_id: int):
        super().__init__()
                # check config
        with open('./resources/config/config.json', 'r') as f:
            # Read the file
            file_content = f.read()
            config = json.loads(file_content)
            self.debug = config["Debug"]
            print(self.debug)
        self.user_id = user_id

        self.timer = tk.Label(self, font=('Helvetica', 48), text="15:00")
        self.timer.grid(row=0, column=0, sticky='nsew')
        self.countdown_running = True
        self.countdown(900)

        # Create canvas
        self.canvas = tk.Canvas(self, width=512, height=512)
        self.canvas.grid(row=1, column=0, sticky='nsew')

        # Configure the row and column weights where the canvas is placed
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.draw_illusion()

        self.counter = tk.Label(self, text=f'Test number {self.illNum} out of 10')
        self.counter.grid()

        # Create slider to adjust the line position
        self.slider = tk.Scale(self, from_=0, to=200, orient='horizontal', command=self.adjust_line)
        self.slider.set(70)
        self.slider.grid()
        
        self.NextButton = tk.Button(self, text='Submit', command=self.submit_data)
        self.NextButton.grid()
        
        if self.debug == 'True':
            # system buttons to redraw the illusion and sliders to adjust values
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

            self.slider_h = tk.Scale(self, from_=0, to=200, orient='horizontal', command=self.adjust_h)
            self.slider_h.set(self.h_param)
            self.slider_h.grid()

            # Angle of the diagonal line
            self.debug_lables_alpha = tk.Label(self, text='Angle of the diagonal line')
            self.debug_lables_alpha.grid()

            self.slider_alpha = tk.Scale(self, from_=-90, to=90, orient='horizontal', command=self.adjust_alpha)
            self.slider_alpha.set(self.alpha)
            self.slider_alpha.grid()

            # Angle of the illusion
            self.debug_lables_beta = tk.Label(self, text='Angle of the illusion')
            self.debug_lables_beta.grid()
            
            self.slider_beta = tk.Scale(self, from_=0, to=360, orient='horizontal', command=self.adjust_beta)
            self.slider_beta.set(self.beta)
            self.slider_beta.grid()

    def draw_illusion(self, line_pos=0):

        # Clear the canvas
        self.canvas.delete('all')
        # print(self.w_param, self.h_param, self.alpha, self.beta)

        
        #Vertical lines using the Line class
        line1 = Line(Vector2D(128, 0), Vector2D(0,1), 200)
        line1.swap_origin()

        self.line2 = Line(Vector2D(128+self.w_param, 0), Vector2D(0,1), 200)
        self.line2.swap_origin()
        
        self.center = Vector2D((line1.org.x + self.line2.org.x)/2, line1.len/2)
        line1.rotate_around_point(self.beta, self.center)
        self.line2.rotate_around_point(self.beta, self.center)

        line1.draw(self.canvas, color='black', width=1)
        self.line2.draw(self.canvas, color='black', width=1)


        # Diagonal line using the Line class
        main_line = Line(Vector2D(128, 75), Vector2D(-1,0), 50)
        main_line.rotate(self.alpha)
        main_line.rotate_around_point(self.beta, self.center)
        main_line.draw(self.canvas, color=self.line_colours[0], width=2)

        addional_line = Line(Vector2D(128+self.w_param, self.h_param), Vector2D(1,0), 50)
        addional_line.rotate(self.alpha)
        addional_line.rotate_around_point(self.beta, self.center)
        addional_line.draw(self.canvas, color=self.line_colours[1], width=2)

        # Continuous line with the same angle as the diagonal line using the Line class
        self.continuous_line = Line(Vector2D(128+self.w_param, 0 + line_pos), Vector2D(1,0), 50)
        self.continuous_line.rotate(self.alpha)
        self.continuous_line.rotate_around_point(self.beta, self.center)
        self.subject_response = self.continuous_line.org
        
        self.continuous_line_obj = self.continuous_line.draw(self.canvas, color=self.line_colours[0], width=2)

        # DEBUG Square at the intersection of the lines
        self.intersection = Line.calculate_intersection(Line, main_line, self.line2)
        # Create the rectangle and keep a reference to it
        self.debug_square = self.canvas.create_rectangle(self.intersection.x-1, self.intersection.y-1, self.intersection.x+1, self.intersection.y+1, fill='green')

        if self.debug != 'True':
            # Make the rectangle invisible
            self.canvas.itemconfig(self.debug_square, state='hidden')

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
        self.draw_illusion(int(value))

    def submit_data(self):
        
        # SEND DATA TO SQL DB
        print(f"Intersection: {self.intersection}")
        print(f"Subject response: {self.subject_response}")
        print(f"Error in pixels: {self.intersection - self.subject_response}")
        absolute_error = (self.intersection - self.subject_response).magnitude()
        
        dpi = self.winfo_fpixels('1i')

        # calculate maximum possible error in pixels
        possible_values = [self.line2.org - self.intersection, self.line2.secn - self.intersection]
        max_error_pixel = possible_values[0].magnitude() if possible_values[1].magnitude() < possible_values[0].magnitude() else possible_values[1].magnitude()

        # calculate the absolute error in mm
        max_error_mm = pixel_to_mm(max_error_pixel, dpi, 2) # 2 is a magic number, it is the scale of the illusion
        absolute_error_mm = pixel_to_mm(absolute_error, dpi, 2) # 2 is a magic number, it is the scale of the illusion
        
        print(f"Max error in mm: {max_error_mm}")
        print(f"Max error in pixels: {max_error_pixel}")

        print(f"Absolute error in mm: {absolute_error_mm}")
        print(f"Absolute error in pixels: {absolute_error}")

        try:
            db = databaseManager.Manager()
            db.savePoggendorffResult(
                self.user_id, self.w_param, self.h_param, self.alpha,
                self.beta, self.intersection.x, self.intersection.y,
                self.subject_response.x, self.subject_response.y,
                absolute_error, absolute_error_mm, max_error_pixel,
                max_error_mm)
            
        except Exception as e:
            print(f"An error occurred while trying to save the data\n{e}")
    
        # Generate a new illusion
        self.w_param = random.randint(2, 10) # width of the wall
        self.h_param = random.randint(75, 150) # offset of second line
        self.alpha = random.randint(10, 80) # angle of the diagonal line
        self.beta = random.randint(0, 360) # angle of illusion itself

        # If user had reached 10 illusions, we redirect to the tests page.
        # On the tests page, we show the user a message box with info that he had completed this test. i.e prob verified by database query.
        if self.illNum != 9:
            self.draw_illusion()

            self.illNum = self.illNum + 1
            self.counter.configure(text=self.illNum)
        else:
            self.switchPage()

    def switchPage(self):
        self.stop_countdown()
        # Hide the current frame
        self.grid_forget()
        # Create and show a new frame or page using the grid manager
        newPage = testsPage.testsGUI(self.master, self.user_id, True, "Poggendorf Illusion")
        newPage.grid(row=0, column=0, sticky="nsew")
        # Configure the master grid to center the new frame
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def stop_countdown(self):
        self.countdown_running = False

    def countdown(self, time_remaining):
        if time_remaining > 0 and self.countdown_running:
            mins, secs = divmod(time_remaining, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.timer.configure(text=timeformat)
            self.tick_sound.play()
            self.after(1000, self.countdown, time_remaining-1)
        elif not self.countdown_running:
            self.timer.configure(text="Timer stopped")
        else:
            self.timer.configure(text="Time's up!")
            self.times_up()

    def times_up(self):
        # This function will be called when the timer ends
        messagebox.showinfo("Timer", "Time's up!")
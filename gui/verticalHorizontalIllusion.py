import tkinter as tk
from tkinter import messagebox
from gui import testsPage
import random
from utils.geometry_utils import Vector2D, Line, Circle, pixel_to_mm
from utils.verthorizDataStore import Test
from database import databaseManager
from pygame import mixer  # Cross-platform solution
import json
class verticalHorizontalIllusion(tk.Frame):
    l_param = 64 # length of the horizontal line
    h_param = 75 # height of the vertical lines
    d_param = 0 # position of the vertical line
    alpha = 0 # angle of the vertical line
    beta = 0 # angle of the illusion
    illNum = 0 # number of the generated illusion
    desired_point = Vector2D(0,0)
    subject_response = Vector2D(0, 0)
    user_id = None
    path = 'resources\\tests\\vertical_horizontal.json'
    test_data = Test(path)
    lines_colour = [
        'blue',
        'red',
    ]

    mixer.init()
    tick_sound = mixer.Sound('./resources/sounds/tick.wav')  # Load your sound file here

    def __init__(self, user_id: int):
        super().__init__()
        with open('./resources/config/config.json', 'r') as f:
            # Read the file
            file_content = f.read()
            config = json.loads(file_content)
            self.debug = config["Debug"]
            self.timer = config["Timer"]
            self.showTimer = config['ShowTimer']
            self.timerSnd = config['TimerSnd']

        self.user_id = user_id

        illusion = self.test_data.get_next_illusion()
        self.l_param = illusion.l_param
        self.h_param = illusion.h_param
        self.d_param = illusion.d_param
        self.alpha = illusion.alpha
        self.beta = illusion.beta
        self.lines_colour = illusion.lines_colour

        self.timer = tk.Label(self, font=('Helvetica', 48), text="15:00")
        self.timer.grid(row=0, column=0, sticky='nsew')
        if not self.showTimer:
            self.timer.grid_forget()
        self.countdown_running = True
        self.countdown(900)

        # Create canvas
        self.canvas = tk.Canvas(self, width=512, height=512)
        self.canvas.grid(row=1, column=0, sticky='nsew')

        # Configure the row and column weights where the canvas is placed
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.draw_illusion()

        self.counter = tk.Label(self, text=self.illNum)
        self.counter.grid()

        # Create slider to adjust the circle position
        self.slider = tk.Scale(self, from_=0, to=128, orient='horizontal', command=self.adjust_line)
        self.slider.set(35)
        self.slider.grid()
        
        self.NextButton = tk.Button(self, text='Submit', command=self.submit_data)
        self.NextButton.grid()
        if self.debug:
            # system buttons to redraw the illusion and sliders to adjast values
            self.debug_lables_title = tk.Label(self, text='Debug controls')
            self.debug_lables_title.grid()

            # Create a button to redraw the illusion
            self.redraw_button = tk.Button(self, text='Redraw', command=self.draw_illusion)
            self.redraw_button.grid()

            # Create sliders to adjust the parameters of the illusion
            
            # Length of the horizontal line
            self.debug_lables_widht = tk.Label(self, text='Length of the horizontal line')
            self.debug_lables_widht.grid()
            
            self.slider_r = tk.Scale(self, from_=1, to=128, orient='horizontal', command=self.adjust_l)
            self.slider_r.set(self.l_param)
            self.slider_r.grid()

            # Height of the vertical lines
            self.debug_lables_height = tk.Label(self, text='Height of the vertical lines')
            self.debug_lables_height.grid()

            self.slider_d = tk.Scale(self, from_=128, to=1, orient='horizontal', command=self.adjust_h)
            self.slider_d.set(self.h_param)
            self.slider_d.grid()

            # Position of the vertical line
            self.debug_lables_position = tk.Label(self, text='Position of the vertical line')
            self.debug_lables_position.grid()

            self.slider_position = tk.Scale(self, from_=-64, to=64, orient='horizontal', command=self.adjust_d)
            self.slider_position.set(self.d_param)
            self.slider_position.grid()

            # Angle of the vertical line
            self.debug_lables_alpha = tk.Label(self, text='Angle of the vertical line')
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



    def draw_illusion(self, length=35):
        self.canvas.delete('all')

        # Calculate the position of the lines
        self.ill_center = Vector2D(128, 128)


        self.desired_point = Vector2D(self.ill_center.x, self.h_param)

        horizontal_line = Line(Vector2D(self.ill_center.x - self.l_param/2, self.ill_center.y), Vector2D(1, 0), self.l_param)
        self.vertical_line = Line(Vector2D(self.ill_center.x + self.d_param, self.ill_center.y), Vector2D(0, -1), length)

        self.vertical_line.rotate_around_point(self.alpha, Vector2D(self.ill_center.x + self.d_param, self.ill_center.y))

        horizontal_line.rotate_around_point(self.beta, self.ill_center)
        self.vertical_line.rotate_around_point(self.beta, self.ill_center)

        self.desired_point.rotate_around_point(self.alpha, Vector2D(self.ill_center.x + self.d_param, self.ill_center.y))
        self.desired_point.rotate_around_point(self.beta, self.ill_center)

        self.subject_response = self.vertical_line.secn

        # Draw the lines
        horizontal_line.draw(self.canvas, color=self.lines_colour[0], width=1)
        self.vertical_line.draw(self.canvas, color=self.lines_colour[1], width=1)

        # Debug circle at desried point
        if self.debug:
            self.circle = Circle(self.desired_point, 1)
            self.circle.draw(self.canvas, color='white', width=1)

            self.center_circle = Circle(self.ill_center, 1)
            self.center_circle.draw(self.canvas, color='white', width=1)

            
        self.canvas.scale('all', 0, 0, 2, 2) # TODO: Look into how the elements are positioned, currently this is causing problems.

    def adjust_alpha(self, value):
        self.alpha = int(value)

    def adjust_beta(self, value):
        self.beta = int(value)
    
    def adjust_h(self, value):
        self.h_param = int(value)
    
    def adjust_d(self, value):
        self.d_param = int(value)

    def adjust_l(self, value):
        self.l_param = int(value)

    def adjust_line(self, value):          
        self.draw_illusion(int(value))

    def submit_data(self):
        
        # SEND DATA TO SQL DB
        dpi = self.winfo_fpixels('1i')
        

        absolute_error = (self.desired_point - self.subject_response).magnitude()
        absolute_error_mm = pixel_to_mm(absolute_error, dpi, 2) # 2 is a magic number, it is the scale of the illusion
        
        max_error_pixel = (self.desired_point - self.vertical_line.org).magnitude()
        max_error_mm = pixel_to_mm(max_error_pixel, dpi, 2) # 2 is a magic number, it is the scale of the illusion
    
        try:
            db = databaseManager.Manager()
            db.saveVertHorzResult(
                self.user_id, self.l_param, self.h_param, self.d_param,
                self.alpha, self.beta, self.desired_point.x, 
                self.desired_point.y, self.subject_response.x, 
                self.subject_response.y, absolute_error, 
                absolute_error_mm, max_error_pixel, max_error_mm)
            
        except Exception as e:
            print(f"An error occurred while trying to save the data\n{e}")
    
        # Generate a new illusion
        illusion = self.test_data.get_next_illusion()
        self.l_param = illusion.l_param
        self.h_param = illusion.h_param
        self.d_param = illusion.d_param
        self.alpha = illusion.alpha
        self.beta = illusion.beta
        self.lines_colour = illusion.lines_colour

        # If user had reached 10 illusions, we redirect to the tests page.
        # On the tests page, we show the user a message box with info that he had completed this test. i.e prob verified by database query.
        if self.illNum != self.test_data.illusion_amount - 1:
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
        newPage = testsPage.testsGUI(self.master, self.user_id, True, "Müller-Lyer illusion")
        newPage.grid(row=0, column=0, sticky="nsew")
        # Configure the master grid to center the new frame
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def stop_countdown(self):
        self.countdown_running = False

    def countdown(self, time_remaining):
        if self.timer:
            if time_remaining > 0 and self.countdown_running:
                mins, secs = divmod(time_remaining, 60)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                self.timer.configure(text=timeformat)
                if self.timerSnd:
                    self.tick_sound.play()
                self.after(1000, self.countdown, time_remaining-1)
            elif not self.countdown_running:
                self.timer.configure(text="Timer stopped")
            else:
                self.timer.configure(text="Time's up!")
                self.times_up()
        else:
            1

    def times_up(self):
        # This function will be called when the timer ends
        messagebox.showinfo("Timer", "Time's up!")
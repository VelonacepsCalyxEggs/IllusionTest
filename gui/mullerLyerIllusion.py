import tkinter as tk
from tkinter import messagebox
from gui import testsPage
import random
from utils.geometry_utils import Vector2D, Line, Circle, pixel_to_mm
from utils.mullerLyerDataStore import Test
from database import databaseManager
from pygame import mixer  # Cross-platform solution
import json
class MullerLyerIllusion(tk.Frame):
    r_param = 10 # radius of the circles
    d_param = 20 # distance between the circles
    alpha = 0 # angle of the illusion
    illNum = 0 # number of the generated illusion
    desired_point = Vector2D(4*r_param + 2*d_param, 128)
    subject_response = Vector2D(0, 0)
    user_id = None
    path = 'resources\\tests\\muller_lyuer.json'
    test_data = Test(path)
    circles_fill = [
        'blue',
        'blue',
        'red',   
    ]
    circles_outline = [
        'black',
        'black',
        'black',
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
        self.r_param = illusion.r_param
        self.d_param = illusion.d_param
        self.circles_fill = illusion.fill
        self.circles_outline = illusion.outline

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
        self.slider = tk.Scale(self, from_=256 - self.d_param, to=0, orient='horizontal', command=self.adjust_circle)
        self.slider.set(70)
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
            
            # Radius of the circles
            self.debug_lables_widht = tk.Label(self, text='Radius of the circle')
            self.debug_lables_widht.grid()
            
            self.slider_r = tk.Scale(self, from_=2, to=25, orient='horizontal', command=self.adjust_r)
            self.slider_r.set(self.r_param)
            self.slider_r.grid()

            # Distance between the lines
            self.debug_lables_height = tk.Label(self, text='Distance between the lines')
            self.debug_lables_height.grid()

            self.slider_d = tk.Scale(self, from_=10, to=150, orient='horizontal', command=self.adjust_d)
            self.slider_d.set(self.d_param)
            self.slider_d.grid()

            # Angle of the illusion
            self.debug_lables_alpha = tk.Label(self, text='Angle of the illusion')
            self.debug_lables_alpha.grid()

            self.slider_alpha = tk.Scale(self, from_=0, to=360, orient='horizontal', command=self.adjust_alpha)
            self.slider_alpha.set(self.alpha)
            self.slider_alpha.grid()

    def draw_illusion(self, circle_pos=0):

        # Clear the canvas
        self.canvas.delete('all')

        self.ill_center = Vector2D(128, 128)
        self.desired_point = Vector2D(3*self.r_param + 2*self.d_param, 128)
        
        # calculate the position of the circles
        first_circle_pos = Vector2D(self.r_param, self.ill_center.y)
        second_circle_pos = Vector2D(self.r_param + self.d_param, self.ill_center.y)
        third_circle_pos = Vector2D(256 - self.r_param - 2 - circle_pos, self.ill_center.y)

        # draw the circles
        first_circle = Circle(first_circle_pos, self.r_param)
        second_circle = Circle(second_circle_pos, self.r_param)
        third_circle = Circle(third_circle_pos, self.r_param)

        first_circle.rotate_around_point(self.alpha, self.ill_center)
        second_circle.rotate_around_point(self.alpha, self.ill_center)
        third_circle.rotate_around_point(self.alpha, self.ill_center)

        self.subject_response = third_circle_pos

        first_circle.draw(self.canvas, color=self.circles_outline[0],
                          fill=self.circles_fill[0], width=1)
        second_circle.draw(self.canvas, color=self.circles_outline[1],
                           fill=self.circles_fill[1], width=1)
        third_circle.draw(self.canvas, color=self.circles_outline[2],
                          fill=self.circles_fill[2], width=1)
        
        #Debug lines and circle
        if self.debug:
            self.line1 = Line(Vector2D(first_circle_pos.x + self.r_param, first_circle_pos.y + self.r_param), Vector2D(1, 0), self.d_param)
            self.line2 = Line(Vector2D(second_circle_pos.x + self.r_param, second_circle_pos.y + self.r_param), Vector2D(1, 0), self.d_param)

            self.line1.rotate_around_point(self.alpha, self.ill_center)
            self.line2.rotate_around_point(self.alpha, self.ill_center)

            self.canvas.create_line(self.line1.org.x, self.line1.org.y, self.line1.secn.x, self.line1.secn.y, fill='green', width=1)
            self.canvas.create_line(self.line2.org.x, self.line2.org.y, self.line2.secn.x, self.line2.secn.y, fill='black', width=1)

            self.debug_square = Circle(self.desired_point, 1)
            self.debug_square.rotate_around_point(self.alpha, self.ill_center)
            self.debug_square.draw(self.canvas, color='green', fill='green', width=1) 
        

        self.canvas.scale('all', 0, 0, 2, 2) # TODO: Look into how the elements are positioned, currently this is causing problems.

    def adjust_alpha(self, value):
        self.alpha = int(value)
    
    def adjust_d(self, value):
        self.d_param = int(value)
    
    def adjust_r(self, value):
        self.r_param = int(value)

    def adjust_circle(self, value):          
        self.draw_illusion(int(value))

    def submit_data(self):
        
        dpi = self.winfo_fpixels('1i')
        
        # Calculate the error in pixels and mm
        absolute_error = (self.desired_point - self.subject_response).magnitude()
        max_error_pixel = (self.desired_point - Vector2D(256 - self.r_param - 2, self.ill_center.y)).magnitude()
        
        absolute_error_mm = pixel_to_mm(absolute_error, dpi, 2) # 2 is a magic number, it is the scale of the illusion
        max_error_mm = pixel_to_mm(max_error_pixel, dpi, 2) # 2 is a magic number, it is the scale of the illusion

        try:
            db = databaseManager.Manager()
            db.saveMullerLyerResult(
                self.user_id, self.r_param, self.d_param, self.alpha,
                self.desired_point.x, self.desired_point.y,
                self.subject_response.x, self.subject_response.y,
                absolute_error, absolute_error_mm,
                max_error_pixel, max_error_mm)
            
        except Exception as e:
            print(f"An error occurred while trying to save the data\n{e}")
    
        # Generate a new illusion
        illusion = self.test_data.get_next_illusion()
        self.r_param = illusion.r_param
        self.d_param = illusion.d_param
        self.circles_fill = illusion.fill
        self.circles_outline = illusion.outline

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

    def times_up(self):
        # This function will be called when the timer ends
        messagebox.showinfo("Timer", "Time's up!")
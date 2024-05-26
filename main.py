import tkinter as tk
from functions import exit 
from gui import registerPage
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.show_frame(registerPage.registerGUI)

    def show_frame(self, context):
        frame = registerPage.registerGUI(self)
        frame.tkraise()





if __name__ == "__main__":
    app = App()
    
    app.title('Illusion Test')
    app.iconbitmap("./gui/res/logo.ico")

    # Make it resize to full screen, avoided using the fullscreen true parameter since we probable would want to use the width and height values as globals
    width = app.winfo_screenwidth()
    height = app.winfo_screenheight()
    app.geometry(f"{width}x{height}+0+0")
    app.state('zoomed')  # Maximize the window

    app.mainloop()

#TODO: SEPARATE THE GUI AND FUNCTIONS INTO SEPARATE FILES
#PS: TODO IS A LIE
#PPS: READ OVER 1 LINE ABOVE
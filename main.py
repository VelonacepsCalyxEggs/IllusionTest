import tkinter as tk
from gui import registerPage
import json
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.show_frame(registerPage.registerGUI)

        # check config
        with open('./resources/config/config.json', 'r') as f:
            # Read the file
            file_content = f.read()
            config = json.loads(file_content)
            self.debug = config["Debug"]

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

#TODO: DO
#! PS: TODO IS A LIE
#! PPS: READ OVER 1 LINE ABOVE
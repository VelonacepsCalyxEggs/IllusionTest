import tkinter as tk

def test_function():
    print('Button clicked!')

# Main window declaration or someshit idk I aint reading all that
root = tk.Tk()
root.title('Illusion Test')

# Make it resize to full screen, avoided using the fullscreen true parameter since we probable would want to use the width and height values as globals
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f"{width}x{height}+0+0")
root.state('zoomed')  # Maximize the window

label = tk.Label(root, text='Hello There!')
label.pack()

button = tk.Button(root, text='Click My Balls', command=test_function)
button.pack()

entry = tk.Entry(root)
entry.pack()

root.mainloop()

#TODO: SEPARATE THE GUI AND FUNCTIONS INTO SEPARATE FILES
#PS: TODO IS A LIE
#PPS: READ 27th LINE
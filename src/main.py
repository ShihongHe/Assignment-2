import tkinter as tk
import my_modules.GUI as GUI
import matplotlib
matplotlib.use('TkAgg')


if __name__ == '__main__':
    # Create a new Tkinter root window
    root = tk.Tk()
    # Create a new Tkinter root window
    root.geometry('1000x800+300+30')
    root.title('Site suitability')
    # Create an instance of the Application class and set it as the root window's content
    app = GUI.Application(master=root)
    root.protocol("WM_DELETE_WINDOW", app.exit)
    root.mainloop()

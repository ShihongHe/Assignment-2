import tkinter as tk
import GUI


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1000x800+300+30')
    root.title('Site suitability')
    app = GUI.Application(master=root)
    root.protocol("WM_DELETE_WINDOW", app.exit)
    root.mainloop()
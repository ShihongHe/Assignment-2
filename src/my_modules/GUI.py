import tkinter as tk
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import asksaveasfilename
from matplotlib import pyplot as plt
import matplotlib
import my_modules.io as io
import my_modules.raster as raster
import os
     
class Application(tk.Frame):
    """A tkinter application for visualizing and processing raster files"""

    def __init__(self, master=None):
        """
        Initializes the Application object

        Parameters
        ----------
        master : tkinter.Tk, optional
            The main tkinter window. The default is None.

        Returns
        -------
        None.

        """
        super().__init__(master)
        self.master = master
        self.pack()
        #The canvas that displays the raster images
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(master=self.master)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #A list of tkinter widgets displayed in the window
        self.widgets=[]
        #A list of tkinter widgets displayed in the window.
        self.scales=[]
        self.multiply=[]
        self.createWidget()
        
    def createWidget(self):
        """
        Creates the menus and bindings for the main tkinter window.

        Returns
        -------
        None.

        """
        # Create the main menu bar
        menubar = tk.Menu(self.master)

        # Create a submenu
        menuFile = tk.Menu(menubar)
        menuHelp = tk.Menu(menubar)

        # Adds submenu to the main menu bar
        menubar.add_cascade(label="File", menu=menuFile)
        menubar.add_cascade(label="Help", menu=menuHelp)

        # Add menu item
        menuFile.add_command(label='Show raster', accelerator='ctrl+s', command=self.openfile)
        menuFile.add_command(label="Visualise the suitability", accelerator='ctrl+v', command=self.suitability)
        menuFile.add_separator()  # Add a divider
        menuFile.add_command(label='Exit', accelerator='ctrl+e', command=self.exit)
        menuHelp.add_command(label='Readme', accelerator='ctrl+r', command=self.open_readme)
        # Add the main menu bar to the root window
        self.master['menu'] = menubar
        
        
        #Added shortcut key handling
        self.master.bind('<Control-s>',lambda event:self.openfile())
        self.master.bind('<Control-v>',lambda event:self.suitability())
        self.master.bind('<Control-e>',lambda event:self.exit())
        self.master.bind('<Control-r>',lambda event:self.open_readme())
        
    def openfile(self):
        """
        Prompts the user to select raster files to load and displays them on the canvas

        Returns
        -------
        None.

        """
        #Select file
        files=askopenfilenames()
        #File is empty error out of the loop
        while not files:
            tk.messagebox.showerror("Error", "Please select at least one file!")
            return
        #Determines if the component list is empty. If it is not empty, destroy all components
        if  self.widgets:
            self.destroy()
        #Create  raster objects from a list of files
        self.creatRaster(files)
        #Creat fig and axes
        fig, axes = plt.subplots(nrows=1, ncols=len(files), figsize=(18,6))
        #Create buttons 
        self.btn=tk.Button(self,text='Visualise the suitability',command=self.suitability)
        self.btn.grid(row=0,column=0)
        self.widgets.append(self.btn)
        self.plot(fig,axes)
        plt.close()
        
        
    def suitability(self,judge=True):
        """
        Displays a window with a slider for each loaded raster to adjust its weight, 
        and displays a final raster calculated as the weighted sum of the loaded rasters. 
        The user can add  rasters from the window.
        If the "judge" parameter is True, it prompts the user to select raster files to load.
        If the "judge" parameter is False, add the raster

        Parameters
        ----------
        judge : Boole, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        """
        #Follow the judge to determine whether to open the file for the first time or add the file
        if judge:
            #Select file
            files=askopenfilenames()
            #File is empty error out of the loop
            while not files:
                tk.messagebox.showerror("Error", "Please select at least one file!")
                return
            #Create  raster objects from a list of files
            self.creatRaster(files)
            #Count the number of files to determine the number of subgraphs
            self.number=len(files)+1
            
        #Determines if the component list is empty. If it is not empty, destroy all components
        if self.widgets:
            self.destroy()
            
        #Creat fig and axes
        fig, axes = plt.subplots(nrows=1, ncols=self.number, figsize=(18,6))
        
        #Create the corresponding number of label slider and input box according to the number of files, 
        #use grid to determine the placement position, and bind the corresponding function
        for i in range(len(self.raster_list)):
            var = tk.StringVar()
            self.label=tk.Label(self,text=self.raster_list[i].name)
            self.label.grid(row=i,column=0)
            self.scale = tk.Scale(self, from_=0, to=100, length=200, 
                             tickinterval=20, orient='horizontal',
                             command= lambda x , axes=axes: self.update(x, axes),
                             variable=var)
            self.scale.set(int(100/len(self.raster_list)))
            self.scale.grid(row=i, column=1)
            self.entry=tk.Entry(self, textvariable=var)
            self.entry.grid(row=i,column=2)
            self.entry.bind("<KeyRelease>", lambda event, axes=axes: self.update(self.entry.get(), axes))
            #Add the widgets to the list of scales and widgets
            self.scales.append( self.scale)
            self.widgets.append( self.label)
            self.widgets.append( self.entry)
        
        #Draw rasters
        self.plot(fig,axes,False)
        
        #Create buttons for saving text files, saving images, and adding data.
        self.btn1=tk.Button(self,text="Save Image",command=self.saveimage)
        self.btn1.grid(row=len(self.raster_list),column=0)
        self.btn2=tk.Button(self,text="Save File",command=self.savefile)
        self.btn2.grid(row=len(self.raster_list),column=1)
        self.btn3=tk.Button(self,text="Add",command=self.addfile)
        self.btn3.grid(row=len(self.raster_list),column=2)
        
        #Add the buttons to the list of widgets
        self.widgets.append(self.btn1)
        self.widgets.append(self.btn2)
        self.widgets.append(self.btn3)
        plt.close()
        
        
    def plot(self,fig,axes,judge=True):
        """
        Plots the loaded rasters on the canvas

        Parameters
        ----------
        fig : matplotlib.figure
            The matplotlib figure object that contains the canvas.
        axes : matplotlib.axes
            The matplotlib axes object of the canvas.
        judge : Boole, optional
            A flag. The default is True.

        Returns
        -------
        None.

        """
        #Destroy the canvas
        self.canvas.get_tk_widget().destroy()
        #Creat new canvas
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=self.master)
        self.canvas.get_tk_widget().forget()
        #Place canvas
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        #Determine the number of subgraphs to plot
        if len(self.raster_list)==1 & judge :
            axes.imshow(self.raster_list[0].environment)
            axes.set_title(self.raster_list[0].name)
        else:
            for i in range(len(self.raster_list)):
                axes[i].imshow(self.raster_list[i].environment)
                axes[i].set_title(self.raster_list[i].name)
        
    
    
    
    def creatRaster(self,files,judge=True):
        """
        Creates a Raster object for each file path in the "files" parameter and appends them to the raster_list attribute. 
        If the "judge" parameter is True, it empties the raster_list before appending the new rasters.

        Parameters
        ----------
        files : list
            A list of filenames  to create a Raster object from..
        judge : Boole, optional
            A flag indicating whether to clear any previously created Raster objects. The default is True.

        Returns
        -------
        None.

        """
        #Clear the list the first time a raster object is created. Add files are added directly to the original list
        if judge:
            self.raster_list=[]
        for i in range(len(files)):
            #read data
            data=io.read_data(files[i])
            file_name = files[i].split('/')[-1].split('.')[0]
            #The instantiated raster object is stored in the list
            self.raster_list.append(raster.Raster(data, file_name))
            
            
    def update(self,value, axes):
        """
        Calculates the new raster based on the updated weights of each raster and updates the 
        canvas display accordingly.

        Parameters
        ----------
        value : str
            The new weight value of the updated raster.
        axes : matplotlib.axes
            The matplotlib axes object of the canvas.

        Returns
        -------
        None.

        """
        self.multiply=[]     
        for i in range(len(self.raster_list)):
            #multiply each raster by its corresponding weight and store it in Multiply
            self.multiply.append(self.raster_list[i].multiply(self.scales[i].get() * 0.01))
        #Add up all the rasters
        self.new=raster.Raster.add_rasters(self.multiply)
        
        #normalization
        self.new.normalize()
        # Display the normalized image
        axes[-1].clear()
        axes[-1].imshow(self.new.environment)
        axes[-1].set_title('Site suitability')
        self.canvas.draw()
        
    
    def destroy(self):
        """
        Destroys all tkinter widgets

        Returns
        -------
        None.

        """
        #destroy  widget
        for widget in self.widgets:
            widget.destroy()
        for scale in self.scales:
            scale.destroy()
        #Clear the list
        self.widgets=[]
        self.scales=[]
        
        
    def savefile(self):
        """
        Prompts the user to select a file to save the processed raster as a text file.

        Returns
        -------
        None.

        """
        #Select the file to save the file
        self.filename = asksaveasfilename(title='Save as', initialdir='unnamed.txt',
                                          filetypes=[('txt', '*.txt')],
                                          defaultextension='.txt')
        #write data
        io.write_data(self.filename, self.new.environment)
                
        
    def saveimage(self):
        """
        Prompts the user to select a file to save the processed raster as a JPEG image

        Returns
        -------
        None.

        """
        #Select the file to save the file
        self.filename = asksaveasfilename(title='Save as', initialdir='unnamed.jpg',
                                          filetypes=[('jpg', '*.jpg')],
                                          defaultextension='.jpg')
        #save jpg
        plt.imshow(self.new.environment)
        plt.savefig(self.filename)
        
    def addfile(self):
        """
        Prompts the user to select additional raster files to load and adds them to the window

        Returns
        -------
        None.

        """
        #Select file
        files=askopenfilenames()
        #File is empty error out of the loop
        while not files:
            tk.messagebox.showerror("Error", "Please select at least one file!")
            return
        
        #Create  raster objects from a list of files
        self.creatRaster(files,False)
        #Count the number of files to determine the number of subgraphs
        self.number+=len(files)
        #Add component to draw image
        self.suitability(False)
        
        

    def exit(self):
        """
        Closes the tkinter window and quits the application

        Returns
        -------
        None.

        """
        #quit
        self.master.quit()
        self.master.destroy()
        
    def open_readme(self):
        """
        Opens the README.md file in the default system text editor

        Returns
        -------
        None.

        """
        #open README.md
        os.startfile('..\README.md')


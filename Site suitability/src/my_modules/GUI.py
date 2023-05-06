import tkinter as tk
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import asksaveasfilename
from matplotlib import pyplot as plt
import matplotlib
import my_modules.io as io
import my_modules.raster as raster
import os
     
class Application(tk.Frame):

    def __init__(self, master=None):
        """
        

        Parameters
        ----------
        master : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        super().__init__(master)
        self.master = master
        self.pack()
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(master=self.master)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.widgets=[]
        self.scales=[]
        self.multiply=[]
        self.createWidget()
        
    def createWidget(self):
        # 创建主菜单栏
        menubar = tk.Menu(self.master)

        # 创建子菜单
        menuFile = tk.Menu(menubar)
        menuHelp = tk.Menu(menubar)

        # 将子菜单加入到主菜单栏
        menubar.add_cascade(label="File", menu=menuFile)
        menubar.add_cascade(label="Help", menu=menuHelp)

        # 添加菜单项
        menuFile.add_command(label='Show raster', accelerator='ctrl+s', command=self.openfile)
        menuFile.add_command(label="Visualise the suitability", accelerator='ctrl+v', command=self.suitability)
        menuFile.add_separator()  # 添加分割线
        menuFile.add_command(label='Exit', accelerator='ctrl+e', command=self.exit)
        menuHelp.add_command(label='Readme', accelerator='ctrl+r', command=self.open_readme)
        # 将主菜单栏加到根窗口
        self.master['menu'] = menubar
        
        
        #增加快捷键的处理
        self.master.bind('<Control-s>',lambda event:self.openfile())
        self.master.bind('<Control-v>',lambda event:self.suitability())
        self.master.bind('<Control-e>',lambda event:self.exit())
        self.master.bind('<Control-r>',lambda event:self.open_readme())
        
        
    def suitability(self,judge=True):
        if judge:
            files=askopenfilenames()
            while not files:
                tk.messagebox.showerror("Error", "Please select at least one file!")
                
                return
            self.creatRaster(files)
            self.number=len(files)+1
        if self.widgets:
            self.destroy()
        fig, axes = plt.subplots(nrows=1, ncols=self.number, figsize=(18,6))
        
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
            self.scales.append( self.scale)
            self.widgets.append( self.label)
            self.widgets.append( self.entry)
            
        self.plot(fig,axes,False)
        self.btn1=tk.Button(self,text="Save Image",command=self.saveimage)
        self.btn1.grid(row=len(self.raster_list),column=0)
        self.btn2=tk.Button(self,text="Save File",command=self.savefile)
        self.btn2.grid(row=len(self.raster_list),column=1)
        self.btn3=tk.Button(self,text="Add",command=self.addfile)
        self.btn3.grid(row=len(self.raster_list),column=2)
        self.widgets.append(self.btn1)
        self.widgets.append(self.btn2)
        self.widgets.append(self.btn3)
        plt.close()
        
    
            
    def update(self,value, axes):
        self.multiply=[]     
        for i in range(len(self.raster_list)):
            self.multiply.append(self.raster_list[i].multiply(self.scales[i].get() * 0.01))
        self.new=raster.Raster.add_rasters(self.multiply)
        self.new.normalize()
        axes[-1].clear()
        axes[-1].imshow(self.new.environment)
        axes[-1].set_title('Site suitability')
        self.canvas.draw()
        

        
    def plot(self,fig,axes,judge=True):
        
        self.canvas.get_tk_widget().destroy()
        
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=self.master)
        self.canvas.get_tk_widget().forget()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        if len(self.raster_list)==1 & judge :
            axes.imshow(self.raster_list[0].environment)
            axes.set_title(self.raster_list[0].name)
        else:
            for i in range(len(self.raster_list)):
                axes[i].imshow(self.raster_list[i].environment)
                axes[i].set_title(self.raster_list[i].name)
        
    
    def openfile(self):
        
        files=askopenfilenames()
        while not files:
            tk.messagebox.showerror("Error", "Please select at least one file!")
            return
        if  self.widgets:
            self.destroy()
        self.creatRaster(files)
        fig, axes = plt.subplots(nrows=1, ncols=len(files), figsize=(18,6))
        self.btn=tk.Button(self,text='Visualise the suitability',command=self.suitability)
        self.btn.grid(row=0,column=0)
        self.widgets.append(self.btn)
        self.plot(fig,axes)
        plt.close()
    
    def creatRaster(self,files,judge=True):
        if judge:
            self.raster_list=[]
        for i in range(len(files)):
            data=io.read_data(files[i])
            file_name = files[i].split('/')[-1].split('.')[0]
            self.raster_list.append(raster.Raster(data, file_name))
    
    def destroy(self):
        for widget in self.widgets:
            widget.destroy()
        for scale in self.scales:
            scale.destroy()
        self.widgets=[]
        self.scales=[]
        
        
    def savefile(self):
        self.filename = asksaveasfilename(title='Save as', initialdir='unnamed.txt',
                                          filetypes=[('txt', '*.txt')],
                                          defaultextension='.txt')
        io.write_data(self.filename, self.new.environment)
                
        
    def saveimage(self):
        self.filename = asksaveasfilename(title='Save as', initialdir='unnamed.jpg',
                                          filetypes=[('jpg', '*.jpg')],
                                          defaultextension='.jpg')
        plt.imshow(self.new.environment)
        plt.savefig(self.filename)
        
    def addfile(self):
        files=askopenfilenames()
        while not files:
            tk.messagebox.showerror("Error", "Please select at least one file!")
            return
        self.creatRaster(files,False)
        self.number+=len(files)
        self.suitability(False)

    def exit(self):
        self.master.quit()
        self.master.destroy()
        
    def open_readme(self):
        os.startfile('..\..\..\README.md')

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1000x800+300+30')
    root.title('Site suitability')
    app = Application(master=root)
    root.protocol("WM_DELETE_WINDOW", app.exit)
    root.mainloop()

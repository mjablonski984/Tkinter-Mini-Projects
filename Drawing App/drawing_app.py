from tkinter import *
from tkinter import ttk, filedialog, colorchooser
import PIL
from PIL import ImageGrab, ImageTk, Image


class main:
    def __init__(self,master):
        self.master = master
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.old_x = None
        self.old_y = None
        self.penwidth = 5
        self.penwidth_var = StringVar()
        self.capstyle = 'round'
        self.capstyle_var = StringVar(value=self.capstyle)
        self.drawWidgets()
        
        self.c.bind('<B1-Motion>',self.paint)
        self.c.bind('<ButtonRelease-1>',self.reset)
        


    def paint(self,e):
        if self.old_x and self.old_y:
            # create_line(x-start,y-start,x-end,y-end)
            self.c.create_line(self.old_x, self.old_y, e.x, e.y, width=self.penwidth, fill=self.color_fg, capstyle=self.capstyle, smooth=True)
        # set old(start position to curent mouse position to draw continuous line  )
        self.old_x = e.x
        self.old_y = e.y
    
    
    # Stop drawing when mouse btn is released
    def reset(self,e):
        self.old_x = None
        self.old_y = None


    # Clear canvas
    def clear(self):
        self.c.delete(ALL)


    # Change pen width
    def change_width(self,e):
        self.penwidth = int(float(e))
        # Set the StringVar to update a label text
        self.penwidth_var.set(self.penwidth)


   # Change pen cap
    def change_cap(self):
        self.capstyle = self.capstyle_var.get()


    # Save created image to a file
    def save(self):
        file = filedialog.asksaveasfilename(filetypes=[('PNG','.png')])
        if file:
            # get the position of upper left corner of a canvas, and its height & width 
            x = self.master.winfo_rootx() + self.c.winfo_x()
            y = self.master.winfo_rooty() + self.c.winfo_y()
            x1 = x + self.c.winfo_width()
            y1 = y + self.c.winfo_height()
            # grab the position of a canvas and save its content to a image file
            PIL.ImageGrab.grab().crop((x,y,x1,y1)).save(file + '.png')


    # Open image file
    def open(self):
        file = filedialog.askopenfilename(filetypes=[('JPG, PNG','*.png *.jpg')])
        if file:
            img = Image.open(file)         
            self.c.image = ImageTk.PhotoImage(img)
            self.c.create_image(0,0, anchor=NW, image=self.c.image)

    
    # Change pen color
    def change_fg(self):
        self.color_fg = colorchooser.askcolor(color=self.color_fg)[1]
        self.color.config(bg=self.color_fg)


    # Change background color
    def change_bg(self):
        # Picks hex value of a color, (color arg. sets the selected color when colorpicker opens)
        self.color_bg = colorchooser.askcolor(color=self.color_bg)[1]
        self.c['bg'] = self.color_bg


    # Draw an app
    def drawWidgets(self):
        # Create a toolbar frame
        self.controls = Frame(self.master, padx=5, pady=5, bg='#F5FFFA')
        Label(self.controls, text='Pen Width:', font=('',14), bg='#F5FFFA' ).grid(row=0, column=0, padx=(20,0))
        self.slider = ttk.Scale(self.controls, from_=5, to=100, command=self.change_width, orient=HORIZONTAL)
        self.slider.set(self.penwidth)
        self.slider.grid(row=0, column=1, ipadx=30)
        Label(self.controls, textvariable=self.penwidth_var, font=('',14), bg='#F5FFFA' ).grid(row=0, column=2)

        Label(self.controls, text='Pen Type:', font=('',14), bg='#F5FFFA' ).grid(row=0, column=3, padx=(20,0))
        self.cap1 = Radiobutton(self.controls, text="Round", variable=self.capstyle_var, value='round', command=self.change_cap, bg='#F5FFFA')
        self.cap1.grid(row=0, column=4)
        self.cap2 = Radiobutton(self.controls, text="Projecting", variable=self.capstyle_var, value='projecting', command=self.change_cap, bg='#F5FFFA')
        self.cap2.grid(row=0, column=5)
        self.cap3 = Radiobutton(self.controls, text="Butt", variable=self.capstyle_var, value='butt', command=self.change_cap, bg='#F5FFFA')
        self.cap3.grid(row=0, column=6)
        
        Label(self.controls, text='Color:', font=('',14), bg='#F5FFFA' ).grid(row=0, column=7, padx=(20,0))
        self.color = Button(self.controls, width=5, bg=self.color_fg, command=self.change_fg, relief=GROOVE)
        self.color.grid(row=0, column=8)
        
        self.controls.pack(fill=X)

        # Create Canvas widget
        self.c = Canvas(self.master, width=800, height=600, bg=self.color_bg)
        self.c.pack(fill=BOTH, expand=True)

        # Create main menu, add submenus and menu items
        menu = Menu(self.master)
        self.master.config(menu=menu)

        filemenu = Menu(menu, tearoff=False)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='Open File', command=self.open)
        filemenu.add_separator()
        filemenu.add_command(label='Save File', command=self.save)
        
        colormenu = Menu(menu, tearoff=False)
        menu.add_cascade(label='Colors', menu=colormenu)
        colormenu.add_command(label='Brush Color', command=self.change_fg)
        colormenu.add_command(label='Background Color', command=self.change_bg)

        optionmenu = Menu(menu, tearoff=False)
        menu.add_cascade(label='Options', menu=optionmenu)
        optionmenu.add_command(label='Clear Canvas', command=self.clear)
        optionmenu.add_separator() #separator line
        optionmenu.add_command(label='Exit', command=self.master.destroy)



# Create tkinter window object and pass it to a main class, and start the main loop
if __name__=='__main__':
    root = Tk()
    main(root)
    root.title('TK painter')
    root.minsize(800, 600)
    root.iconbitmap('icon.ico')
    root.mainloop()
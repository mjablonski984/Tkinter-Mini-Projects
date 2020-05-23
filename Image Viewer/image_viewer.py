from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import os


class ImageViewer:
    def __init__(self, master):
        self.master = master
        self.master.title('Image Viewer')
        self.master.iconbitmap('icon.ico')
        self.master.minsize(960,560)
        
        self.c_size = (960,560)
        self.img = None
        self.imgs_list = []
        self.img_num = 0
        self.create_gui()

        self.master.bind('<Left>', lambda e: self.back())
        self.master.bind('<Right>', lambda e: self.forward())
        
        self.canvas.bind('<Configure>', self.on_resize)
    


    # Change size of images
    def on_resize(self,event):
        try:
            # Get current size of canvas
            self.c_size = (event.width,event.height -20)
            # If image is loaded : get it's path by cutting it from status and recreate image, else load default text
            if len(self.imgs_list) >= 1:
                self.create_image(self.status['text'].replace('Current Image: ',''))
            else:
                self.create_text()
        except Exception as e:
            print(f'Error: {e}')
        


    def create_gui(self):
        # Canvas
        self.canvas = Canvas(self.master, height=self.c_size[1],width=self.c_size[0],
			bg='black',  highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        # Display text if no image selected
        self.create_text()

        # Image path bar on the bottom
        self.status=Label(self.master,text = 'Current Image: None', bg='#7e8989', fg='white', bd=0,
            padx=10, pady=5, font=('Verdana',12),  relief='sunken',anchor=W)
        self.status.pack(side=BOTTOM,fill=X)
        
        # Controls bar
        self.controls = Frame(self.master, bg='#7e8989', padx=10, pady=5)
        
        Button(self.controls, text="Image", bd=0, fg='white', bg='#4b4a67', font=('Verdana',14)
			,command=self.open_file, activebackground='white', activeforeground='#4b4a67').pack(side=LEFT)
        Button(self.controls, text="Folder", bd=0, fg='white', bg='#4b4a67', font=('Verdana',14)
			,command=self.open_folder, activebackground='white', activeforeground='#4b4a67').pack(side=LEFT,padx=(10,0))

        self.arrows = Frame(self.controls, bg='#7e8989')
        self.btn_back = Button(self.arrows, text='<<', bd=0, fg='white', bg='#4b4a67', font=('Verdana',14)
            , command=self.back, activebackground='white', activeforeground='#4b4a67')
        self.btn_back.pack(side=LEFT)
        self.btn_forward = Button(self.arrows, text='>>', bd=0, fg='white', bg='#4b4a67', font=('Verdana',14)
            , command=self.forward, activebackground='white', activeforeground='#4b4a67')
        self.btn_forward.pack(side=LEFT, padx=(10,0))
        self.arrows.pack(side=LEFT, fill='none', expand=True)

        self.img_num_label = Label(self.controls, text=f'Image {self.img_num} of {len(self.imgs_list)}', 
            font=('Verdana',12), fg='white', bg='#7e8989', anchor=E)
        self.img_num_label.pack(side=RIGHT)
        self.controls.pack(side=BOTTOM,fill=X)

    
    def create_text(self):
        self.canvas.delete(ALL)
        self.canvas.create_text(self.c_size[0]/2, self.c_size[1]/2, text='No image', font=('Verdana',28), fill='white')


    def create_image(self, file):
        try:
            self.pilImage = Image.open(file)
            self.img = ''

            if( (self.pilImage.size[0] > self.c_size[0]) or (self.pilImage.size[1] > self.c_size[1]) ):
                # Scale down if image is bigger than canvas
                resize=self.pilImage.resize((self.c_size[0],self.c_size[1]),Image.ANTIALIAS)
                self.img = ImageTk.PhotoImage(resize)
            else:
                self.img = ImageTk.PhotoImage(self.pilImage)
                
            # Clear canvas
            self.canvas.delete(ALL)
			# Create new image
            self.canvas.create_image(self.c_size[0]/2+10, self.c_size[1]/2+10, anchor=CENTER, image=self.img)
			# Update image path bar
            self.status['text']='Current Image: '+file
            
        except Exception as e:
            print(f'Error: {e}')
            self.create_text()


    def open_file(self):
        try:
            self.imgs_list = []
            # Open single image and add to a list
            file = fd.askopenfilename(filetypes=[('Images','*.png *.jpg *.gif')])
            self.imgs_list=[file]
            # Update image number counter and 
            self.img_num = 1
            self.img_num_label.config(text=f'Image {self.img_num} of {len(self.imgs_list)}')
            # Create new image
            self.create_image(self.imgs_list[0])
        except Exception as e:
            print(f'Error: {e}')


    def open_folder(self):
        try:
            directory = fd.askdirectory()
            # Open directory and  if files inside match given extensions, add to the file list
            if directory:
                self.imgs_list = []
                extensions = ['png', 'jpg', 'jpeg', 'gif']
                for fn in os.listdir(directory):
                    if any(fn.lower().endswith(ext) for ext in extensions):
                        self.imgs_list.append(directory + '/' + fn)
                # If list isn't empty update img number and img number label
                if len(self.imgs_list) >= 1:
                    self.img_num = 1
                    self.img_num_label.config(text=f'Image {self.img_num} of {len(self.imgs_list)}')
                    # Create new image
                    self.create_image(self.imgs_list[0])
                else:
                    self.create_text()
                    self.status['text']='Current Image: None'
        except Exception as e:
            print(f'Error: {e}')


    def forward(self):
        if len(self.imgs_list ) <= 1:
            return
        if self.img_num > len(self.imgs_list ) - 1:
            self.img_num = 0
        # Create image, increment img number and update img number label
        self.create_image(self.imgs_list[self.img_num])
        self.img_num += 1
        self.img_num_label.config(text=f'Image {self.img_num} of {len(self.imgs_list)}')

    
    def back(self):
        if len(self.imgs_list ) <= 1:
            return
        if self.img_num <= 1:
            self.img_num = len(self.imgs_list ) + 1

        self.img_num -= 1
        self.create_image(self.imgs_list[self.img_num - 1])
        self.img_num_label.config(text=f'Image {self.img_num } of {len(self.imgs_list)}')

        


root = Tk()

ImageViewer(root)

root.mainloop()
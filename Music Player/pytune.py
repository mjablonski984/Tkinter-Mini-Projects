import os
import time
import threading
from tkinter import *
from tkinter import messagebox, filedialog
from pygame import mixer
from mutagen.mp3 import MP3


class Menubar:

    def __init__(self, parent):
    
        menubar = Menu(parent.master)
        parent.master.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open", command=parent.browse_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.master.destroy)

        aboutmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=aboutmenu)
        aboutmenu.add_command(label="About Us", command=self.about_us)

    def about_us(self):
        messagebox.showinfo('About PyTune', 'A simple music player created with Python and Tkinter')

        

class PyTune:

    def __init__(self, master):
        master.title("PyTune")
        master.iconbitmap("images/icon.ico")
        
        self.master = master
        
        # initialize music mixer from pygame module
        mixer.init() 

        self.filename_path = ''
        self.playlist = []
        self.paused = False
        self.muted = False

        self.menubar = Menubar(self)        
        self.create_gui()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.config(bg="#f1f2f6")
        self.master.winfo_children()



    def create_gui(self):
        # status bar
        self.statusbar = Label(self.master, text="Welcome to PyTune", relief=SUNKEN, anchor=W, bg="#f1f2f6", fg="#000")
        self.statusbar.pack(side=BOTTOM, fill=X)

        # left frame - playlist
        left_frame = Frame(root, bg="#f1f2f6")
        left_frame.pack(side=LEFT, padx=20)

        self.playlistbox = Listbox(left_frame, font=("Verdana, 10"), width=30, bg="#F8F8FF")
        self.playlistbox.pack()
        
        self.add_img = PhotoImage(file='images/add.png')
        add_btn = Button(left_frame, image=self.add_img, command=self.browse_file,
                 bg="#f1f2f6",activebackground="#f1f2f6", borderwidth=0)
        add_btn.pack(side=LEFT, fill=X, expand=1)
        self.del_img = PhotoImage(file='images/del.png')
        del_btn = Button(left_frame, image=self.del_img, command=self.del_song,
                 bg="#f1f2f6",activebackground="#f1f2f6", borderwidth=0)
        del_btn.pack(side=RIGHT, fill=X, expand=1)
        
        # right frame - controls
        rightframe = Frame(root, bg="#f1f2f6")
        rightframe.pack()

        topframe = Frame(rightframe, bg="#f1f2f6")
        topframe.pack()

        self.lengthlabel = Label(topframe, text='Total Length : --:--', bg="#f1f2f6", fg="#000", font=("Verdana, 10"))
        self.lengthlabel.pack(side=LEFT, pady=(20,0), padx=10)

        self.currenttimelabel = Label(topframe, text='Current Time : --:--', bg="#f1f2f6", fg="#000", font=("Verdana, 10"))
        self.currenttimelabel.pack(side=LEFT, pady=(20,0), padx=10)

        middleframe = Frame(rightframe, bg="#f1f2f6")
        middleframe.pack(pady=30, padx=30)

        self.rewind_img = PhotoImage(file='images/rewind.png')
        self.rewind_btn = Button(middleframe, image=self.rewind_img, command=self.rewind_music,
                         borderwidth=0, bg="#f1f2f6",activebackground="#f1f2f6")
        self.rewind_btn.grid(row=0, column=0, padx=5)

        self.play_img = PhotoImage(file='images/play.png')
        self.play_btn = Button(middleframe, image=self.play_img, command=self.play_music, 
                        borderwidth=0, bg="#f1f2f6",activebackground="#f1f2f6")
        self.play_btn.grid(row=0, column=1, padx=5)

        self.stop_img = PhotoImage(file='images/stop.png')
        self.stop_btn = Button(middleframe, image=self.stop_img, command=self.stop_music, 
                        borderwidth=0, bg="#f1f2f6",activebackground="#f1f2f6")
        self.stop_btn.grid(row=0, column=2, padx=5)

        self.pause_img = PhotoImage(file='images/pause.png')
        self.pause_btn = Button(middleframe, image=self.pause_img, command=self.pause_music, 
                        borderwidth=0, bg="#f1f2f6",activebackground="#f1f2f6")
        self.pause_btn.grid(row=0, column=3, padx=5)

        bottomframe = Frame(rightframe, bg="#f1f2f6")
        bottomframe.pack()
        self.mute_img = PhotoImage(file='images/mute.png')
        self.volume_img = PhotoImage(file='images/volume.png')
        self.volume_btn = Button(bottomframe, image=self.volume_img, command=self.mute_music,
                         borderwidth=0, bg="#f1f2f6",activebackground="#f1f2f6")
        self.volume_btn.grid(row=0, column=1)

        self.scale = Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=self.set_vol,
                    sliderrelief=FLAT, bd=0, bg="#f1f2f6", troughcolor="#121212")
        self.scale.set(70)  # set the default value of scale when music player starts
        mixer.music.set_volume(0.7)
        self.scale.grid(row=0, column=2, pady=15, padx=30)


    # display details about song
    def show_details(self, play_song):
        file_data = os.path.splitext(play_song)

        if file_data[1] == '.mp3':
            audio = MP3(play_song)
            total_length = audio.info.length
        else:
            a = mixer.Sound(play_song)
            total_length = a.get_length()
        # div - total_length/60, mod - total_length % 60
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        #  format string - display 0 for mins or secs if < 10
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        self.lengthlabel['text'] = f"Total Length {timeformat}"
        # use threading to run while loop every sec when song is playing
        t1 = threading.Thread(target=self.start_count, args=(total_length,))
        t1.start()

    
    # mixer.music.get_busy() - Returns FALSE when stop btn in pressed - allowing to stop the counter
    def start_count(self, t):
        current_time = 0
        while current_time <= t and mixer.music.get_busy():
            # pause counter when pause btn is pressed
            if self.paused:
                continue
            else:
                # get and format song time: mins -secs
                mins, secs = divmod(current_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                self.currenttimelabel['text'] = f"Current Time {timeformat}"
                # delay execution by 1sec and add i sec to the counter
                time.sleep(1)
                current_time += 1


    def play_music(self):
        if self.paused:
            mixer.music.unpause()
            self.statusbar['text'] = "Music Resumed"
            self.paused = False
        else:
            try:
                # stop the music and play new song after 1 sec (same time as iteration se set in )
                self.stop_music()
                time.sleep(1)
                selected_song = self.playlistbox.curselection()
                selected_song = int(selected_song[0])
                play_it = self.playlist[selected_song]
                mixer.music.load(play_it)
                mixer.music.play()
                self.statusbar['text'] = f"Playing music {os.path.basename(play_it)}"
                self.show_details(play_it)
            except:
                messagebox.showerror('File not found', 'File not found. Please try again.')


    def pause_music(self):
        self.paused = True
        mixer.music.pause()
        self.statusbar['text'] = "Music Paused"

    
    def stop_music(self):
        mixer.music.stop()
        self.statusbar['text'] = "Music Stopped"


    def rewind_music(self):
        self.play_music()
        self.statusbar['text'] = "Music Rewinded"


    # set_volume of mixer (takes value from 0 to 1).
    def set_vol(self, val):
        volume = int(val) / 100
        mixer.music.set_volume(volume)


    def mute_music(self):
        if  self.muted:
            mixer.music.set_volume(0.7)
            self.volume_btn.configure(image=self.volume_img)
            self.scale.set(70)
            self.muted = False
        else:
            mixer.music.set_volume(0)
            self.volume_btn.configure(image=self.mute_img)
            self.scale.set(0)
            self.muted = True


    # stop music and threading before closing app 
    def on_closing(self):
        self.stop_music()
        self.master.destroy()


    def browse_file(self):
        self.filename_path = filedialog.askopenfilename()
        self.add_to_playlist(self.filename_path)


    def add_to_playlist(self, filename):
        filename = os.path.basename(filename)
        index = 0
        self.playlistbox.insert(index, filename)
        self.playlist.insert(index, self.filename_path)
        index += 1
    

    def del_song(self):
        try:
            selected_song = self.playlistbox.curselection()
            selected_song = int(selected_song[0])
            self.playlistbox.delete(selected_song)
            self.playlist.pop(selected_song)
        except IndexError as e:
            print(e)




if __name__ == "__main__":
    root = Tk()
    PyTune(root)
    root.mainloop()
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from tkfontchooser import askfont


class Menubar:

    def __init__(self, parent):
        font_specs = ("", 10)

        menubar = tk.Menu(parent.master, font=font_specs)
        parent.master.config(menu=menubar)

        # file
        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        menubar.add_cascade(label="File", menu=file_dropdown)
        file_dropdown.add_command(label="New File", accelerator="Ctrl+N", command=parent.new_file)
        file_dropdown.add_command(label="Open File", accelerator="Ctrl+O", command=parent.open_file)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Save", accelerator="Ctrl+S", command=parent.save)
        file_dropdown.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=parent.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Exit", command=parent.quit)
        
        # settings
        settings_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_dropdown)
        settings_dropdown.add_command(label="Font" , accelerator="Ctrl+Shift+F", command=parent.set_font)
        settings_dropdown.add_separator()
        settings_dropdown.add_command(label="Text Color",accelerator="Ctrl+Shift+C",command=parent.set_color)
        
        # themes submenu
        theme_subm = tk.Menu(settings_dropdown, font=font_specs, tearoff=0)
        settings_dropdown.add_cascade(label="Change theme", menu=theme_subm)
        theme_subm.add_command(label='Dark', command=lambda: parent.set_theme('#231f20','#efe6dd'))
        theme_subm.add_command(label='Dark blue', command=lambda: parent.set_theme('#003049','#eae2b7'))
        theme_subm.add_command(label='Dark green', command=lambda: parent.set_theme('#02040f','#73a942'))
        theme_subm.add_command(label='Dark gold', command=lambda: parent.set_theme('#02040f','#ffb627'))
        theme_subm.add_separator()
        theme_subm.add_command(label='White (Default)', command=lambda: parent.set_theme('white','black'))
        theme_subm.add_command(label='Light blue', command=lambda: parent.set_theme('#e4e4e4','#3797a4'))
        
        # about
        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        menubar.add_cascade(label="About", menu=about_dropdown)
        about_dropdown.add_command(label="Release Notes", command=self.show_release_notes)
        about_dropdown.add_separator()
        about_dropdown.add_command(label="About", command=self.show_about_message)

    
    def show_about_message(self):
        box_title = "About Notepy"
        box_message = "A simple Python Text Editor"
        messagebox.showinfo(box_title, box_message)

    
    def show_release_notes(self):
        box_title = "Release Notes"
        box_message = "Version 0.1"
        messagebox.showinfo(box_title, box_message)



class Statusbar:

    def __init__(self, parent):

        font_specs = ("", 10)
        # Set stringVar for status label
        self.status = tk.StringVar()
        self.status.set("Notepy")

        label = tk.Label(parent.textarea, textvariable=self.status, fg="black",
                         bg="lightgrey", anchor='sw', font=font_specs)
        label.pack(side=tk.BOTTOM, fill=tk.BOTH)
    
    
     # Update status bar (*agrs passed for keybord events)
    def update_status(self, *args):
        if isinstance(args[0], bool):
            self.status.set("Your File Has Been Saved!")
        else:
            self.status.set("Notepy - version 0.1")




class Notepy:
    def __init__(self, master):
        master.title("Untitled - Notepy")
        master.geometry("1200x700")

        self.font_specs = ("vardana", 15)

        self.master = master
        self.filename = None
        # run quit function when clicked on close window btutton
        self.master.protocol("WM_DELETE_WINDOW",self.quit)

        self.textarea = tk.Text(master, font=self.font_specs)
        # vertical scrollbar
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)
        self.bind_shortcuts()


    # Set font
    def set_font(self, *args):
        font = askfont(self.master)
        if font:
            font['family'] = font['family'].replace(' ', '\ ')
            font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
            if font['underline']:
                font_str += ' underline'
            if font['overstrike']:
                font_str += ' overstrike'
            self.textarea['font'] = font_str


    # Set text color
    def set_color(self, *args):
        color = colorchooser.askcolor('black')
        if color:
            self.textarea['fg'] = color[1]
            
    
    # Set color theme
    def set_theme(self, bg, fg):
        self.textarea['insertbackground'] =  fg
        self.textarea['bg'] = bg
        self.textarea['fg'] = fg


    # Set the document title in the window
    def set_window_title(self, name=None):
        if name:
            self.master.title(name + " - Notepy")
        else:
            self.master.title("Untitled - Notepy")


    # Create new file
    def new_file(self, *args):
        if self.filename:
            if messagebox.askyesno("Save","Do you want to save the file before closing?"):
                self.save()
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()

    
    # Open existing file
    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"),
                       ("Text Files", "*.txt"),
                       ("HTML Documents", "*.html"),
                       ("CSS Documents", "*.css"),
                       ("Markdown Documents", "*.md"),
                       ("Python Files", "*.py"),
                       ("JavaScript Files", "*.js")])

        if self.filename:
            # close previous opened file and open new file
            self.textarea.delete(1.0, tk.END)
            with open(self.filename, "r") as f:
                self.textarea.insert(1.0, f.read())
                # update the title name
            self.set_window_title(self.filename)



    # Save to existing file
    def save(self, *args):
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filename, "w") as f:
                    f.write(textarea_content)
                # Display message in status bar by passing True to update_status
                self.statusbar.update_status(True)
            except Exception as e:
                print(e)
        else:
        # if file hasn't been created (filename=None) create new file
            self.save_as()


    # Create new file and save current element
    def save_as(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile="Untitled.txt",
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"),
                        ("Text Files", "*.txt"),
                        ("Python Scripts", "*.py"),
                        ("Markdown Documents", "*.md"),
                        ("JavaScript Files", "*.js"),
                        ("HTML Documents", "*.html"),
                        ("CSS Documents", "*.css")])
            textarea_content = self.textarea.get(1.0, tk.END)
            with open(new_file, "w") as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
            self.statusbar.update_status(True)
        except Exception as e:
            print(e)

    
    # Ask to save curretly opened file and close editor
    def quit(self):
        if (len(self.textarea.get(1.0, tk.END))) > 1:
            if messagebox.askyesno("Save","Do you want to save the file before closing?"):
                self.save()
        quit()


    def bind_shortcuts(self):
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-S>', self.save_as)
        self.textarea.bind('<Control-F>', self.set_font)
        self.textarea.bind('<Control-C>', self.set_color)
        self.textarea.bind('<Key>', self.statusbar.update_status)


if __name__ == "__main__":
    master = tk.Tk()
    np = Notepy(master)
    master.mainloop()
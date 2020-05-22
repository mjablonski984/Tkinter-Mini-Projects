from tkinter import *
import math

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title('Calculator')
        self.master.geometry('500x600')
        self.master.resizable(False, False)
        self.colors = {'dark': '#141414', 'med': '#212121'}        
        
        self.equation = ''
        self.paint_widgets()  



    # Create and position screen text widget and button grid
    def paint_widgets(self):         
        self.screen = Text(self.master, height=1, bd=0, pady=50, padx=5, fg='#fff', bg=self.colors['dark'], font=('Helvetica',32),
                state='disabled', selectbackground=self.colors['dark'], inactiveselectbackground=self.colors['dark'])
        self.screen.grid(row=0, column=0, columnspan=5, sticky=W+E+N+S)

        # make columns and rows stick to each other, fill entire remaining space and prevents overflow beyond window
        for x in range(1,5):
            self.master.columnconfigure(x, weight=1)
            self.master.rowconfigure(x, weight=1)    

        self.buttons = [
        [
        self.create_button(7),
        self.create_button(8),
        self.create_button(9),
        self.create_button('/'),
        self.create_button('DEL', None)       
        ],[
        self.create_button(4),
        self.create_button(5),
        self.create_button(6),
        self.create_button('*'),
        self.create_button('CE', None)        
        ],[
        self.create_button(1),
        self.create_button(2),
        self.create_button(3),
        self.create_button('-'),
        self.create_button('=', None)
        ],[
        self.create_button('.'),
        self.create_button(0),
        self.create_button(u"\u221A", None),
        self.create_button('+')       
        ]
        ]        
        # Create buttons grid using enumerate func. to get index for each row and button
        for row_index, row in enumerate(self.buttons):
            for col_index, col in enumerate(row):
                self.buttons[row_index][col_index].grid(row=row_index + 1, column=col_index, sticky=W+E+N+S)
                if self.buttons[2][4]:
                    self.buttons[2][4].grid(row=3, column=4, rowspan=2, sticky=W+E+N+S)


    def create_button(self, val, write=True):
        return Button(self.master, text=val, command=lambda:self.click(val,write), width=5, bd=1, bg=self.colors['med'], fg='#fff',
                      activebackground=self.colors['dark'], activeforeground='#fff', font=('Helvetica',24))                


    # Handle button clicks
    def click(self, text, write):
        if write == None:
            if text == '=' and self.equation:
                # remove operators from the beginning and the end of a string before avaluation
                while self.equation[0] in ['/','*']:
                    self.equation = self.equation[1:]
                while not self.equation[-1].isdigit():
                    self.equation = self.equation[:-1] 

                result = str(eval(self.equation))
                self.clear_screen()
                self.insert_screen(result,newline=True)
            elif text == u"\u221A" and self.equation:
                result = str(math.sqrt(eval(self.equation)))
                self.clear_screen()
                self.insert_screen(result,newline=True)
            elif text == "CE":
                self.clear_screen()
            elif text == 'DEL':
                self.del_screen()
        else:
            self.insert_screen(text)


    # Append new value to equasion string and display on the 'screen'
    def insert_screen(self, value,newline=False):
        # Enable text input to insert values
        self.screen.configure(state='normal')
        # Tag_config allows to name selected text widget and add properties
        self.screen.tag_config('val',justify=RIGHT)
        # Insert before char at index
        self.screen.insert(END,str(value),'val')
        self.equation += str(value)
        # Disable screen
        self.screen.configure(state ='disabled')


    # Clear entire screen and set equasion to empty string
    def clear_screen(self):
        self.equation = ''
        self.screen.configure(state='normal')
        self.screen.delete(1.0, END)
        self.screen.configure(state='disabled')


    # Remove last digit from equasion (copy string minus lat char, and re-insert it after deleting previous string)
    def del_screen(self):
        self.equation = self.equation[:-1]
        self.screen.configure(state='normal')
        text = self.screen.get("1.0",END)[:-2]
        self.screen.tag_config('val',justify=RIGHT)
        self.screen.delete(1.0, END)
        self.screen.insert(END,text, 'val')
        self.screen.configure(state='disabled')



root = Tk()

calculator = Calculator(root)

root.mainloop()
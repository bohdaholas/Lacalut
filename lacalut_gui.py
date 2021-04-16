from tkinter import *
from tkinter import scrolledtext  
from functools import partial
from tkinter.ttk import Combobox
from tkinter.ttk import Radiobutton

import json
import re


class Lacalut:
    def __init__(self):
        self.custom_verse_available = True
        self.verse = None
        self.proceed_db()

    def proceed_db(self):
        with open("poetry_db.json", mode="r", encoding="utf-8") as f:
                data = json.load(f)
        self.newdata = {}
        for key in data:
            newkey = re.sub('[“”(</a>)(</A>)]', '', key)
            self.newdata[newkey] = data[key]

    def initialise_starting_window(self):
        self.starting_window = Tk()
        # self.starting_window.configure(bg = "#63C77C")
        text = Label(self.starting_window, text= "Please chose the verse OR enter your own")
        text.pack()

        self.input = Entry(self.starting_window)
        self.input.pack()

        self.starting_window.title("Lacalut")
        self.starting_window.geometry('350x600')

        self.lbl = Label(self.starting_window, text="")
        self.lbl.pack()
        
        self.enter_custom_btn = Button(self.starting_window, text="enter custom verse", bg = "#315EBB", command = self.initialise_custom_verse_window)
        self.enter_custom_btn.pack()

        self.submit_verse_btn = Button(self.starting_window, text="submit your verse", bg = "#315EBB", command = self.submit_verse)
        self.submit_verse_btn.pack()

        self.user_verse_preview = Label(self.starting_window, text= "Your verse preview", height= 25)
        self.user_verse_preview.pack()


        self.selected = IntVar()

        self.rad1 = Radiobutton(self.starting_window, text='stream mode (we will interrupt you on first mistake)', value=1, variable=self.selected)
        self.rad1.pack()  
        self.rad2 = Radiobutton(self.starting_window, text='post analisys (we will let you know what you said wrong)', value=2, variable=self.selected)
        self.rad2.pack()

        self.move_to_analisys_btn = Button(self.starting_window, text="proceed to studying", command= self.proceed_with_settings, bg= "#315EBB")
        self.move_to_analisys_btn.pack()
        # self.btn1 = Button(self.starting_window, text="print verse", bg = "#315EBB", command = self.print_custom_verse)
        # self.btn1.pack()

        self.starting_window.mainloop()
    
    def proceed_with_settings(self):
        print(self.selected.get())
        if self.selected.get() == 1:
            self.initialise_last_page_streaming()
        elif self.selected.get() == 2:
            self.initialise_last_page_post_processing()

    def initialise_last_page_streaming(self):
        self.learning_window = Tk()
        self.learning_window.geometry('300x300')

        self.learning_window_msg = Label(self.learning_window, text= "grats")
        self.learning_window_msg.pack()

        self.indicator = Label(self.learning_window, text= "start talking when ready", bg="#64F341", height= 5, width= 20, font=("Arial", 15))
        self.indicator.pack()

        self.test_wrong_btn = Button(self.learning_window, text= "testWrong", command = self.indicate_streaming_mistake)
        self.test_wrong_btn.pack()

        self.test_ok_btn = Button(self.learning_window, text= "testOk", command = self.indicate_streaming_ok)
        self.test_ok_btn.pack()

        self.learning_window.mainloop()
    
    def initialise_last_page_post_processing(self):
        self.learning_window = Tk()
        self.learning_window.geometry('300x300')

        self.start_listening_btn = Button(self.learning_window, text= "start listening", command= start_listening)
        self.start_listening_btn.pack()

        self.stop_listening_btn = Button(self.learning_window, text= "stop listening", command= stop_listening)
        self.stop_listening_btn.pack()

        self.learning_window_msg = Label(self.learning_window, text= "grats")
        self.learning_window_msg.pack()

        self.report = Label(self.learning_window, text="your report will be here")
        self.report.pack()

        self.learning_window.mainloop()

    def indicate_streaming_mistake(self):
        self.indicator.configure(text= "mistake in line\n{}".format("!!LINE!!"), bg="#FA9D0E")

    def indicate_streaming_ok(self):
        self.indicator.configure(text= "everything is OK", bg="#64F341")

    def print_custom_verse(self):
        print(self.verse)

    def submit_verse(self):
        if self.verse == None or self.input.get():
            if self.input.get() in self.newdata:
                self.verse = self.newdata[self.input.get()]
        if len(self.verse) > 600:
            self.verse = self.verse[:600] + "..."
        self.user_verse_preview.config(text=self.verse)

    
    def initialise_custom_verse_window(self):
        if self.custom_verse_available:
            self.custom_verse_available = False
            self.custom_verse_window = Tk()

            self.enter_your_verse = Label(self.custom_verse_window, text= "enter your verse")
            self.enter_your_verse.pack()

            self.txt = scrolledtext.ScrolledText(self.custom_verse_window, width=40, height=10, bg="#85ABFC")
            self.txt.pack(anchor='center')
            
            self.submit_btn = Button(self.custom_verse_window, text="submit your verse", bg = "#315EBB", command = self.submit_custom_verse)
            self.submit_btn.pack()

            self.custom_verse_window.mainloop()

    
    def submit_custom_verse(self):
        self.verse = self.txt.get(1.0, END)
        self.custom_verse_window.destroy()
        self.custom_verse_available = True


def start_listening():
    pass

def stop_listening():
    pass


if __name__ == "__main__":
    main_window = Lacalut()
    main_window.initialise_starting_window()
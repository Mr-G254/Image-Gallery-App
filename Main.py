from customtkinter import*
from PIL import Image


class MainWindow():
    def __init__(self):
        
        self.App = CTk()
        self.App.title("Image Gallery")
        self.App.geometry("850x450+200+150")

        self.img0 = CTkImage(Image.open("Image-Gallery-App\Icons\menu.png"),size=(24,24))
        self.img1 = CTkImage(Image.open("Image-Gallery-App\Icons\home.png"),size=(24,24))
        self.img2 = CTkImage(Image.open("Image-Gallery-App\Icons\\folder.png"),size=(24,24))
        self.img3 = CTkImage(Image.open("Image-Gallery-App\Icons\exit.png"),size=(24,24))


        self.Main_frame = CTkFrame(self.App,width=850,height=450,fg_color="#5A011B",corner_radius=0)
        self.Main_frame.place(x=0,y=0)

        self.Menubar = CTkFrame(self.Main_frame,width=40,height=450,fg_color="#760526",corner_radius=0)
        self.Menubar.place(x=0,y=0)
        self.is_menu_maximised = False

        self.menu = CTkButton(self.Menubar,width=40,height=35,image=self.img0,fg_color="#760526",corner_radius=0,hover_color="#B80438",text="",command=self.resize_menu_bar)
        self.menu.place(x=0,y=0)

        self.menu_text = CTkLabel(self.Menubar,height=31,width=110,fg_color="#760526",corner_radius=5,text="   Menu",font=("Times",16),anchor=W)
        self.menu_text.place(x=45,y=3)
        self.menu_text.bind('<Enter>',lambda Event: self.highlight(Event,self.menu_text,self.menu))
        self.menu_text.bind('<Leave>',lambda Event: self.unhighlight(Event,self.menu_text,self.menu))
        self.menu_text.bind('<Button-1>',lambda Event: self.resize_event(Event))

        self.menu.bind('<Enter>',lambda Event: self.highlight(Event,self.menu_text,""))
        self.menu.bind('<Leave>',lambda Event: self.unhighlight(Event,self.menu_text,""))

        self.home = CTkButton(self.Menubar,width=40,height=35,image=self.img1,fg_color="#760526",corner_radius=0,hover_color="#B80438",text="")
        self.home.place(x=0,y=35)

        self.home_text = CTkLabel(self.Menubar,height=31,width=110,fg_color="#760526",corner_radius=5,text="   Home",font=("Times",16),anchor=W)
        self.home_text.place(x=45,y=37)
        self.home_text.bind('<Enter>',lambda Event: self.highlight(Event,self.home_text,self.home))
        self.home_text.bind('<Leave>',lambda Event: self.unhighlight(Event,self.home_text,self.home))

        self.home.bind('<Enter>',lambda Event: self.highlight(Event,self.home_text,""))
        self.home.bind('<Leave>',lambda Event: self.unhighlight(Event,self.home_text,""))

        self.folder = CTkButton(self.Menubar,width=40,height=35,image=self.img2,fg_color="#760526",corner_radius=0,hover_color="#B80438",text="")
        self.folder.place(x=0,y=70)

        self.folder_text = CTkLabel(self.Menubar,height=31,width=110,fg_color="#760526",corner_radius=5,text="   Folders",font=("Times",16),anchor=W)
        self.folder_text.place(x=45,y=72)
        self.folder_text.bind('<Enter>',lambda Event: self.highlight(Event,self.folder_text,self.folder))
        self.folder_text.bind('<Leave>',lambda Event: self.unhighlight(Event,self.folder_text,self.folder))

        self.folder.bind('<Enter>',lambda Event: self.highlight(Event,self.folder_text,""))
        self.folder.bind('<Leave>',lambda Event: self.unhighlight(Event,self.folder_text,""))

        self.exit = CTkButton(self.Menubar,width=40,height=35,image=self.img3,fg_color="#760526",corner_radius=0,hover_color="#B80438",text="",command=self.close)
        self.exit.place(x=0,y=415)

        self.exit_text = CTkLabel(self.Menubar,height=31,width=110,fg_color="#760526",corner_radius=5,text="   Exit",font=("Times",16),anchor=W)
        self.exit_text.place(x=45,y=417)
        self.exit_text.bind('<Enter>',lambda Event: self.highlight(Event,self.exit_text,self.exit))
        self.exit_text.bind('<Leave>',lambda Event: self.unhighlight(Event,self.exit_text,self.exit))
        self.exit_text.bind('<Button-1>',lambda Event: self.close_event(Event))

        self.exit.bind('<Enter>',lambda Event: self.highlight(Event,self.exit_text,""))
        self.exit.bind('<Leave>',lambda Event: self.unhighlight(Event,self.exit_text,""))

        self.App.mainloop()

    def resize_menu_bar(self):
        if self.is_menu_maximised == False:
            self.Menubar.configure(width=160)
            self.is_menu_maximised = True
        
        else:
            self.Menubar.configure(width=40)
            self.is_menu_maximised = False

    def resize_event(self,Event):
        self.resize_menu_bar()

    def highlight(self,Event,label,button):
        label.configure(fg_color="#B80438")

        if button != "":
            button.configure(fg_color="#B80438")

    def unhighlight(self,Event,label,button):
        label.configure(fg_color="#760526")

        if button != "":
            button.configure(fg_color="#760526")

    def close(self):
        self.App.destroy()

    def close_event(self,Event):
        self.close()

app = MainWindow()
#2A272Egr
#5A011B
#760526
#830127
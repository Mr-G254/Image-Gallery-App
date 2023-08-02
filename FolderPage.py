from customtkinter import*
from PIL import Image
from datetime import date

class FolderPage():
    def __init__(self,Frame):
        self.img0 = CTkImage(Image.open("Icons/add.png"),size=(18,18))
        self.img1 = CTkImage(Image.open("Icons/folder2.png"),size=(60,60))
        self.img2 = CTkImage(Image.open("Icons/bin.png"),size=(18,18))

        self.frame = CTkFrame(Frame,width=500,height=440,fg_color="#760526",corner_radius=8)

        self.titlebar = CTkLabel(self.frame,width=150,height=34,fg_color="#5A011B",corner_radius=7,text="")
        self.titlebar.place(x=175,y=10)

        self.title = CTkLabel(self.titlebar,width=110,height=28,text="Folders",font=("Times",15),fg_color="#760526",corner_radius=7)
        self.title.place(x=3,y=3)

        self.add = CTkButton(self.titlebar,width=24,height=28,text="",image=self.img0,fg_color="#5A011B",hover_color="#5A011B")
        self.add.place(x=114,y=3)

        self.folder_frame = CTkScrollableFrame(self.frame,width=320,height=370,fg_color="#760526",)
        self.folder_frame.place(x=5,y=50)

        self.folder1 = CTkFrame(self.folder_frame,width=310,height=77,fg_color="#5A011B",corner_radius=9)
        self.folder1.grid(row=0,column=0)

        self.item_frame = CTkFrame(self.folder1,width=270,height=71,corner_radius=9,fg_color="#5A011B")
        self.item_frame.place(x=3,y=3)
        self.item_frame.bind('<Enter>',lambda Event: self.highlight_folder(Event,self.item_frame))
        self.item_frame.bind('<Leave>',lambda Event: self.unhighlight_folder(Event,self.item_frame))

        self.icon = CTkLabel(self.item_frame,height=60,width=55,fg_color="#5A011B",text="",image=self.img1)
        self.icon.place(x=15,y=10)
        self.icon.bind('<Enter>',lambda Event: self.highlight_folder(Event,self.item_frame))
        self.icon.bind('<Leave>',lambda Event: self.unhighlight_folder(Event,self.item_frame))


        self.folder_name = CTkLabel(self.item_frame,width=150,height=30,fg_color="#5A011B",text="Pictures",font=("Times",17),anchor=W)
        self.folder_name.place(x=90,y=10)
        self.folder_name.bind('<Enter>',lambda Event: self.highlight_folder(Event,self.item_frame))
        self.folder_name.bind('<Leave>',lambda Event: self.unhighlight_folder(Event,self.item_frame))


        self.folder_details = CTkLabel(self.item_frame,width=150,height=30,fg_color="#5A011B",text=f"Images | {date.today()}",font=("Times",15),anchor=W)
        self.folder_details.place(x=90,y=30)
        self.folder_details.bind('<Enter>',lambda Event: self.highlight_folder(Event,self.item_frame))
        self.folder_details.bind('<Leave>',lambda Event: self.unhighlight_folder(Event,self.item_frame))

        self.folder1.bind('<Enter>',lambda Event: self.highlight_folder(Event,self.item_frame))
        self.folder1.bind('<Leave>',lambda Event: self.unhighlight_folder(Event,self.item_frame))

        self.delete = CTkButton(self.folder1,height=30,width=30,image=self.img2,text="",fg_color="#5A011B",hover_color="#5A011B")
        self.delete.place(x=275,y=23)
        self.delete.bind('<Enter>',lambda Event: self.highlight_folder(Event,self.item_frame))
        self.delete.bind('<Leave>',lambda Event: self.unhighlight_folder(Event,self.item_frame))

        self.close = CTkButton(self.frame,height=30,width=120,fg_color="#5A011B",hover_color="#5A011B",corner_radius=6,text="Close",font=("Times",15),command=self.hide)
        self.close.place(x=360,y=400)

    def place(self):
        self.frame.place(x=50,y=5)

    def hide(self):
        self.frame.place_forget()

    def highlight_folder(self,Event,frame):
        frame.configure(fg_color="#760526")
        for i in frame.winfo_children():
            i.configure(fg_color="#760526")
        
    def unhighlight_folder(self,Event,frame):
        frame.configure(fg_color="#5A011B")
        for i in frame.winfo_children():
            i.configure(fg_color="#5A011B")
from customtkinter import*
from PIL import Image,ImageTk

class ImageTools():
    def __init__(self,master,image_list):
        self.l = CTkImage(Image.open("Icons/left-arrow.png"))
        self.r = CTkImage(Image.open("Icons/right-arrow.png"))
        self.img0 = CTkImage(Image.open("Icons/crop.png"),size=(25,25))
        self.img1 = CTkImage(Image.open("Icons/flip_h.png"),size=(25,25))
        self.img2 = CTkImage(Image.open("Icons/flip_v.png"),size=(25,25))
        self.img3 = CTkImage(Image.open("Icons/pencil.png"),size=(25,25))

        self.Image_list = image_list
        self.current_image = ""

        self.image_frame = CTkFrame(master,width=850,height=450,fg_color="#5A011B",corner_radius=0)

        self.back = CTkButton(self.image_frame,width=100,height=30,text="Back",font=("Times",16),corner_radius=5,fg_color="#760526",hover_color="#760526",command=lambda: self.image_frame.place_forget())
        self.back.place(x=5,y=5)

        self.save = CTkButton(self.image_frame,width=100,height=30,text="Save",font=("Times",16),corner_radius=5,fg_color="#760526",hover_color="#760526")
        self.save.place(x=745,y=5)

        self.left = CTkButton(self.image_frame,width=20,height=50,text="",image=self.l,fg_color="#5A011B",hover_color="#760526",corner_radius=5,command=self.previous)
        self.left.place(x=5,y=200)

        self.right = CTkButton(self.image_frame,width=20,height=50,text="",image=self.r,fg_color="#5A011B",hover_color="#760526",corner_radius=5,command=self.next)
        self.right.place(x=810,y=200)

        self.toolbar = CTkFrame(self.image_frame,width=206,height=40,corner_radius=7,fg_color="#760526")
        self.toolbar.place(x=325,y=5)

        self.crop = CTkButton(self.toolbar,width=50,height=40,text="",image=self.img0,corner_radius=0,fg_color="#760526",hover_color="#760526")
        self.crop.place(x=3,y=0)

        self.flip_h = CTkButton(self.toolbar,width=50,height=40,text="",image=self.img1,corner_radius=0,fg_color="#760526",hover_color="#760526")
        self.flip_h.place(x=53,y=0)

        self.flip_v = CTkButton(self.toolbar,width=50,height=40,text="",image=self.img2,corner_radius=0,fg_color="#760526",hover_color="#760526")
        self.flip_v.place(x=103,y=0)

        self.draw = CTkButton(self.toolbar,width=50,height=40,text="",image=self.img3,corner_radius=0,fg_color="#760526",hover_color="#760526")
        self.draw.place(x=153,y=0)

        self.canvas = CTkCanvas(self.image_frame,width=760,height=390,background="#5A011B",highlightthickness=0)
        self.canvas.place(x=45,y=55)

    def display_image(self,path):
        self.current_image = path
        self.img = Image.open(path)
        width,height=self.img.size

        if height > 390:
            perc = ((height-390)/height)*100
            width = ((100-perc)/100)*width
            height = 390

            self.img = self.img.resize((int(width),height),Image.Resampling.LANCZOS)

        self.image = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(380,195,image=self.image)

    def next(self):
        current_index = self.Image_list.index(self.current_image)

        if current_index == len(self.Image_list)-1:
            next_image = self.Image_list[0]
        else:                                    
            next_image = self.Image_list[current_index+1]

        self.display_image(next_image)

    def previous(self):
        current_index = self.Image_list.index(self.current_image)

        if current_index > 0:
            prev_image = self.Image_list[current_index-1]
            self.display_image(prev_image)

    def place(self,Event,path):
        self.display_image(path)
        self.image_frame.tkraise()
        self.image_frame.place(x=0,y=0)
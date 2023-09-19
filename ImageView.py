from customtkinter import*
from tkinter import Canvas
from PIL import Image,ImageTk

class ImageView():
    def __init__(self,master,image_list,load_image_function):
        self.app = master
        self.callback = load_image_function
        self.l = CTkImage(Image.open("Icons/left-arrow.png"))
        self.r = CTkImage(Image.open("Icons/right-arrow.png"))
        self.img0 = CTkImage(Image.open("Icons/crop.png"),size=(25,25))
        self.img1 = CTkImage(Image.open("Icons/flip_h.png"),size=(25,25))
        self.img2 = CTkImage(Image.open("Icons/flip_v.png"),size=(25,25))
        self.img3 = CTkImage(Image.open("Icons/pencil.png"),size=(25,25))

        self.Image_list = image_list
        self.current_image_path = ""
        self.is_cropped = False
        self.x_ratio = 0
        self.y_ratio = 0
        self.start_x = 0
        self.start_y = 0

        self.image_frame = CTkFrame(master,width=850,height=450,fg_color="#5A011B",corner_radius=0)

        self.back = CTkButton(self.image_frame,width=100,height=30,text="Back",font=("Times",16),corner_radius=5,fg_color="#760526",hover_color="#760526",command=self.go_back)
        self.back.place(x=5,y=5)

        self.save = CTkButton(self.image_frame,width=100,height=30,text="Save",font=("Times",16),corner_radius=5,fg_color="#760526",hover_color="#760526",command=self.save_edited_image)
        self.save.place(x=745,y=5)

        self.left = CTkButton(self.image_frame,width=20,height=50,text="",image=self.l,fg_color="#5A011B",hover_color="#760526",corner_radius=5,command=self.previous)
        self.left.place(x=5,y=200)

        self.right = CTkButton(self.image_frame,width=20,height=50,text="",image=self.r,fg_color="#5A011B",hover_color="#760526",corner_radius=5,command=self.next)
        self.right.place(x=810,y=200)

        self.toolbar = CTkFrame(self.image_frame,width=206,height=39,corner_radius=7,fg_color="#760526")
        self.toolbar.place(x=325,y=5)

        self.crop = CTkButton(self.toolbar,width=50,height=35,text="",image=self.img0,corner_radius=6,fg_color="#760526",hover_color="#760526",command=self.crop_selection)
        self.crop.place(x=2,y=2)

        self.flip_h = CTkButton(self.toolbar,width=50,height=35,text="",image=self.img1,corner_radius=6,fg_color="#760526",hover_color="#5A011B")
        self.flip_h.place(x=53,y=2)

        self.flip_v = CTkButton(self.toolbar,width=50,height=35,text="",image=self.img2,corner_radius=6,fg_color="#760526",hover_color="#5A011B")
        self.flip_v.place(x=103,y=2)

        self.draw = CTkButton(self.toolbar,width=50,height=35,text="",image=self.img3,corner_radius=6,fg_color="#760526",hover_color="#760526",command=self.draw_image)
        self.draw.place(x=154,y=2)

        self.canvas = Canvas(self.image_frame,width=760,height=395,background="#5A011B",highlightthickness=0)
        self.canvas.place(x=45,y=53)

    def display_image(self,path):
        self.current_image_path = path
        self.img = Image.open(path)
        self.width,self.height=self.img.size

        original_width = self.width
        original_height = self.height

        if self.height > 390:
            perc = ((self.height-390)/self.height)*100
            self.width = ((100-perc)/100)*self.width
            self.height = 390

            self.img = self.img.resize((int(self.width),self.height),Image.Resampling.LANCZOS)

        self.x_ratio = original_width/self.width
        self.y_ratio = original_height/self.height
        self.image = ImageTk.PhotoImage(self.img)

        self.disable_crop()
        self.reset_toolbar_buttons()
        self.canvas.delete('all')

        self.Image = self.canvas.create_image(380,195,image=self.image)
        self.app.title(path)

    def next(self):
        self.canvas.delete('all')

        current_index = self.Image_list.index(self.current_image_path)

        if current_index == len(self.Image_list)-1:
            next_image = self.Image_list[0]
        else:                                    
            next_image = self.Image_list[current_index+1]

        self.canvas.unbind('<Motion>')
        self.display_image(next_image)

    def previous(self):
        self.canvas.delete('all')

        current_index = self.Image_list.index(self.current_image_path)

        if current_index > 0:
            self.canvas.unbind('<Motion>')
            prev_image = self.Image_list[current_index-1]
            self.display_image(prev_image)

    def place(self,Event,path):
        self.display_image(path)
        self.image_frame.tkraise()
        self.image_frame.place(x=0,y=0)
        self.app.title(path)

    def get_coordinates(self):
        coordinates = self.canvas.coords(self.Image)
        self.x1 = coordinates[0] - (self.width/2)
        self.y1 = coordinates[1] - (self.height/2)
        self.x2 = coordinates[0] + (self.width/2)
        self.y2 = coordinates[1] + (self.height/2)

        self.start_x = self.x1
        self.start_y = self.y1

    def crop_selection(self):
        self.crop.configure(state=DISABLED,fg_color="#5A011B")
        self.draw.configure(state=NORMAL,fg_color="#760526")

        self.get_coordinates()
        self.border = self.canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,width=3,outline='#FF4D00')
        self.get_border_coordinates()
        self.canvas.bind('<Motion>',lambda Event: self.get_selection(Event))

    def get_border_coordinates(self):
        coords = self.canvas.coords(self.border)
        self.b_x1 = coords[0]
        self.b_y1 = coords[1]
        self.b_x2 = coords[2]
        self.b_y2 = coords[3]

    def get_selection(self,Event):
        if Event.x >= int(self.x1) and Event.x <= int(self.x2) and Event.y == int(self.b_y1):
            self.canvas.configure(cursor='sb_v_double_arrow')
            self.canvas.unbind('<Button-1>')
            self.canvas.bind('<Button-1>',lambda Event: self.cursor_motion(Event,'x','a'))
            self.canvas.unbind('<ButtonRelease-1>')
            self.canvas.bind('<ButtonRelease-1>',lambda Event: self.cursor_motion_stop(Event))

        elif Event.x >= int(self.x1) and Event.x <= int(self.x2) and Event.y == int(self.b_y2):
            self.canvas.configure(cursor='sb_v_double_arrow')
            self.canvas.unbind('<Button-1>')
            self.canvas.bind('<Button-1>',lambda Event: self.cursor_motion(Event,'x','b'))
            self.canvas.unbind('<ButtonRelease-1>')
            self.canvas.bind('<ButtonRelease-1>',lambda Event: self.cursor_motion_stop(Event))

        elif Event.y >= int(self.y1) and Event.y <= int(self.y2) and Event.x == int(self.b_x1):
            self.canvas.configure(cursor='sb_h_double_arrow')
            self.canvas.unbind('<Button-1>')
            self.canvas.bind('<Button-1>',lambda Event: self.cursor_motion(Event,'y','a'))
            self.canvas.unbind('<ButtonRelease-1>')
            self.canvas.bind('<ButtonRelease-1>',lambda Event: self.cursor_motion_stop(Event))

        elif Event.y >= int(self.y1) and Event.y <= int(self.y2) and Event.x == int(self.b_x2):
            self.canvas.configure(cursor='sb_h_double_arrow')
            self.canvas.unbind('<Button-1>')
            self.canvas.bind('<Button-1>',lambda Event: self.cursor_motion(Event,'y','b'))
            self.canvas.unbind('<ButtonRelease-1>')
            self.canvas.bind('<ButtonRelease-1>',lambda Event: self.cursor_motion_stop(Event))

        else:
            self.canvas.configure(cursor='')
        
        self.get_border_coordinates()

    def cursor_motion(self,Event,x_or_y,a_or_b):
        self.canvas.unbind('<Motion>')
        self.canvas.bind('<Motion>',lambda Event: self.resize_selection(Event,x_or_y,a_or_b))

    def cursor_motion_stop(self,Event):
        self.canvas.unbind('<Motion>')
        self.canvas.bind('<Motion>',lambda Event: self.get_selection(Event))

    def resize_selection(self,Event,x_or_y,a_or_b):
        if x_or_y == 'x':
            if a_or_b == 'a':
                if Event.y >= self.y1 and Event.y < self.y2:
                    self.canvas.coords(self.border,self.b_x1,Event.y,self.b_x2,self.b_y2)
            elif a_or_b == 'b':
                if Event.y <= self.y2 and Event.y > self.y1:
                    self.canvas.coords(self.border,self.b_x1,self.b_y1,self.b_x2,Event.y)
            
            self.is_cropped = True
        
        elif x_or_y == 'y':
            if a_or_b == 'a':
                if Event.x >= self.x1 and Event.x < self.x2:
                    self.canvas.coords(self.border,Event.x,self.b_y1,self.b_x2,self.b_y2)
            elif a_or_b == 'b':
                if Event.x <= self.x2 and Event.x > self.x1:
                    self.canvas.coords(self.border,self.b_x1,self.b_y1,Event.x,self.b_y2)
            
            self.is_cropped = True

        self.get_coordinates()
    
    def disable_crop(self):
        try:
            self.is_cropped = False
            self.canvas.unbind('<Motion>')
            self.canvas.unbind('<Button-1>')
            self.canvas.delete(self.border)
        except:
            pass

    def reset_toolbar_buttons(self):
        self.draw.configure(state=NORMAL,fg_color="#760526")
        self.crop.configure(state=NORMAL,fg_color="#760526")

    def draw_image(self):
        try:
            self.disable_crop()
        except:
            pass

        self.draw.configure(state=DISABLED,fg_color="#5A011B")
        self.crop.configure(state=NORMAL,fg_color="#760526")

    def save_edited_image(self):
        if self.is_cropped:
            coords_from_0 =[(self.b_x1 - self.start_x),(self.b_y1 - self.start_y),(self.b_x2 - self.start_x),(self.b_y2 - self.start_y)]
            crop_coords = [(coords_from_0[0] * self.x_ratio),(coords_from_0[1] * self.y_ratio),(coords_from_0[2] * self.x_ratio),(coords_from_0[3] * self.y_ratio)] 

            image = Image.open(self.current_image_path)
            crop = image.crop(crop_coords)
            
            name = self.current_image_path.split(".") 
            filename = f"{name[0]}(1).{name[1]}"
            crop.save(filename)

            self.Image_list.append(filename)
            self.Image_list.sort()
            
            self.display_image(filename)
            self.callback()

    def go_back(self):
        self.app.title('Image Gallery')
        self.image_frame.place_forget()
        self.crop.configure(state=NORMAL,fg_color="#760526")
        self.draw.configure(state=NORMAL,fg_color="#760526")
        self.canvas.unbind('<Motion>')
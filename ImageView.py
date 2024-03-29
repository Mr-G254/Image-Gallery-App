from customtkinter import*
from tkinter import Canvas,messagebox,colorchooser,Spinbox
from PIL import Image,ImageTk
import os
import cv2
import imutils

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
        self.img4 = CTkImage(Image.open("Icons/bin.png"),size=(20,20))
        self.img5 = CTkImage(Image.open("Icons/color-picker.png"),size=(24,24))
        self.img6 = CTkImage(Image.open("Icons/up.png"),size=(6,6))
        self.img7 = CTkImage(Image.open("Icons/down.png"),size=(6,6))

        self.Image_list = image_list
        self.current_image_path = ""

        self.is_cropped = False
        self.x_ratio = 0
        self.y_ratio = 0
        self.start_x = 0
        self.start_y = 0

        self.flip = []

        self.visible_image = ''
        self.original_image = ''

        self.chosen_color = "black"
        self.pixel_size = 10

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
        self.toolbar.place(x=303,y=5)

        self.crop = CTkButton(self.toolbar,width=50,height=35,text="",image=self.img0,corner_radius=6,fg_color="#760526",hover_color="#5A011B",command=self.crop_selection)
        self.crop.place(x=2,y=2)

        self.flip_h = CTkButton(self.toolbar,width=50,height=35,text="",image=self.img1,corner_radius=6,fg_color="#760526",hover_color="#5A011B",command=self.flip_horizontal)
        self.flip_h.place(x=53,y=2)

        self.flip_v = CTkButton(self.toolbar,width=50,height=35,text="",image=self.img2,corner_radius=6,fg_color="#760526",hover_color="#5A011B",command=self.flip_vertical)
        self.flip_v.place(x=103,y=2)

        self.draw = CTkButton(self.toolbar,width=50,height=35,text="",image=self.img3,corner_radius=6,fg_color="#760526",hover_color="#5A011B",command=self.draw_image)
        self.draw.place(x=154,y=2)

        self.delete = CTkButton(self.image_frame,width=40,height=39,text="",image=self.img4,corner_radius=5,fg_color="#760526",hover_color="#5A011B")
        self.delete.place(x=514,y=5)

        self.canvas = Canvas(self.image_frame,width=762,height=397,background="#5A011B",highlightthickness=0)
        self.canvas.place(x=44,y=47)

        self.draw_eframe = CTkFrame(self.image_frame,width=150,height=39,corner_radius=7,fg_color="#760526")

        self.color_frame = CTkFrame(self.draw_eframe,width=90,height=35,corner_radius=6,fg_color="black")
        self.color_frame.place(x=2,y=2)

        self.color_button = CTkButton(self.color_frame,width=30,height=30,fg_color="black",text='',image=self.img5,hover_color='black',command=self.choose_color)
        self.color_button.place(x=3,y=2)

        self.entry = CTkEntry(self.draw_eframe,width=32,height=34,fg_color="#5A011B",font=('Times',17),corner_radius=4,border_width=0)
        self.entry.insert(0,str(self.pixel_size))
        self.entry.bind('<KeyRelease>',self.check_value)
        self.entry.place(x=94,y=2)

        self.up = CTkButton(self.draw_eframe,width=21,height=17,fg_color="#5A011B",text='',corner_radius=4,image=self.img6,command=lambda: self.change_value('add'))
        self.up.place(x=128,y=2)

        self.down = CTkButton(self.draw_eframe,width=21,height=17,fg_color="#5A011B",text='',corner_radius=4,image=self.img7,command=lambda: self.change_value('minus'))
        self.down.place(x=128,y=20)

        self.editing_frame = CTkFrame(self.image_frame,width=762,height=397,fg_color="#5A011B") 
        self.placed = FALSE

        self.editing_image = CTkLabel(self.editing_frame,text='',width=762,height=397,fg_color="#5A011B")
        self.editing_image.place(x=0,y=0)

    def place_editing_frame(self):
        self.editing_frame.place(x=44,y=49)
        self.placed = TRUE

    def display_image(self,path):
        self.editing_frame.place_forget()
        self.current_image_path = path
        self.original_image = cv2.imread(path)

        self.img = cv2.imread(path)
        self.height,self.width,channels = self.img.shape

        original_width = self.width
        original_height = self.height

        if self.height > 390:
            perc = ((self.height-390)/self.height)*100
            self.width = ((100-perc)/100)*self.width
            self.height = 390

            if self.width > 760:
                perc = ((self.width-760)/self.width)*100
                self.width = 760
                self.height = ((100-perc)/100)*self.height

            self.img = imutils.resize(self.img, width=int(self.width), height=(self.height))

        self.x_ratio = original_width/self.width
        self.y_ratio = original_height/self.height
        self.image0 = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.visible_image = self.image0
        self.image = ImageTk.PhotoImage(Image.fromarray(self.visible_image))

        self.disable_crop()
        self.disable_draw()
        self.reset_toolbar_buttons()
        self.canvas.delete('all')

        self.Image = self.canvas.create_image(381,199,image=self.image)
        self.app.title(f"Image Gallery - {path}")

        self.delete.configure(command = lambda: self.delete_image(self.current_image_path))
        self.get_coordinates()
        

    def next(self):
        self.disable_crop()
        self.disable_draw()
        self.editing_frame.place_forget()
        self.placed = False
        self.canvas.delete('all')

        current_index = self.Image_list.index(self.current_image_path)

        if current_index == len(self.Image_list)-1:
            next_image = self.Image_list[0]
        else:                                    
            next_image = self.Image_list[current_index+1]

        self.canvas.unbind('<Motion>')
        self.display_image(next_image)

    def previous(self):
        self.disable_crop()
        self.disable_draw()
        self.editing_frame.place_forget()
        self.placed = False
        self.canvas.delete('all')

        current_index = self.Image_list.index(self.current_image_path)

        if current_index > 0:
            self.canvas.unbind('<Motion>')
            prev_image = self.Image_list[current_index-1]
        
        elif current_index == 0:
            prev_image = self.Image_list[len(self.Image_list)-1]

        self.display_image(prev_image)

    def place(self,Event,path):
        self.display_image(path)
        self.image_frame.tkraise()
        self.image_frame.place(x=0,y=0)

    def get_coordinates(self):
        coordinates = self.canvas.coords(self.Image)
        self.x1 = coordinates[0] - (self.width/2)
        self.y1 = coordinates[1] - (self.height/2)
        self.x2 = coordinates[0] + (self.width/2)
        self.y2 = coordinates[1] + (self.height/2)

        self.start_x = self.x1
        self.start_y = self.y1

    def crop_selection(self):
        self.disable_draw()
        
        self.flip.clear()
        self.visible_image = self.image0
        self.crop.configure(state=DISABLED,fg_color="#5A011B")
        self.draw.configure(state=NORMAL,fg_color="#760526")

        try:
            self.editing_frame.place_forget()
            self.canvas.delete(self.border)
        except:
            pass

        # self.get_coordinates()
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
        if Event.x >= int(self.x1) and Event.x <= int(self.x2) and Event.y <= int(self.b_y1)+3 and Event.y >= int(self.b_y1):
            self.canvas.configure(cursor='sb_v_double_arrow')
            self.canvas.unbind('<Button-1>')
            self.canvas.bind('<Button-1>',lambda Event: self.cursor_motion(Event,'x','a'))
            self.canvas.unbind('<ButtonRelease-1>')
            self.canvas.bind('<ButtonRelease-1>',lambda Event: self.cursor_motion_stop(Event))

        elif Event.x >= int(self.x1) and Event.x <= int(self.x2) and Event.y <= int(self.b_y2) and Event.y >= int(self.b_y2)-3:
            self.canvas.configure(cursor='sb_v_double_arrow')
            self.canvas.unbind('<Button-1>')
            self.canvas.bind('<Button-1>',lambda Event: self.cursor_motion(Event,'x','b'))
            self.canvas.unbind('<ButtonRelease-1>')
            self.canvas.bind('<ButtonRelease-1>',lambda Event: self.cursor_motion_stop(Event))

        elif Event.y >= int(self.y1) and Event.y <= int(self.y2) and Event.x >= int(self.b_x1)-3 and Event.x <= int(self.b_x1):
            self.canvas.configure(cursor='sb_h_double_arrow')
            self.canvas.unbind('<Button-1>')
            self.canvas.bind('<Button-1>',lambda Event: self.cursor_motion(Event,'y','a'))
            self.canvas.unbind('<ButtonRelease-1>')
            self.canvas.bind('<ButtonRelease-1>',lambda Event: self.cursor_motion_stop(Event))

        elif Event.y >= int(self.y1) and Event.y <= int(self.y2) and Event.x >= int(self.b_x2) and Event.x <= int(self.b_x2)+3:
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

        # self.get_coordinates()
    
    def disable_crop(self):
        try:
            self.crop.configure(state=NORMAL,fg_color="#760526")
            self.is_cropped = False
            self.canvas.unbind('<Motion>')
            self.canvas.unbind('<Button-1>')
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
        self.draw_eframe.place(x=564,y=5)
        self.editing_frame.place_forget()

        try:
            self.canvas.delete(self.border)
        except:
            pass

        self.canvas.bind('<Motion>',self.draw_config)
    
    def flip_horizontal(self):
        self.color_frame.place_forget()
        self.disable_crop()
        self.place_editing_frame()

        self.visible_image = cv2.flip(self.visible_image, 1)
        self.editing_image.configure(image = ImageTk.PhotoImage(Image.fromarray(self.visible_image)))
        self.flip.append(1)

    def flip_vertical(self):
        self.color_frame.place_forget()
        self.disable_crop()
        self.place_editing_frame()

        self.visible_image = cv2.flip(self.visible_image, 0)
        self.editing_image.configure(image = ImageTk.PhotoImage(Image.fromarray(self.visible_image)))
        self.flip.append(0)

    def save_edited_image(self):
        if self.is_cropped:
            coords_from_0 =[(self.b_x1 - self.start_x),(self.b_y1 - self.start_y),(self.b_x2 - self.start_x),(self.b_y2 - self.start_y)]
            crop_coords = [(coords_from_0[0] * self.x_ratio),(coords_from_0[1] * self.y_ratio),(coords_from_0[2] * self.x_ratio),(coords_from_0[3] * self.y_ratio)]

            edited_image = self.original_image[int(crop_coords[1]):int(crop_coords[3]),int(crop_coords[0]):int(crop_coords[2])]

        elif len(self.flip) > 0:
            edited_image = self.original_image

            for i in self.flip:
                edited_image = cv2.flip(edited_image,i)

        filename = self.get_filename()
        cv2.imwrite(filename,edited_image)
        self.add_saved_image(filename)
        self.disable_crop()
       
    def get_filename(self):
        name = self.current_image_path.split(".") 

        count = 1
        f_name = name[0].split('(')[0]
        filename = f"{f_name}({str(count)}).{name[1]}"

        while os.path.exists(filename):
            count = count + 1
            filename = f"{f_name}({str(count)}).{name[1]}"
        
        return filename

    def add_saved_image(self,filename):
        self.Image_list.append(filename)
        self.Image_list.sort()
        
        self.display_image(filename)
        self.callback()

    def delete_image(self,filename):
        if messagebox.askyesno("Deleting image",f"Are you sure you want to delete '{self.current_image_path}'"):

            self.next()
            os.remove(filename)
            self.Image_list.remove(filename)
            self.callback()


    def go_back(self):
        self.current_image_path = ''
        self.app.title('Image Gallery')
        self.image_frame.place_forget()
        self.crop.configure(state=NORMAL,fg_color="#760526")
        self.draw.configure(state=NORMAL,fg_color="#760526")
        self.canvas.unbind('<Motion>')

    def choose_color(self):
        try:
            color = colorchooser.askcolor(title="Choose a color",initialcolor="black")
            self.chosen_color = color[1]
            self.color_frame.configure(fg_color =self.chosen_color)
            self.color_button.configure(fg_color = self.chosen_color,hover_color=self.chosen_color)

        except: 
            pass

    def check_value(self,Event):
        value = self.entry.get()

        try:
            size = int(value)
            if len(value) > 2:
                value = value[len(value) - 2:]
                self.entry.delete(0,END)
                self.entry.insert(0,value)

            self.pixel_size = int(value)
            if self.pixel_size == 0:
                self.pixel_size = 1

            self.entry.delete(0,END)
            self.entry.insert(0,self.pixel_size)

        except:
            self.entry.delete(0,END)
            self.pixel_size = 10
            self.entry.insert(0,self.pixel_size)

    def change_value(self,value):
        if value == 'add':
            if self.pixel_size < 99:
                self.pixel_size = self.pixel_size + 1
        else:
            if self.pixel_size > 1:
                self.pixel_size = self.pixel_size - 1

        self.entry.delete(0,END)
        self.entry.insert(0,str(self.pixel_size))
    
    def draw_config(self,Event):
        if Event.y >= self.y1 and Event.y <= self.y2 and Event.x >= self.x1 and Event.x < self.x2:
            self.canvas.configure(cursor="@Cursor/Pen.cur")
            self.canvas.bind('<B1-Motion>',lambda Event: self.draw_on_image(Event))
        else:
            self.canvas.configure(cursor="")
            self.canvas.unbind('<B1-Motion>')

    def draw_on_image(self,Event):
        x1 = Event.x - (self.pixel_size/2)
        if x1 < self.x1:
            x1 = self.x1

        y1 = Event.y - (self.pixel_size/2)
        if y1 < self.y1:
            y1 = self.y1

        x2 = Event.x + (self.pixel_size/2)
        if x2 > self.x2:
            x2 = self.x2

        y2 = Event.y + (self.pixel_size/2)
        if y2 > self.y2:
            y2 = self.y2

        if Event.y >= self.y1 and Event.y <= self.y2 and Event.x >= self.x1 and Event.x < self.x2:
            drawing = self.canvas.create_oval(x1,y1,x2,y2,fill=self.chosen_color,outline='')
        else:
            self.canvas.unbind('<B1-Motion>')

            
    
    def disable_draw(self):
        try:
            self.canvas.unbind('<Motion>')
            self.canvas.unbind('<Button-1>')
            self.draw_eframe.place_forget()
        except:
            pass

        
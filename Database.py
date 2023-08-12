import sqlite3
import os

class Database():
    def __init__(self):
        if "App.db" not in os.listdir():
            self.db = sqlite3.connect("App.db")

            self.db.execute("CREATE TABLE Folders(Id integer primary key, Name text, Path text, Date text)")
        
        else:
            self.db = sqlite3.connect("App.db")

        self.Folder_path=[]
        self.Folder_names=[]
        self.Folder_date=[]

        self.Images = []

        self.get_folders()
        self.get_images()

    def add_folder(self,Name,Path,Date,Callback):
        self.db.execute(f"INSERT INTO Folders (Name,Path,Date) VALUES(?,?,?)",(Name,Path,Date))
        self.db.commit()

        self.get_folders()
        return Callback()

    def delete_folder(self,Name,Callback):
        self.db.execute(f"DELETE FROM Folders WHERE Name= '{Name}'")
        self.db.commit()

        self.get_folders()
        return Callback()

    def get_folders(self):
        self.Folder_names.clear()
        self.Folder_path.clear()
        self.Folder_date.clear()

        for i in self.db.execute("SELECT * FROM Folders"):
            self.Folder_names.append(i[1])
            self.Folder_path.append(i[2])
            self.Folder_date.append(i[3])

    
    def get_images(self):
        for i in self.Folder_path:
            for x in os.listdir(i):
                if x.endswith(".png") or x.endswith(".PNG") or x.endswith(".jpg") or x.endswith(".JPG") or x.endswith(".jpeg") or x.endswith(".JPEG") :
                    self.Images.append(f"{i}/{x}")

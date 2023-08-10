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

        self.get_folders()

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

    


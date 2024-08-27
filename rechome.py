import spacy
import fitz
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk
from main import LoginPage
import pymysql

class Rechome:
    def __init__(self, root,uname):
        self.root = root
        self.uname=uname
        self.root.title("Recruiter Home Page")
        self.root.geometry("900x600+200+50")
        self.nlp = spacy.load('en_core_web_lg')

        self.bg_frame = tk.Frame(self.root)
        self.bg_frame.place(relwidth=1, relheight=1)

        self.bg_image = ImageTk.PhotoImage(file="rajeshbgrnd.png")
        self.bg_label = tk.Label(self.bg_frame, image=self.bg_image, width=900, height=600)
        self.bg_label.place(relwidth=1, relheight=1)

        self.label_title = tk.Label(root, text="Welcome to Job Platform",bg="#012147", fg="ivory2", font=("Times New Roman", 30))
        self.label_title.pack(pady=20, padx=20)

        self.post_job_btn=tk.Button(root,text="Post Job Vacancy",font=("Times New Roman",20),bg="ivory2",activebackground="#012147",activeforeground="ivory2",command=self.on_press_post)
        self.post_job_btn.pack(pady=35)

        self.del_job_btn=tk.Button(root,text="Remove Job Vacancy",font=("Times New Roman",20),bg="ivory2",activebackground="#012147",activeforeground="ivory2",command=self.on_press_del)
        self.del_job_btn.pack(pady=35)

        self.btn_previous = tk.Button(self.bg_frame, text="<-- Previous", bg="#01254C",fg="white", font=("Times New Roman", 12), command=self.back)
        self.btn_previous.place(x=2, y=2)

        self.find_res_btn=tk.Button(root,text="Find best matching resume",font=("Times New Roman",20),bg="ivory2",activebackground="#012147",activeforeground="ivory2",command=self.on_press_find)
        self.find_res_btn.pack(pady=35)
    
    def on_press_del(self):
        if messagebox.askyesno("Warning","Do you want to remove your posted job vacancy?"):
            self.mycon = pymysql.connect(host='localhost', user='root', password='Titi@2005')
            self.mycursor = self.mycon.cursor()
            self.mycursor.execute("USE all_users")
            self.mycursor.execute("update recruiters set job_desc=NULL where Username=%s",(self.uname))
            self.mycon.commit()
            messagebox.showinfo("Success","Vacancy removed")
        else:
            messagebox("Cancelled","Vacancy not removed")

    def on_press_post(self):
        self.root.destroy()
        import createjob
        createjob.main(self.uname)
        

    def on_press_find(self):
        self.root.destroy()
        import resumecmpr
        resumecmpr.main(self.uname)

    def back(self):
        self.root.destroy()
        import main
        main.main()
    
def main(uname):
    root = tk.Tk()
    root.title("Recruiter Home Page")
    root.geometry("900x600+200+50")
    app=Rechome(root,uname)
    root.mainloop()
if __name__=="__main__":
    uname=LoginPage.log_in()
    main(uname)
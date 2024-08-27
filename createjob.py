import tkinter as tk
from tkinter import  messagebox
from PIL import ImageTk
from main import LoginPage
import pymysql

class createjob:
    def __init__(self, root,uname):
        self.root = root
        self.uname=uname
        self.root.title("Best Matching Resume")
        self.root.geometry("900x600+200+50")
        self.bg_frame = tk.Frame(self.root)
        self.bg_frame.place(relwidth=1, relheight=1)

        self.bg_image = ImageTk.PhotoImage(file="rajeshbgrnd.png")
        self.bg_label = tk.Label(self.bg_frame, image=self.bg_image, width=900, height=600)
        self.bg_label.place(relwidth=1, relheight=1)
        
        tk.Label(self.bg_frame, text="Post Job Vacancy", font=("Times New Roman", 25), bg="ivory2").place(x=330, y=40)

        self.comp_lbl=tk.Label(root,text="Company Name",font=("Times New Roman",17),bg="ivory2")
        self.comp_lbl.place(x=10,y=120)

        self.comp_entry = tk.Entry(self.bg_frame, width=35, font=("Arial", 19), bg="ivory2")
        self.comp_entry.place(x=175, y=120)

        self.job_lbl=tk.Label(root,text="Position",font=("Times New Roman",17),bg="ivory2")
        self.job_lbl.place(x=10,y=220)

        self.job_des_entry = tk.Entry(self.bg_frame, width=35, font=("Arial", 19), bg="ivory2")
        self.job_des_entry.place(x=175, y=220)

        self.vac_lbl=tk.Label(root,text="Vacancies",font=("Times New Roman",17),bg="ivory2")
        self.vac_lbl.place(x=10,y=320)

        self.job_vac_entry = tk.Entry(self.bg_frame, width=35, font=("Arial", 19), bg="ivory2")
        self.job_vac_entry.place(x=175, y=320)

        self.btn_previous = tk.Button(root,text="<-- Previous", bg="#243141",fg="cyan", font=("Times New Roman", 12), command=self.back)
        self.btn_previous.place(x=2,y=2)

        self.btn_post = tk.Button(root,text="POST", bg="#243141",fg="cyan", font=("Times New Roman", 18), command=self.post)
        self.btn_post.place(x=370,y=400)
        

    def back(self):
        self.root.destroy()
        import rechome
        rechome.main(self.uname)
    
    def post(self):
        self.mycon = pymysql.connect(host='localhost', user='root', password='Titi@2005')
        self.mycursor = self.mycon.cursor()
        self.mycursor.execute("USE all_users")
        self.mycursor.execute("select job_desc from recruiters where Username=%s",(self.uname))
        results=self.mycursor.fetchone()
        self.job_des=self.comp_entry.get()+'-'+self.job_des_entry.get()+'-'+self.job_vac_entry.get()
        if results[0] is None:
            self.query="update recruiters set job_desc=%s where Username=%s"
            self.mycursor.execute(self.query,(self.job_des,self.uname))
            self.mycon.commit()
            messagebox.showinfo("Success","Job posted")
        else:
            messagebox.showwarning("Warning","Vacancy already posted for this username")
        
def main(uname):
    root = tk.Tk()
    root.geometry("800x600+300+15")
    app = createjob(root,uname) 
    root.mainloop()

if __name__ == "__main__":
    uname=LoginPage.log_in()
    main(uname)
import tkinter as tk
from tkinter import filedialog,messagebox
from tkinter import PhotoImage, Label
from main import LoginPage
import pymysql
import webbrowser

class JobPlatformHomePage:
    def __init__(self, master,uname):
        self.master = master
        self.uname=uname
        self.master.title("Job Platform")
        self.bg_image = PhotoImage(file="nbgrnd_2.png")
        self.bg_label=Label(self.master,image=self.bg_image)
        self.bg_label.place(x=0,y=0)
     
        self.bg_label = Label(master, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)
       
        self.label_title = tk.Label(master, text="Welcome to Job Platform", bg="#243141",fg="cyan", font=("Helvetica", 30))
        self.label_title.pack(pady=20, padx=20)

        self.btn_display_resume = tk.Button(master, text="Display Resume", bg="#243141", fg="cyan", font=("Times New Roman", 15), command=self.display_resume)
        self.btn_display_resume.place(x=305, y=400) 

        self.btn_view_offers = tk.Button(master, text="View Offers",bg="#243141" ,fg="cyan", font=("Times New Roman", 15), command=self.view_jobs)
        self.btn_view_offers.place(x=320,y=200)

        self.btn_post_job = tk.Button(master, text="Apply Now",bg="#243141", fg="cyan", font=("Times New Roman", 15), command=self.post_job)
        self.btn_post_job.place(x=320,y=300)
        
        self.btn_upload_resume = tk.Button(master, text="Upload Resume", bg="#243141",fg="cyan", font=("Times New Roman", 15), command=self.upload_resume)
        self.btn_upload_resume.place(x=18,y=100)

        self.path = tk.Entry(master, width=40, bg="ivory2", font=("Arial", 15))
        self.path.place(x=185,y=107)

        self.btn_previous = tk.Button(master,text="<-- Previous", bg="#243141",fg="cyan", font=("Times New Roman", 12), command=self.show_login)
        self.btn_previous.place(x=2,y=2)

        self.fillup=PhotoImage(file="company2.png")
        self.fillup_lbl=tk.Label(master,image=self.fillup)
        self.fillup_lbl.place(x=0,y=450)
    def show_login(self):
        self.master.destroy()
        import main
        main.main()
    def upload_resume(self):
        filename = filedialog.askopenfilename()
        if filename:
            try:
                self.mycon = pymysql.connect(host='localhost', user='root', password='Titi@2005')
                self.mycursor = self.mycon.cursor()
                self.mycursor.execute("USE all_users")
                self.mycursor.execute("UPDATE seekers SET resume_path=%s WHERE Username=%s", (filename, self.uname))
                self.mycon.commit()
                messagebox.showinfo("Resume upload", "Resume uploaded successfully")
                self.path.delete(0, tk.END)
                self.path.insert(0, filename)
            except pymysql.Error as e:
                print("Error:", e)
                messagebox.showerror("Error", "An error occurred while uploading the resume.")

    def display_resume(self):
        self.mycon = pymysql.connect(host='localhost', user='root', password='Titi@2005')
        self.mycursor = self.mycon.cursor()
        self.mycursor.execute("USE all_users")
        self.query="select resume_path from seekers where Username=%s"
        self.mycursor.execute(self.query,(self.uname,))
        resume_path=self.mycursor.fetchone()[0]
        if resume_path:
            webbrowser.open(resume_path)
        else:
            messagebox.showwarning("Display Resume", "No resume file path available to display.")

    def view_jobs(self):
        self.master.destroy()
        import viewoffer
        viewoffer.main(self.uname)

    def post_job(self):
        self.master.destroy()
        import apply
        apply.main(self.uname)

def main(uname):
    root = tk.Tk()
    root.geometry("800x600+300+15")
    app = JobPlatformHomePage(root,uname) 
    print(uname)
    root.mainloop()

if __name__ == "__main__":
    uname=LoginPage.log_in()
    main(uname)

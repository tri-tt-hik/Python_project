from tkinter import *
from tkinter import messagebox
import pymysql
from PIL import ImageTk

class LoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Login Page")
        self.bg_image = ImageTk.PhotoImage(file="bgrnd3.png")
        self.bg_label=Label(self.master,image=self.bg_image)
        self.bg_label.place(x=0,y=0,relheight=1,relwidth=1)

        self.uname = Entry(self.master, width=25, font=('Consolas', 14), bg='white', bd=0, fg="grey")
        self.uname.place(x=290, y=352)

        self.password = Entry(self.master, width=25, font=("Consolas", 14), show="*", bg="white", fg="grey", bd=0)
        self.password.place(x=290, y=425)

        self.pwdvisible = False

        self.openeye = PhotoImage(file="openeye.png")
        self.closedeye = PhotoImage(file="closedeye.png")
        self.Ebutton = Button(self.master, image=self.closedeye, bg="white", bd=0, command=self.toggle_pwd, cursor='hand2')
        self.Ebutton.place(x=535, y=420)

        self.fgot_pwd = Button(self.master, width=14, text="Forgot password", font=("Microsoft Yahei UI Light", 12), bg="#316074",
                            bd=0, fg="white", activebackground="#1C4757", cursor="hand2", command=self.fgotpwd)
        self.fgot_pwd.place(x=440, y=482)
        Frame(self.master, width=124, height=1).place(x=445, y=510)

        self.rem_var=IntVar()
        self.rem_checkbutton=Checkbutton(self.master,bg="#407F91",activebackground="#407F91", variable=self.rem_var)
        self.rem_checkbutton.place(x=230,y=484)

        self.seek_var = IntVar()
        self.seek_checkbutton = Checkbutton(self.master, text="SEEKER", font=("Liberation Serif", 10), bg="#407F91",activebackground="#407F91", variable=self.seek_var)
        self.seek_checkbutton.place(x=225, y=300)

        self.rec_var = IntVar()
        self.rec_checkbutton = Checkbutton(self.master, text="RECRUITER", font=("Liberation Serif", 10), bg="#438496",activebackground="#438496", variable=self.rec_var)
        self.rec_checkbutton.place(x=325, y=300)

        self.login = Button(self.master, width=23, text="LOGIN", font=("Microsoft Yahei UI Light", 20), bg="#1C4656", bd=0, fg="white",activebackground="#316074", cursor="hand2", command=self.log_in)
        self.login.place(x=225, y=537)

        self.create = Label(self.master, text="Don't have an account?", font=("Microsoft Yahei UI Light", 12), bg="#2A5568", bd=0,
                        fg="white")
        self.create.place(x=225, y=600)

        self.newaccnt = Button(self.master, text="Create new account", font=("Microsoft Yahei UI Light", 8, "bold"), bg="#2E5D71",
                            bd=0, fg="cyan", activebackground="#2A5568", activeforeground="cyan", cursor="hand2",
                            command=self.create_accnt)
        self.newaccnt.place(x=400, y=600)
        Frame(self.master, width=120, height=1, bg="cyan").place(x=403, y=617)

    def toggle_pwd(self):
        if self.pwdvisible:
            self.closedeye.config(file="closedeye.png")
            self.password.config(show='*')
        else:
            self.closedeye.config(file="openeye.png")
            self.password.config(show='')
        self.pwdvisible = not self.pwdvisible

    def create_accnt(self):
        self.master.destroy()
        import signup
        signup.main()

    def log_in(self):
        u_name=self.uname.get()
        mycon = pymysql.connect(host='localhost', user='root', password='Titi@2005')
        mycursor = mycon.cursor()
        query = 'use all_users'
        mycursor.execute(query)
        if self.seek_var.get() == 1:
            query="select remember from seekers where Username=%s"
            mycursor.execute(query,(u_name))
            result=mycursor.fetchone()
            try:    
                if result[0]==1:
                    mycursor.execute("select password from seekers where Username=%s",(u_name))
                    pwd=mycursor.fetchone()[0] 
                    if self.password.get()=="": 
                        self.password.insert(0,pwd)
                    else:
                        pass
            except:
                messagebox.showerror("Error", "User not found. If you don't have an account, create a new one")    
        elif self.rec_var.get() == 1:
            query="select remember from recruiters where Username=%s"
            mycursor.execute(query,(u_name))
            result=mycursor.fetchone()  
            try:  
                if result[0]==1:
                    mycursor.execute("select password from recruiters where Username=%s",(u_name))
                    pwd=mycursor.fetchone()[0]  
                    if self.password.get()=="": 
                        self.password.insert(0,pwd)
                    else:
                        pass 
            except:
                 messagebox.showerror("Error", "User not found. If you don't have an account, create a new one") 
        if self.uname.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "All fields are required")
        elif self.seek_var.get() == 0 and self.rec_var.get() == 0:
            messagebox.showerror("Error", "Select at least one role")
        elif self.seek_var.get() == 1 and self.rec_var.get() == 1:
            messagebox.showerror("Error", "Select only one role")
        else:
            if self.seek_var.get() == 1:
                query = 'SELECT * from seekers where Username=%s'
            elif self.rec_var.get() == 1:
                query = 'SELECT * from recruiters where Username=%s'
            mycursor.execute(query, (self.uname.get(),))
            result = mycursor.fetchone()
            if result:
                if result[3] == self.password.get():
                    if self.seek_var.get() == 1:
                        if self.rem_var.get()==1:
                            mycursor.execute("update seekers set remember=1 where Username=%s",(u_name))
                            mycon.commit()
                        self.master.destroy()
                        import nithishlogin
                        nithishlogin.main(u_name)
                    elif self.rec_var.get() == 1:
                        if self.rem_var.get()==1:
                            mycursor.execute("update recruiters set remember=1 where Username=%s",(u_name))
                            mycon.commit()
                        self.master.destroy()
                        import rechome
                        rechome.main(u_name)
                else:
                    messagebox.showerror("Error", "Incorrect Password")
            
        return u_name

    def fgotpwd(self):
        self.master.destroy()
        import fgot_pwd

def main():
    root = Tk()
    window_width = 800
    window_height = 700
    root.geometry(f"{window_width}x{window_height}+300+0")
    root.resizable(0, 0)
    LoginPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()

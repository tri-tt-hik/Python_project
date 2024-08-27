from tkinter import *
from tkinter import messagebox
import pymysql
from PIL import ImageTk

class SignUpPage:
    def __init__(self, master):
        self.master = master
        self.master.title("SIGN UP")

        self.w_width = 800
        self.w_height = 700
        self.master.geometry(f"{self.w_width}x{self.w_height}+250+10")
        self.master.resizable(0, 0)
        self.bg_image = ImageTk.PhotoImage(file="accnt.png")
        self.bg_label=Label(self.master,image=self.bg_image)
        self.bg_label.place(x=0,y=0,relheight=1,relwidth=1)

        self.openeye = PhotoImage(file="openeye.png")
        self.closedeye = PhotoImage(file="closedeye.png")

        self.title = Label(master, text="SIGN UP", font=("Microsoft Yahei UI Light", 20), bg="white")
        self.title.pack()

        self.accntimg = ImageTk.PhotoImage(file="accnt.png")
        self.accnt_lbl = Label(master, image=self.accntimg) 
        self.accnt_lbl.place(x=0, y=0)

        self.accnt = Label(master, text="Create Account", font=("Microsoft Yahei UI Light", 25, "bold"), bg="#4B7A80", fg="white", bd=0)
        self.accnt.place(x=260, y=145)

        self.fname = Entry(master, width=25, font=("Microsoft Yahei UI Light", 13), bg="#FFFFFF", fg="grey", bd=0)
        self.fname.insert(0, 'First Name')
        self.fname.bind('<FocusIn>', self.on_press_fname)
        self.fname.place(x=234, y=197)

        self.lname = Entry(master, width=25, font=("Microsoft Yahei UI Light", 13), bg="#FFFFFF", fg="grey", bd=0)
        self.lname.insert(0, 'Last Name')
        self.lname.bind('<FocusIn>', self.on_press_lname)
        self.lname.place(x=234, y=259)

        self.uname = Entry(master, width=25, font=("Microsoft Yahei UI Light", 13), bg="#FFFFFF", fg="grey", bd=0)
        self.uname.insert(0, 'Username')
        self.uname.bind('<FocusIn>', self.on_press_uname)
        self.uname.place(x=234, y=321)

        self.pwdhidden = True
        self.pwd = Entry(master, width=25, font=("Microsoft Yahei UI Light", 13), bg="#FFFFFF", fg="grey", bd=0)
        self.pwd.insert(0, 'Password')
        self.pwd.bind('<FocusIn>', self.on_press_pwd)
        self.pwd.place(x=234, y=385)

        self.cfm_pwdhidden = True
        self.cfm_pwd = Entry(master, width=25, font=("Microsoft Yahei UI Light", 13), bg="#FFFFFF", fg="grey", bd=0)
        self.cfm_pwd.insert(0, 'Confirm Password')
        self.cfm_pwd.bind('<FocusIn>', self.on_press_cfm_pwd)
        self.cfm_pwd.place(x=234, y=450)

        self.email = Entry(master, width=25, font=("Microsoft Yahei UI Light", 13), bg="#FFFFFF", fg="grey", bd=0)
        self.email.insert(0, 'E-mail')
        self.email.bind('<FocusIn>', self.on_press_email)
        self.email.place(x=234, y=513)

        self.canvas = Canvas(master, width=350, height=41, bg="#1E1E36", borderwidth=0, highlightthickness=0)
        self.canvas.place(x=219, y=570)

        self.seek_var = IntVar()
        self.seek_checkbutton = Checkbutton(master, text="SEEKER", font=("Liberation Serif", 10), bg="white", activebackground="white", variable=self.seek_var)
        self.seek_checkbutton.place(x=225 , y=574)

        self.rec_var = IntVar()
        self.rec_checkbutton = Checkbutton(master, text="RECRUITER", font=("Liberation Serif", 10), bg="white", activebackground="white", variable=self.rec_var)
        self.rec_checkbutton.place(x=325, y=574)

        self.alreadyaccnt = Label(master, text="Already have an account? ", font=("Microsoft Yahei UI Light", 11), bg="#1A1B30", fg="white")
        self.alreadyaccnt.place(x=225, y=612)

        self.log_in = Button(master, text="Log In", font=("Microsoft Yahei UI Light", 10), bg="#1A1B30", fg="cyan", activebackground="#1A1B30", activeforeground="red", bd=0, command=self.login_user, cursor="hand2")
        self.log_in.place(x=400, y=611)

        self.create = Button(master, width=18, text="Create Account", font=("Microsoft Yahei UI Light", 15), bd=0, bg="#1A182E", fg="cyan", activebackground="cyan", activeforeground="#1A182E", cursor="hand2", command=self.createaccount)
        self.create.place(x=285, y=636)

    def on_press_fname(self, event):
        if self.fname.get() == "First Name":
            self.fname.delete(0, END)
            self.fname.config(fg="black")

    def on_press_lname(self, event):
        if self.lname.get() == "Last Name":
            self.lname.delete(0, END)
            self.lname.config(fg="black")

    def on_press_uname(self, event):
        if self.uname.get() == "Username":
            self.uname.delete(0, END)
            self.uname.config(fg="black") 

    def on_press_pwd(self, event):
        if self.pwd.get() == "Password":
            self.pwd.delete(0, END)
            self.pwd.config(fg="black")

    def on_press_cfm_pwd(self, event):
        if self.cfm_pwd.get() == "Confirm Password":
            self.cfm_pwd.delete(0, END)
            self.cfm_pwd.config(fg="black")

    def on_press_email(self, event):
        if self.email.get() == "E-mail":
            self.email.delete(0, END)
            self.email.config(fg="black")

    def login_user(self):
        self.master.destroy()
        import main
        main.main()

    def createaccount(self):
        if self.fname.get() in (None, "First Name") or self.lname.get() in (None, "Last Name") or self.uname.get() in (None, "Usename") or self.pwd.get() in (None, "Password") or self.cfm_pwd.get() in (None, "Confirm Password") or self.email.get() in (None, "E-mail"):
            messagebox.showerror("Error", "All fields are required")     
        elif self.cfm_pwd.get() != self.pwd.get():
            messagebox.showerror("Error", "Confirm the correct password")
        elif self.seek_var.get() == 0 and self.rec_var.get() == 0:
            messagebox.showerror("Error", "Select at least one role")
        elif self.seek_var.get() == 1 and self.rec_var.get() == 1:
            messagebox.showerror("Error", "Select only one role")
        else:
            try:
                mycon = pymysql.connect(host='localhost', user='root', password='Titi@2005')
                mycursor = mycon.cursor()
                query = 'USE all_users'
                mycursor.execute(query)
                try:
                    query = 'INSERT INTO allusernames values(%s)'
                    mycursor.execute(query, self.uname.get())
                except:
                    messagebox.showerror("Error", "Username already exists")
                if self.seek_var.get() == 1:
                    query = 'INSERT INTO seekers(First_Name, Last_Name, Username, password, email) VALUES (%s, %s, %s, %s, %s)'
                elif self.rec_var.get() == 1:
                    query = 'INSERT INTO recruiters(First_Name, Last_Name, Username, password, email) VALUES (%s, %s, %s, %s, %s)'
                values = (self.fname.get(), self.lname.get(), self.uname.get(), self.pwd.get(), self.email.get())
                mycursor.execute(query, values)
                mycon.commit()
                messagebox.showinfo("Welcome {}".format(self.uname.get()), "Account created successfully")
                self.login_user()
            except:
                messagebox.showerror("Error", "Something went wrong")


def main():
    root = Tk()
    app = SignUpPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()

from tkinter import *
from tkinter import messagebox
import pymysql
from PIL import ImageTk
import vonage
import random as random
otp=random.randint(1000,10000)
OTP=str(otp)
client = vonage.Client(key="08e48819", secret="xijluqXmZYUv2snO")
sms = vonage.Sms(client)
print(OTP)

responseData = sms.send_message(
    {
        "from": "JOB RECRUITERS",
        "to": "917397403930",
        "text": "OTP: "+OTP,
    }
)

if responseData["messages"][0]["status"] == "0":
    print("Message sent successfully.")
else:
    print(f"Message failed with error: {responseData['messages'][0]['error-text']}")


def on_press_username(event):
    if username.get()=="Username":
        username.delete(0,END)
def on_press_newpwd(event):
    if newpwd.get()=="New Password":
        newpwd.delete(0,END)
def on_press_cfmpwd(event):
    if cfmpwd.get()=="Confirm Password":
        cfmpwd.delete(0,END)

def submit_pwd():
    if username.get()==""or username.get()=="Username" or newpwd.get()=="" or newpwd.get()=="New Password" or  cfmpwd.get()=="" or cfmpwd.get()=="Confirm Password" or otp_entry.get()=="Enter OTP" or otp_entry.get()=="":
        messagebox.showerror("Error","All fields are required")
    elif newpwd.get()!=cfmpwd.get():
        messagebox.showerror("Error","Passwords not matching")
    else:
        mycon=pymysql.connect(host='localhost',user='root',password='Titi@2005')
        mycursor=mycon.cursor()
        query='use all_users' #use database 'users'
        mycursor.execute(query)
        query='select * from seekers where Username=%s'
        mycursor.execute(query, username.get())
        skr = mycursor.fetchone()
        if otp_entry.get()==OTP:

            if skr:
                query = 'update seekers set password=%s where Username=%s'
                mycursor.execute(query, (cfmpwd.get(), username.get()))
                mycon.commit()
            else:
                query = 'update recruiters set password=%s where Username=%s'
                mycursor.execute(query, (cfmpwd.get(), username.get()))
                mycon.commit()
            messagebox.showinfo("Password Change","Password changed successfully")
            root.destroy()
            import main
            main.main()
        else:
            messagebox.showerror("Error","OTP not matching")
        
def on_press_back():
    root.destroy()
    import main
    main.main()
def on_press_otp(event):
    if otp_entry.get()=="Enter OTP":
        otp_entry.delete(0,END)

root = Tk()
window_width = 510
window_height = 510
root.geometry(f"{window_width}x{window_height}+420+115")
root.resizable(0, 0)
root.title("Forgot Password")


bgrnd = ImageTk.PhotoImage(file="fgotpwd.png")
bgrnd_lbl = Label(root, image=bgrnd)
bgrnd_lbl.place(x=0, y=0, relwidth=1, relheight=1)

enter_uname=Label(root,text="Enter Username*",font=("Microsoft Yahei UI Light",14),bg="white",fg="red")
enter_uname.place(x=90,y=120)


enter_nwpwd=Label(root,text="Set New Password*",font=("Microsoft Yahei UI Light",12),bg="white",fg="red")
enter_nwpwd.place(x=90,y=218)

enter_cfmpwd=Label(root,text="Confirm New Password*",font=("Microsoft Yahei UI Light",12),bg="white",fg="red")
enter_cfmpwd.place(x=90,y=310)

username=Entry(root,width=25,font=("Liberation Serif",15),bg="white",bd=0,fg="gray")
username.insert(0,"Username")
username.place(x=100,y=165)
username.bind('<FocusIn>',on_press_username)

newpwd=Entry(root,width=25,font=("Liberation Serif",15),bg="white",bd=0,fg="gray")
newpwd.insert(0,"New Password")
newpwd.place(x=100,y=255)
newpwd.bind('<FocusIn>',on_press_newpwd)

cfmpwd=Entry(root,width=25,font=("Liberation Serif",15),bg="white",bd=0,fg="gray")
cfmpwd.insert(0,"Confirm Password")
cfmpwd.place(x=100,y=345)
cfmpwd.bind('<FocusIn>',on_press_cfmpwd)

otp_entry=Entry(root,width=21,font=("Liberation Serif",22),bg="white",fg="gray")
otp_entry.insert(0,"Enter OTP")
otp_entry.place(x=90,y=400)
otp_entry.bind('<FocusIn>',on_press_otp)

back=Button(root,text="Back",font=("Microsoft Yahei UI Light",10,"bold"),bg="white",fg="#2D80EB",cursor="hand2",bd=0,activeforeground="#2D80EB",activebackground="white",command=on_press_back)
back.place(x=334,y=445)

submit=Button(root,text="Submit Password",font=("Microsoft Yahei UI Light",10,"bold"),bg="white",fg="#2D80EB",cursor="hand2",bd=0,activeforeground="#2D80EB",activebackground="white",command=submit_pwd)
submit.place(x=94,y=445)
root.mainloop()

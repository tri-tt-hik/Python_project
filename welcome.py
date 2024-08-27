from tkinter import *
import pymysql
from PIL import ImageTk

def on_press_login():
    root.destroy()
    import main 
    main.main()
def on_press_signup():
    root.destroy()
    import signup  
    signup.main()  

root = Tk()
root.title("WELCOME")
w_width = 800
w_height = 500
root.geometry(f"{w_width}x{w_height}+250+150")
root.resizable(0, 0)


bgrnd=ImageTk.PhotoImage(file="wel_bgrnd_1.png")
bgrnd_lbl=Label(root, image=bgrnd)
bgrnd_lbl.place(x=0, y=0, relwidth=1, relheight=1)

canvas = Canvas(root, width=400, height=300, bg="#F1F1E7")
canvas.place(x=200, y=90)

welcome = Label(root, text="WELCOME", font=("broadway", 25, "bold"), bg="#F1F1E7", bd=0)
welcome.place(x=320, y=110)

seeker = Button(root, text="LOGIN", font=("copperplate gothic light", 12), bg="#F1F1E7", command=on_press_login)
seeker.place(x=240, y=300)

recruiter = Button(root, text="SIGNUP", font=("copperplate gothic light", 12), bg="#F1F1E7", command=on_press_signup)
recruiter.place(x=450, y=300)

root.mainloop()

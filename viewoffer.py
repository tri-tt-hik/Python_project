import tkinter as tk
from tkinter import messagebox, PhotoImage
from tkinter import ttk
import pymysql

class viewoffer:
    def __init__(self, master, uname):
        self.master = master
        self.uname = uname
        self.master.title("View Offers")
        self.bg_image = PhotoImage(file="nbgrnd_2.png")
        self.bg_label = tk.Label(self.master, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relheight=1, relwidth=1)
       
        self.label_title = tk.Label(master, text="OFFERS RECEIVED", bg="black", fg="cyan", font=("Helvetica", 30))
        self.label_title.pack(pady=20, padx=20)

        self.btn_previous = tk.Button(master, text="<-- Previous", bg="black", fg="cyan", font=("Times New Roman", 12), command=self.show_home)
        self.btn_previous.place(x=2, y=2)

        self.tree = ttk.Treeview(master, columns=("Company", "Position"), show='headings', height=15)
        self.tree.heading("Company", text="Company Name")
        self.tree.heading("Position", text="Position")
        self.tree.column("Company", width=200)
        self.tree.column("Position", width=200)
        self.tree.pack(pady=20)

        self.mycon = pymysql.connect(host='localhost', user='root', password='Titi@2005')
        self.mycursor = self.mycon.cursor()
        self.mycursor.execute("use all_users")
        self.mycursor.execute("select offers from seekers where Username=%s", (self.uname,))
        self.result = self.mycursor.fetchone()
        
        if self.result and self.result[0]:
            self.offerstr = self.result[0].split('-')
            self.offcomp = self.offerstr[0]
            self.offposn = self.offerstr[1]
            self.tree.insert("", "end", values=(self.offcomp, self.offposn))
        else:
            self.tree.insert("", "end", values=("No Offers Yet", "N/A"))

    def show_home(self):
        self.master.destroy()
        import nithishlogin
        nithishlogin.main(self.uname)

def main(uname):
    root = tk.Tk()
    root.geometry("800x600+300+15")
    app = viewoffer(root, uname) 
    print(uname)
    root.mainloop()

if __name__ == "__main__":
    from main import LoginPage
    uname = LoginPage.log_in()
    main(uname)

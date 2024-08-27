import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from main import LoginPage
import pymysql

class Application:
    def __init__(self, master, uname):
        self.master = master
        self.uname = uname
        self.master.title("Job Platform")
        self.bg_image = PhotoImage(file="nbgrnd_2.png")
        self.bg_label = tk.Label(self.master, image=self.bg_image)
        self.bg_label.place(x=0, y=0)
     
        self.bg_label = tk.Label(master, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)
       
        self.label_title = tk.Label(master, text="APPLY FOR JOB", bg="black", fg="cyan", font=("Helvetica", 30))
        self.label_title.pack(pady=20, padx=20)

        self.btn_previous = tk.Button(master, text="<-- Previous", bg="black", fg="cyan", font=("Times New Roman", 12), command=self.show_home)
        self.btn_previous.place(x=2, y=2)

        self.search_label = tk.Label(master, text="Company/Position:", font=("Times New Roman", 14), bg="black", fg="cyan")
        self.search_label.place(x=20, y=90)
        self.search_entry = tk.Entry(master, font=("Times New Roman", 15), bg="ivory2")
        self.search_entry.place(x=180, y=90)
        self.search_btn = tk.Button(master, text="Search", font=("Times New Roman", 12), bg="black", fg="cyan", command=self.search_jobs)
        self.search_btn.place(x=386, y=87)

        self.tree = ttk.Treeview(master, columns=("Company", "Position", "Vacancies"), show='headings', height=15)
        self.tree.heading("Company", text="Company Name")
        self.tree.heading("Position", text="Position")
        self.tree.heading("Vacancies", text="Vacancies")
        self.tree.column("Company", width=200)
        self.tree.column("Position", width=200)
        self.tree.column("Vacancies", width=100)
        self.tree.place(x=100, y=130)

        self.mycon = pymysql.connect(host='localhost', user='root', password='Titi@2005')
        self.mycursor = self.mycon.cursor()
        self.mycursor.execute("USE all_users")
        self.query = "SELECT job_desc FROM recruiters"
        self.mycursor.execute(self.query)
        self.result = self.mycursor.fetchall()

        self.complist = []
        self.desclist = []
        self.vaclist = []
        self.populate_jobs()

        self.comp_name = tk.Label(master, text="Company Name", font=("Times New Roman", 14), bg="black", fg="cyan")
        self.comp_name.place(x=100, y=500)

        self.posn = tk.Label(master, text="Position", font=("Times New Roman", 14), bg="black", fg="cyan")
        self.posn.place(x=100, y=550)

        self.comp_name_entry = tk.Entry(master, font=("Times New Roman", 15), bg="ivory2")
        self.comp_name_entry.place(x=260, y=500)

        self.posn_entry = tk.Entry(master, font=("Times New Roman", 15), bg="ivory2")
        self.posn_entry.place(x=260, y=550)

        self.apply_btn = tk.Button(master, text="Apply Now", font=("Times New Roman", 14), bg="black", fg="cyan", command=self.on_press_apply)
        self.apply_btn.place(x=485, y=525)

    def populate_jobs(self, filter_text=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.complist.clear()
        self.desclist.clear()
        self.vaclist.clear()

        for row in self.result:
            desc = row[0]
            if desc:
                fields = desc.split('-')
                if len(fields) >= 3:
                    company_name = fields[0].strip().lower()
                    position = fields[1].strip().lower()
                    vacancy = fields[2].strip()
                    if filter_text.lower() in company_name or filter_text.lower() in position:
                        self.complist.append(company_name)
                        self.desclist.append(position)
                        self.vaclist.append(vacancy)
                        if vacancy != '0':
                            self.tree.insert("", tk.END, values=(company_name, position, vacancy))
                        
    def search_jobs(self):
        filter_text = self.search_entry.get()
        self.populate_jobs(filter_text)

    def on_press_apply(self):
        self.company = self.comp_name_entry.get()
        self.posn = self.posn_entry.get()
        if self.company.lower() not in self.complist:
            messagebox.showwarning("Warning", "Company name not found")
        elif self.posn.lower() not in self.desclist:
            messagebox.showwarning("Warning", "Entered Position not found")
        else:
            self.description = self.company + "-" + self.posn
            self.query = "UPDATE seekers SET Applied=%s WHERE Username=%s"
            self.mycursor.execute(self.query, (self.description, self.uname))
            self.mycon.commit()
            messagebox.showinfo("Success", "Applied Successfully")

    def show_home(self):
        self.master.destroy()
        import nithishlogin
        nithishlogin.main(self.uname)
        
def main(uname):
    root = tk.Tk()
    root.geometry("800x600+300+15")
    app = Application(root, uname) 
    print(uname)
    root.mainloop()

if __name__ == "__main__":
    uname = LoginPage.log_in()
    main(uname)

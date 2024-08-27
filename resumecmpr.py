import spacy
import fitz
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk
import webbrowser
from main import LoginPage
import pymysql

class ResumeMatcherApp:
    def __init__(self, root,uname):
        self.root = root
        self.uname=uname
        self.root.title("Best Matching Resume")
        self.root.geometry("900x600+200+50")
        self.nlp = spacy.load('en_core_web_lg')

        self.bg_frame = tk.Frame(self.root)
        self.bg_frame.place(relwidth=1, relheight=1)

        self.bg_image = ImageTk.PhotoImage(file="rajeshbgrnd.png")
        self.bg_label = tk.Label(self.bg_frame, image=self.bg_image, width=900, height=600)
        self.bg_label.place(relwidth=1, relheight=1)

        self.btn_previous = tk.Button(self.bg_frame, text="<-- Previous", bg="#01254C",fg="white", font=("Times New Roman", 12), command=self.back)
        self.btn_previous.place(x=2, y=2)
        self.mycon = pymysql.connect(host='localhost', user='root', password='Titi@2005')
        self.mycursor = self.mycon.cursor()
        self.mycursor.execute("use all_users")
        self.mycursor.execute("select job_desc from recruiters where Username=%s",(self.uname))
        self.result=self.mycursor.fetchone()
        self.job_desc=self.result[0].split('-')
        self.vac=self.job_desc[2]
        self.job=self.job_desc[0]+'-'+self.job_desc[1]

        tk.Label(self.bg_frame, text="Find Matching Resume", font=("Times New Roman", 30), bg="#012147", fg="ivory2").place(x=290, y=40)

        tk.Label(self.bg_frame, text="Upload Job Requirements PDF:", font=("Arial", 15), bg="#012147", fg="ivory2").place(x=320, y=140)
        self.job_req_entry = tk.Entry(self.bg_frame, width=35, font=("Arial", 19), bg="ivory2")
        self.job_req_entry.place(x=200, y=170)

        self.browse_job_req_button = tk.Button(self.bg_frame, text="Browse", command=self.browse_job_requirements,
                                               font=("Arial", 10), bg="LightYellow2")
        self.browse_job_req_button.place(x=410, y=220)
        
        browse_resumes_button = tk.Button(self.bg_frame, text="Browse Resumes", command=self.browse_resumes, font=("Arial", 12),bg="LightYellow2")
        browse_resumes_button.place(x=380,y=260)

        self.compare_button = tk.Button(self.bg_frame, text="Compare Resumes", command=self.perform_comparison,
                                        font=("Arial", 12), bg="LightYellow2")
        self.compare_button.place(x=375, y=295)

        self.result_text = tk.Text(self.bg_frame, width=80, height=3, state=tk.DISABLED, bg="ivory2",
                                   font=("Arial", 10))
        self.result_text.place(x=170, y=330)

        self.open_pdf_button = tk.Button(self.bg_frame, text="Open Best Matching Resume", state=tk.DISABLED,
                                         font=("Arial", 12), bg="LightYellow2")
        self.open_pdf_button.place(x=330,y=550)

        self.approve = tk.Button(self.bg_frame, text="Approve aplicant", state=tk.DISABLED,command=self.on_press_approve,
                                               font=("Arial", 10), bg="LightYellow2")
        self.approve.place(x=390, y=500)
    
    def on_press_approve(self):
        self.mycon = pymysql.connect(host='localhost', user='root', password='Titi@2005')
        self.mycursor = self.mycon.cursor()
        self.mycursor.execute("use all_users")
        self.query="select Username from seekers where resume_path=%s"
        self.mycursor.execute(self.query,(self.best_resume))
        self.seluname=self.mycursor.fetchone()[0]
        self.query="update seekers set offers=%s where Username=%s"
        self.mycursor.execute(self.query,(self.job,self.seluname))
        self.mycon.commit()
        self.vac=str(int(self.vac)-1)
        if self.vac=='0':
            self.mycursor.execute("update recruiters set job_desc=NULL where Username=%s",(self.uname))
            self.mycon.commit()
        else:
            self.job_desc=self.job+'-'+self.vac
            self.mycursor.execute("update recruiters set job_desc=%s where Username=%s",(self.job_desc,self.uname))
            self.mycon.commit()
        messagebox.showinfo("Success","Resume Approved")

    def read_pdf(self, file_path):
        pdf_document = fitz.open(file_path)
        text_lines = []
        for page in pdf_document:
            lines = page.get_text("text").split("\n")
            text_lines.extend(lines)
        pdf_document.close()
        return text_lines
    def back(self):
        self.root.destroy()
        import rechome
        rechome.main(self.uname)

    def extract_qualification_work_experience_skillset(self, lines):
        qualifications = []
        work_experience = []
        skillset = []
        for line in lines:
            doc = self.nlp(line.lower())
            for token in doc:   
                if token.text == "education" or token.text == "qualifications" or token.text == "qualification" :
                    qualifications.append(line)
                elif token.text == "experience" or token.text == "experiences":
                    work_experience.append(line)
                skillset.append(line)
        return qualifications, work_experience, skillset

    def calculate_similarity(self, lines1, lines2):
        qualifications1, work_experience1, skillset1 = self.extract_qualification_work_experience_skillset(lines1)
        qualifications2, work_experience2, skillset2 = self.extract_qualification_work_experience_skillset(lines2)
        for i in range(len(lines1)):
            if "skills" in lines1[i].lower():
                break
        skillset1=lines1[i:]
        for i in range(len(lines2)):
            if "skills" in lines2[i].lower():
                break
        skillset2=lines2[i:]
        print("Skillset 1: ",skillset1)
        print("Skillset 2: ",skillset2)
        qual_sim = self.nlp(" ".join(qualifications1)).similarity(self.nlp(" ".join(qualifications2)))
        work_exp_sim = self.nlp(" ".join(work_experience1)).similarity(self.nlp(" ".join(work_experience2)))
        skillset_sim = self.nlp(" ".join(skillset1)).similarity(self.nlp(" ".join(skillset2)))

        return qual_sim * 75, work_exp_sim * 10, skillset_sim * 100

    def browse_resumes(self):
        self.resumes_list = []
        self.mycon = pymysql.connect(host='localhost', user='root', password='Titi@2005')
        self.mycursor = self.mycon.cursor()
        self.mycursor.execute("USE all_users")
        self.query="select Username,resume_path from seekers where Applied=%s"
        self.mycursor.execute(self.query,(self.job))
        self.result=self.mycursor.fetchall()
        if len(self.result)>0:
            for i in self.result:
                file_path=i[1]
                resume_lines = self.read_pdf(file_path)
                self.resumes_list.append((resume_lines, file_path))
            messagebox.showinfo("Success", f"{len(self.result)} resumes loaded successfully!")
        else:
            messagebox.showerror("Error", "No applications for this position")
            self.result_text.delete(1.0,"end")


    def browse_job_requirements(self):
        if self.result is None:
            messagebox.showerror("Warning","No job found for this username")
        else:
            
            file_path = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
            if file_path:
                self.job_req_lines = self.read_pdf(file_path)
                self.job_req_entry.delete(0, tk.END)
                self.job_req_entry.insert(0, file_path)
                messagebox.showinfo("Success", "Job requirements loaded successfully!")

    def perform_comparison(self):
        job_req_path = self.job_req_entry.get()
        if not job_req_path:
            messagebox.showerror("Error", "Please provide job requirements PDF!")
            return
        job_req_lines = self.job_req_lines

        best_similarity = 0
        self.best_resume = None

        for resume_lines, resume_path in self.resumes_list:
            qual_sim, work_exp_sim, skillset_sim = self.calculate_similarity(resume_lines, job_req_lines)
            total_similarity = (qual_sim + work_exp_sim + skillset_sim) / 3
            print(total_similarity)
            if total_similarity > best_similarity:
                print("Inside if block", total_similarity, best_similarity)
                best_similarity = total_similarity
                self.best_resume = resume_path

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        if self.best_resume:
            self.result_text.insert(tk.END, f"Best Matching Resume: {self.best_resume}\nMATCHED PRECENTAGE: {best_similarity}%")
            self.approve.config(state=tk.NORMAL)
            self.open_pdf_button.config(state=tk.NORMAL)
            self.open_pdf_button['command'] = lambda: webbrowser.open(self.best_resume)
        else:
            self.result_text.insert(tk.END, "No matching resume found!\n")
        self.result_text.config(state=tk.DISABLED)

def main(uname):
    root = tk.Tk()
    root.title("Best Matching Resume")
    root.geometry("900x600+200+50")
    app=ResumeMatcherApp(root,uname)
    root.mainloop()
if __name__=="__main__":
    uname=LoginPage.log_in()
    main(uname)



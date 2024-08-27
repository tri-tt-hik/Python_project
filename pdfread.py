import PyPDF2
import tkinter as tk
from tkinter import filedialog, scrolledtext,messagebox


class PDFReader:
    def __init__(self, master, nithishlogin_instance):
        self.master = master
        self.nithishlogin_instance = nithishlogin_instance
        self.master.title("PDF Reader")

        self.open_button = tk.Button(master, text="Click to select PDF", command=self.read_pdf)
        self.open_button.pack(pady=10)

    def read_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            with open(file_path, 'rb') as file:
                


                messagebox.showinfo("Resume","Resume uploaded successfully")

def main():
    root = tk.Tk()
    pdf_reader_instance = PDFReader(root)
    root.mainloop()
if __name__ == "__main__":
    main()
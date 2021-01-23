import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter.filedialog import askopenfile

"""
   Copyright 2020 Pranav Karawale

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


class App:
    """
    App the class containing the GUI and controls' implementation
    """

    window = tk.Tk()
    file = None
    signatureFile = None
    labels = {
        "csvPath": tk.Label(text="Choose CSV File", font=("Segoe UI", 18), pady=10),
        "schoolName": tk.Label(
            text="Enter name of your school", font=("Segoe UI", 18), pady=10
        ),
        "examName": tk.Label(
            text="Enter name of the exam", font=("Segoe UI", 18), pady=10
        ),
        "signatureFile": tk.Label(
            text="Choose signature image (Optional)", font=("Segoe UI", 18), pady=10
        ),
        "authorityName": tk.Label(
            text="Enter the name of the signature holder (Optional; if signature uplaoded)",
            font=("Segoe UI", 18),
            pady=10,
        ),
    }
    inputs = {
        "csvPath": tk.Button(text="Insert CSV File", font=("Segoe UI", 16)),
        "signatureFile": tk.Button(text="Insert Signature File", font=("Segoe UI", 16)),
        "schoolName": tk.Entry(font=("Segoe UI", 18), width=50),
        "examName": tk.Entry(font=("Segoe UI", 18), width=50),
        "authorityName": tk.Entry(font=("Segoe UI", 18), width=50),
    }

    waitLabel = tk.Label(text="")
    csvFileName = tk.Label(text="")
    signatureFileName = tk.Label(text="")

    buttonFrame = tk.Frame(highlightbackground="black", highlightthickness=1, pady=10)

    generateButton = tk.Button(
        master=buttonFrame, text="Generate", font=("Segoe UI", 16)
    )
    closeButton = tk.Button(master=buttonFrame, text="Close", font=("Segoe UI", 16))

    def __init__(self):
        super().__init__()
        self.window.title("Automated Marksheet Generator")
        self.window.geometry("900x700")
        heading = tk.Label(
            text="Automated Marksheet Generator", font=("Segoe UI Bold", 24), pady=5
        )
        heading.pack()

        for key in self.labels.keys():
            self.labels[key].pack()
            if key in self.inputs.keys():
                self.inputs[key].pack()
                if key == "csvPath":
                    self.csvFileName.pack()
                elif key == "signatureFile":
                    self.signatureFileName.pack()

        self.waitLabel.pack()

        self.inputs["csvPath"].bind("<ButtonRelease-1>", self.askForCSVFile)
        self.inputs["signatureFile"].bind("<ButtonRelease-1>", self.askForSignatureFile)
        self.closeButton.bind("<ButtonRelease-1>", self.kill)
        self.generateButton.bind("<ButtonRelease-1>", self.generate)

        self.generateButton.pack(side=tk.LEFT, padx=10)
        self.closeButton.pack(side=tk.LEFT, padx=10)
        self.buttonFrame.pack(side=tk.BOTTOM, fill=tk.X)

    def run(self):
        self.window.mainloop()

    def askForCSVFile(self, event):
        file = askopenfile(
            mode="r", filetypes=[("CSV Files (Comma delimited)", "*.csv")]
        )
        if file is not None:
            self.file = file
            self.csvFileName["text"] = file.name
        else:
            messagebox.showerror("Error", "Please choose another file!!")

    def askForSignatureFile(self, event):
        file = askopenfile(
            mode="r", filetypes=[("PNG Images", "*.png"), ("JPG Images", "*.jpg")]
        )
        self.signatureFileName["text"] = file.name
        self.signatureFile = file

    def kill(self, event):
        self.window.destroy()

    def generate(self, event):
        from src.generator import Generator
        import os

        schoolName = self.inputs["schoolName"].get()
        examName = self.inputs["examName"].get()
        authorityName = self.inputs["authorityName"].get()

        if (not schoolName) and (not examName):
            messagebox.showwarning(
                "Required", "School Name and Exam Name are required!!"
            )
            return
        elif not schoolName:
            messagebox.showwarning("Required", "School Name is required!!")
            return
        elif not examName:
            messagebox.showwarning("Required", "Exam Name is required!!")
            return

        try:
            self.waitLabel["text"] = "Wait..."
            factory = Generator(
                schoolName,
                examName,
                self.file,
                self.signatureFile.name if self.signatureFile else None,
                authorityName,
            )

            if not os.path.isdir("pdfs"):
                os.mkdir("pdfs", 0o666)

            print("Starting to generate PDFs")

            for student in factory.getCSV():
                factory.generatePDF(student["Roll Number"], log=True)
            self.waitLabel["text"] = ""
            messagebox.showinfo("Success!!", "Generated PDFs!! Check the 'pdfs' folder")
        except Exception as e:
            print(e.with_traceback())
            self.waitLabel["text"] = ""
            messagebox.showerror("Error!!", "Something went wrong!! Please try again!!")


if __name__ == "__main__":
    try:
        App().run()
    except Exception as e:
        print(e.with_traceback())
        messagebox.showerror("Error!!", "Something went wrong. Please try again!!")

# Metadata
__author__ = "Pranav Karawale"
__copyright__ = "Copyright 2020, Pranav Karawale"
__credits__ = ["reportlab documentation"]
__license__ = "Apache 2.0"
__maintainer__ = "Pranav Karawale"
__email__ = "pranav.132013007@rfs.edu.in"
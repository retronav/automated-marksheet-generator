import csv
import configparser
from sys import platform

from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.platypus import (
    SimpleDocTemplate,
    Image,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, portrait

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

# Register Segoe UI Normal and Bold font variants
# to use in the PDFs.

fontName = ""

if platform == "win32":
    pdfmetrics.registerFont(TTFont("Segoe UI", "SegoeUI.ttf"))
    pdfmetrics.registerFont(TTFont("Segoe UI Bold", "SegoeUIB.ttf"))
    pdfmetrics.registerFontFamily("Segoe UI", normal="Segoe UI", bold="Segoe UI Bold")
    fontName = "Segoe UI"
elif platform == "darwin":
    pdfmetrics.registerFont(TTFont("Helvetica", "Helvetica.ttf"))
    # there is uncertainty in the font file name
    pdfmetrics.registerFont(TTFont("Helvetica Bold", "HelveticaBold.ttf"))
    pdfmetrics.registerFontFamily(
        "Helvetica", normal="Helvetica", bold="Helvetica Bold"
    )
elif platform == "linux" or platform == "linux2":
    pdfmetrics.registerFont(TTFont("DejaVu", "DejaVu.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVu Bold", "DejaVuBold.ttf"))
    pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu Bold")

# The marks section styling.
# The marks section is actually a table but the
# borders are removed to preserve the minimal look.
TABLESTYLE = lambda length: TableStyle(
    [
        (
            # The FONT command sets the font specified
            "FONT",
            # Apply from first table cell
            (0, 0),
            # Till the end of the table
            (length, length),
            # The font name
            fontName,
            # Font size
            16,
            # Vertical spacing
            10,
        )
    ]
)

with open("./src/schema.ini", "r") as schemafile:
    config = configparser.RawConfigParser()
    config.optionxform = str
    config.read_file(schemafile)
    subjects = config.get("subjects", "subjects")
    # Convert tuple pairs of totalMarks by dict comprehension
    totalMarks = {key: int(value) for key, value in config.items("totalMarks")}

    print(f"Subjects : {subjects}")
    print(f"Total Marks for each subject : {totalMarks}")


class Generator:
    """
    The Generator class is an implementation to create PDFs
    With the feeded data and save it elsewhere.
    """

    schoolname = ""
    examname = ""
    file = None
    signatureFile = None
    authorityName = ""
    __parsedCSV = []
    # List of subjects. See schema.py in this directory for more info
    __subjects = subjects
    # Total marks schema. See schema.py in this directory for more info
    __totalMarks = totalMarks

    def __init__(
        self, schoolname, examname, file, signatureFile=None, authorityName=""
    ):
        """
        Parameters:
        schoolname : The name of the school

        examname : The name of the exam

        file: The CSV file path containing the data

        signatureFile: The path of the image containg an authority's signature(optional)

        authorityName : The name and designation of the authoity whose signature will be
                        embedded (eg, "John Doe, Principal")(optional)
        """
        super().__init__()
        self.schoolname = schoolname
        self.examname = examname
        self.file = file
        self.signatureFile = signatureFile
        self.authorityName = authorityName
        self.__parsedCSV = self.__listify(csv.DictReader(self.file))

    def __listify(self, rawCSV):
        """
        Traverse the dictionary created from the CSV,
        save it in a list and return it
        """
        listifiedCSV = list()
        for dic in rawCSV:
            listifiedCSV.append(dic)
        return listifiedCSV

    def getCSV(self):
        return self.__parsedCSV

    def generatePDF(self, rollNum, log=False):
        """
        Generates the PDF based on the given data

        Parameters:

        rollNum: the roll number of the student whose PDF is to be made
        log=false: whether to log completion status or not
        """
        totalMarks = 0
        obtainedMarks = 0

        targetList = [
            key for key in self.__parsedCSV if key["Roll Number"] == str(rollNum)
        ]
        if len(targetList) == 0:
            raise Exception("Specified Roll Number not found!! Please try again.")
        target = targetList[0]

        for key in target.keys():
            if key in self.__subjects and target[key]:
                totalMarks += self.__totalMarks[key]
                obtainedMarks += int(target[key])

        filename = (
            f"./pdfs/{target['Name'].replace(' ', '.')}-{target['Roll Number']}.pdf"
        )
        doc = SimpleDocTemplate(filename)
        doc.title = f"{target['Name']}'s Marksheet"
        doc.pagesize = portrait(LETTER)

        styles = getSampleStyleSheet()
        content = []
        styles["Normal"].fontName = fontName
        styles["Normal"].fontSize = 18
        styles["Normal"].spaceAfter = 10
        styles["Normal"].spaceBefore = 10

        styles["Heading1"].fontSize = 28
        styles["Heading1"].leading = 30

        styles["Heading2"].fontSize = 24
        styles["Heading2"].leading = 30

        content.append(
            Paragraph(
                f"<font name='Segoe UI'>{self.schoolname}</font>",
                styles["Heading1"],
            ),
        )
        content.append(
            Paragraph(
                f"<font name='Segoe UI'>{self.examname}</font>",
                styles["Heading2"],
            )
        )
        content.append(Spacer(1, 0.75 * inch))
        content.append(
            Paragraph(
                f"Name : {target['Name']}",
                styles["Normal"],
            )
        )
        content.append(
            Paragraph(f"Roll Number : {target['Roll Number']}", styles["Normal"])
        )
        content.append(Spacer(1, 0.5 * inch))
        content.append(Paragraph("Marks :", styles["Normal"]))
        printMarksData = []
        for key, value in target.items():
            if key in self.__subjects and value:
                printMarksData.append(
                    [
                        key,
                        Paragraph(
                            f"<b>{value} / {self.__totalMarks[key]}</b>",
                            styles["Normal"],
                        ),
                    ]
                )

        marksTable = Table(printMarksData, colWidths="*")
        marksTable.setStyle(TABLESTYLE(len(printMarksData)))
        content.append(marksTable)

        content.append(Spacer(1, 0.5 * inch))

        overallData = []
        overallData.append(
            [
                "Total Marks Obtained",
                Paragraph(
                    f"<b>{obtainedMarks} / {totalMarks}</b>",
                    styles["Normal"],
                ),
            ]
        )
        overallData.append(
            [
                "Percentage",
                Paragraph(
                    f"<b>{(obtainedMarks / totalMarks) * 100:.2f}%</b>",
                    styles["Normal"],
                ),
            ]
        )
        overallTable = Table(overallData)
        overallTable.setStyle(TABLESTYLE(len(overallData)))
        content.append(overallTable)

        content.append(Spacer(1, 1 * inch))
        if self.signatureFile is not None:
            image = Image(
                self.signatureFile,
                width=3 * inch,
                height=1 * inch,
                kind="proportional",
            )
            image.hAlign = "LEFT"
            content.append(image)
        if self.authorityName is not None:
            styles["Normal"].fontSize = 16
            content.append(Paragraph(self.authorityName, styles["Normal"]))

        if log:
            print(f"Saved {target['Name']}'s Marksheet in {filename}")
        doc.build(content)


# Metadata
__author__ = "Pranav Karawale"
__copyright__ = "Copyright 2020, Pranav Karawale"
__credits__ = ["reportlab documentation"]
__license__ = "Apache 2.0"
__maintainer__ = "Pranav Karawale"
from io import BytesIO
from os import path
import os
from re import escape
from util.log import log
from jinja2 import Template
from util.constants import template_dir
from pyppeteer import launch
from pdfrw import PdfFileReader, PdfFileWriter
import json

email_info_file_path = "./pdfs/emails.json"


async def generate_pdf(template_data):
    # Create the 'pdfs' folder if it does not exist
    os.makedirs("pdfs", exist_ok=True)
    # Dictionary used to store email and PDF metadata for further storage
    email_info = {}
    log("Start generating PDFs")
    for data in template_data:
        log(f'Generating Report card of {data["student"]["Name"]}')
        with open(path.join(template_dir, "report.html"), "r") as file:
            template = Template(file.read())
            file.close()
        report_html = template.render(data)
        browser = await launch()
        page = await browser.newPage()
        await page.goto("data:html,charset=utf8,<p>Hi</p>")
        await page.evaluate(f"document.write(`{escape(report_html)}`)")
        pdf = await page.pdf(headerTemplate='<h1 class="title">Test PDF</h1>')
        pdf_reader = PdfFileReader(BytesIO(pdf))
        # Add metadata to the PDF.
        pdf_reader.Info.Title = data["student"]["Name"] + "'s Report Card"
        pdf_file_name = "./pdfs/{}.pdf".format(
            data["student"]["Name"].replace(" ", ".")
            + "-"
            + str(data["student"]["RollNo"])
        )
        with open(pdf_file_name, "wb+") as file:
            PdfFileWriter(file, trailer=pdf_reader).write()
            file.close()
        await browser.close()
        log(f"Wrote PDF to {pdf_file_name}")
        if data["student"].get("Email", "") != "":
            # Store email and some metadata in a key-value pair
            email_info[data["student"]["Email"]] = {
                "name": data["student"]["Name"],
                "exam": data["examName"],
                "authority": data["authority"],
                "school": data["schoolName"],
                "file": pdf_file_name,
            }

    email_info_file = open(email_info_file_path, "w+")
    json.dump(email_info, email_info_file, indent=2)
    email_info_file.close()
    log(f"Saved email metdata at {email_info_file_path}")

    log("Done generating PDFs")

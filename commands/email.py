from email.mime.base import MIMEBase
from os import path
import traceback
import click
from util.print_pdf import email_info_file_path
import json
from jinja2 import Template
from util.constants import template_dir, config_dir
import yaml
import sys
from util.log import error, log
import smtplib
from getpass import getpass
from email.message import Message
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


@click.command(
    help="Subcommand to send genrated report cards to the students' respective email addresses."
)
@click.option(
    "-m",
    "--method",
    help="Specify the method to send emails. Allowed values are : outlook (Windows only), smtp.",
)
def email(method):
    with open(path.join(config_dir, "email.yml"), "r") as file:
        email_config = yaml.safe_load(file)
        file.close()

    with open(email_info_file_path, "r") as file:
        email_info = json.load(file)
        file.close()

    with open(path.join(template_dir, "email.html"), "r") as file:
        email_template = Template(file.read())
        file.close()

    email_methods = {
        "outlook": outlook_send,
        "smtp": smtp_send,
    }
    if not method:
        error(
            "No method specified. Run this command again with the method specified with the '-m' flag.",
            2,
        )
    # Check if method is valid
    if method in email_methods.keys():
        email_methods[method](email_info, email_config, email_template)
    else:
        error(
            "Method specified does not exist. Please run the command with --help flag.",
            1,
        )


def outlook_send(email_data, email_config, email_template):
    if sys.platform != "win32":
        error(
            "you are attempting to use Outlook on a non-Windows system. Please use SMTP instead."
        )
    else:
        import win32com.client as win32

        outlook = win32.gencache.EnsureDispatch("Outlook.Application")
        for email, data in email_data.items():
            mail = outlook.CreateItem(0)
            mail.To = email
            if email_config.get("cc"):
                mail.CC = ",".join(email_config["cc"])
            mail.Subject = f'Report Card of {data["exam"]}'
            mail.HTMLBody = email_template.render(**data)
            mail.Attachments.Add(Source=path.abspath(data["file"]))
            log(f"Sending report card to {email}")
            try:
                mail.Send()
                log(f"Sent report card to {email}")
            except Exception as e:
                traceback.print_exc()
                error(f"Could not send email to {email}", 1)


def smtp_send(email_data, email_config, email_template):
    smtp_config = email_config.get("smtp", {})
    if smtp_config == {}:
        error("SMTP settings are missing. Add them in config/email.yml")
    # The get method is not used so that if any required credentials are not
    # present, the program will exit on its own.
    cnx = smtplib.SMTP(host=smtp_config["host"], port=smtp_config["port"])
    try:
        cnx.connect()
        cnx.ehlo()
    except Exception as e:
        traceback.print_exc()
        error("Could not connect to the SMTP server", 1)
    password = getpass("Enter your email password: ")
    try:
        cnx.starttls()
        cnx.login(user=smtp_config["user"], password=password)
    except Exception as e:
        traceback.print_exc()
        error("Could not login with the provided credentials", 1)
    for email, data in email_data.items():
        msg = Message()
        msg["From"] = smtp_config["user"]
        msg["To"] = email
        msg["Subject"] = f'Report Card of {data["exam"]}'
        if email_config.get("cc"):
            msg["CC"] = ",".join(email_config["cc"])
        msg.add_header("Content-Type", "text/html")
        msg.set_payload(email_template.render(**data))

        pdf_file = open(data["file"], "rb")
        pdf_payload = MIMEApplication(pdf_file.read(), _subtype="pdf")
        pdf_payload.add_header(
            "Content-Disposition", "attachment", filename=path.basename(data["file"])
        )
        msg.attach(pdf_payload)
        log(f"Sending report card to {email}")
        try:
            cnx.send_message(msg)
            log(f"Sent report card to {email}")
        except Exception as e:
            traceback.print_exc()
            error(f"Could not send email to {email}", 1)

from util.log import log, error
import click
from os import path
import yaml
import csv
import mysql.connector
from util.print_pdf import generate_pdf
from util.constants import config_dir
import asyncio
import base64


@click.command(help="Subcommand to generate report cards.")
@click.option(
    "-s",
    "--source",
    default="csv",
    help="Sets the source for fetching students' data. Allowed values are 'mysql'/'csv'",
)
def generate(source):
    if source not in ["mysql", "csv"]:
        error(
            "invalid value passed to argument 'source'. Run command with --help to know more"
        )
        exit(2)
    with open(path.join(config_dir, "generate.yml"), "r") as file:
        generator_config = yaml.safe_load(file.read())
        file.close()
    with open(path.join(config_dir, "marks.yml"), "r") as file:
        marks_config = yaml.safe_load(file.read())
        file.close()

    csv_file_path = generator_config["dataFile"]
    # Fetch data according to source
    if source == "csv":
        student_data = get_student_data_csv(csv_file_path, marks_config["maxMarks"])
    elif source == "mysql":
        student_data = get_student_data_mysql(marks_config["maxMarks"])
    student_data = sorted(student_data, key=lambda x: x["RollNo"])
    signature_b64 = ""
    # Check if signatureFile parameter actually exists
    if generator_config["authority"].get("signatureFile", "") != "":
        image = open(
            path.join(config_dir, generator_config["authority"]["signatureFile"]), "rb"
        )
        # Encode image to base64 to directly embed it in HTML using data: protocol.
        signature_b64 = str(base64.encodebytes(image.read()), "utf8")
        image.close()
    template_data = [
        {
            "schoolName": generator_config["schoolName"],
            "examName": generator_config["examName"],
            "authority": generator_config["authority"],
            "maxMarks": marks_config["maxMarks"],
            "student": student,
            "signatureFileURL": signature_b64,
        }
        for student in student_data
    ]
    student_data = [calculate_percentage(x) for x in template_data]
    # Since printPDF is asynchronous and we want to run in a blocking manner,
    # we have to use asyncio.
    asyncio.get_event_loop().run_until_complete(generate_pdf(template_data))


def get_student_data_csv(csvFilePath, subjects):
    log("Fetching and preparing data")
    with open(path.join(config_dir, csvFilePath), "r") as file:
        # Passing the file descriptor directly to the reader
        # works. If the CSV is passed using file.read(), then
        # it is not parsed in the correct manner (just spits out all characters).
        reader = csv.DictReader(file)
        student_data = list(reader)
        for i, entry in enumerate(student_data):
            mutated_entry = entry.copy()
            mutated_entry.setdefault("subjects", {})
            for key in entry.keys():
                # Convert marks string to int.
                if key in subjects.keys() and mutated_entry[key] != "":
                    if int(entry[key]) > subjects[key]:
                        error(
                            f'gained marks of {key} of student {entry["Name"]} are more than the total possible marks',
                            1,
                        )
                    # Nest all subject values into a "subjects" field
                    mutated_entry["subjects"][key] = int(mutated_entry[key])
                    del mutated_entry[key]
                else:
                    # Remove fields that are not excluded from deletion
                    if entry[key] == "":
                        del mutated_entry[key]
            # Replace entry by mutatedEntry
            student_data[i] = mutated_entry.copy()

        file.close()
    log("Done preparing data")
    return student_data


def get_student_data_mysql(subjects):
    log("Fetching and preparing data")
    with open(path.join(config_dir, "mysql.yml"), "r") as file:
        mysql_config = yaml.safe_load(file.read())
        file.close()
    cnx = mysql.connector.connect(
        user=mysql_config["username"],
        password=mysql_config["password"],
        database=mysql_config["database"],
    )
    if not cnx.is_connected():
        click.echo("ERROR: could not connect to database.")
        exit(1)
    cur = cnx.cursor(dictionary=True)
    query = f"SELECT * FROM {mysql_config['table']};"
    cur.execute(query)

    student_data = [row for row in cur]
    # Remove fields with null values
    for i, entry in enumerate(student_data):
        student_data[i] = {k: v for k, v in entry.items() if v}
    for i, entry in enumerate(student_data):
        mutated_entry = entry.copy()
        mutated_entry.setdefault("subjects", {})
        for key in entry.keys():
            if key in subjects.keys():
                # Nest all subject values into a "subjects" field
                mutated_entry["subjects"][key] = mutated_entry[key]
                del mutated_entry[key]
            elif bool(entry[key]) == False:
                del mutated_entry[key]
        # Replace entry by mutatedEntry
        student_data[i] = mutated_entry.copy()

    cnx.close()
    log("Done preparing data")
    return student_data


def calculate_percentage(data):
    total_possible_marks = 0
    total_gained_marks = 0
    for subject, marks in data["student"]["subjects"].items():
        total_gained_marks += marks
        total_possible_marks += data["maxMarks"][subject]
    percentage = total_gained_marks * 100 / total_possible_marks
    data["student"]["total"] = total_gained_marks
    data["maxMarks"]["total"] = total_possible_marks
    # Round the percentage to 2 decimal places
    data["student"]["percentage"] = round(percentage, 2)
    return data

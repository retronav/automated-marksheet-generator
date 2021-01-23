import configparser
import colorama
import ast
from colorama import Fore

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

colorama.init()


def color_print(PREFIX, s):
    print(PREFIX + s + Fore.RESET)


color_print(Fore.CYAN, "Welcome to Generator Schema customiser!!")

print(
    """
Options:
    0 : Quit
    1 : Add new subject
    2 : Remove a subject
"""
)

choice = int(input("Enter your choice: "))

while not -1 < choice < 3:
    color_print(
        Fore.LIGHTRED_EX, "Wrong choice!! Please enter the right option again!!"
    )
    choice = int(input("Enter your choice: "))

if choice == 0:
    exit(0)

config = configparser.RawConfigParser()
config.optionxform = str

with open("./src/schema.ini", "r") as schemafile:
    config.read_file(schemafile)

original_sub = ast.literal_eval(config.get("subjects", "subjects"))

if choice == 1:
    subname = input(
        "Enter the new subject name(eg. Chemistry)(Capitalize first letter) : "
    )
    while not subname:
        subname = input(
            "Enter the new subject name(eg. Chemistry)(Capitalize first letter) : "
        )
    total_marks_for_sub = int(
        input("Enter the total possible marks for the subject(eg. 80): ")
    )
    while not total_marks_for_sub:
        total_marks_for_sub = int(
            input("Enter the total possible marks for the subject(eg. 80): ")
        )
    original_sub.append(subname)
    config.set("subjects", "subjects", str(original_sub))
    config.set("totalMarks", subname, total_marks_for_sub)

    with open("./src/schema.ini", "w") as schemafile:
        config.write(schemafile)
        color_print(Fore.LIGHTGREEN_EX, f"Subject {subname} added successfully")

elif choice == 2:
    subname = input("Enter the subject name to be removed(eg. Chemistry) : ")
    while not subname:
        subname = input("Enter the subject name to be removed(eg. Chemistry) : ")
    if subname in original_sub and config.has_option("totalMarks", subname):
        original_sub.remove(subname)
        config.set("subjects", "subjects", str(original_sub))
        config.remove_option("totalMarks", subname)
        with open("./src/schema.ini", "w") as schemafile:
            config.write(schemafile)
            color_print(Fore.LIGHTGREEN_EX, f"Subject {subname} removed successfully")
    else:
        color_print(Fore.LIGHTRED_EX, "Subject not present!! Terminating program...")


else:
    # This block will never run
    pass


# Metadata
__author__ = "Pranav Karawale"
__copyright__ = "Copyright 2020, Pranav Karawale"
__credits__ = ["reportlab documentation"]
__license__ = "Apache 2.0"
__maintainer__ = "Pranav Karawale"
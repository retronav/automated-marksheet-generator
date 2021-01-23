# Automated Marksheet Generator

# Table Of Contents

1. [Installation](#installation)

   - [Requirements](#requirements)
   - [Setting the virtual enviornment](#setting-the-virtual-enviornment)

2. [Usage](#usage)

   - [Structuring data](#structuring-data)
   - [Exporting data as CSV](#exporting-data-as-csv)
   - [Running the generator](#running-the-generator)

3. [Future Development](#future-development)

# Installation

## Requirements

- You must have Python >=3.8 installed on your PC.
- Also check whether you have `pipenv` installed. If it's not, run the following command:
  `pip install pipenv`

## Setting the virtual enviornment

After cloning the project, run `pipenv shell` to create a pipenv virtual enviornment. After initialising the virtual enviornment, run `pipenv install` to install the dependencies. After successfully installing the dependencies, you can run the generator. Happy hacking :)

# Usage

## Structuring the data

The generator will require data aligned with a predefined schema so that it will detect all the necessary data. The schema is as follows:

---

| Roll Number | Name  | Physics | Chemistry | Math | English | Biology | CS  |
| ----------- | ----- | ------- | --------- | ---- | ------- | ------- | --- |
| 1           | Name1 | 50      | 60        | 50   | 50      |         | 50  |

---

- If a particular student isn't enrolled in a subject, you can keep the cell blank as shown in the above table.
- To add, remove, or modify subjects, run `py util/change-schema.py`

## Exporting data as CSV

### Microsoft Excel

1. In the File tab, click 'Save As'
2. In the file save prompt, enter the name of the file with the .csv extension(eg. `filename.csv`) and select 'CSV (Comma Delimited)' in the file type

## Running the generator

Open a terminal window in this folder and run `py app.py`

# Future Development

NOTE: This project was created as a part of my academic session.

This project can still have more features, but it will probably be worked out in my next academic year. But still, if you are willing to contribute, open a pull request at the [GitHub repository](https://github.com/obnoxiousnerd/automated-marksheet-generator) or if something's broken, open an issue there.

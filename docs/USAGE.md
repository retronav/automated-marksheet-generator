# Usage

# Editing the configuration files

## General Information

If you open the `config` folder, you'll see some files:

1. `email.yml` : This file contains settings for the emailing aspect of the CLI. Outlook specific settings are to be defined under `outlook` field and SMTP settings in the `smtp` field.
2. `generate.yml` : This file contains settings about the school name, exam name, the issuing authority's information required for generating report cards.
3. `marks.yml` : This file contains the values of maximum possible marks of all possible subjects. You should declare all subjects and their max marks in this file for report cards to be properly generated.
4. `mysql.yml` : If you want to load the students' data from a MySQL database instead of a CSV file, you can specify the connection settings for the database in this file.

The above files are written in a language called YAML. So you might need to [take a look]() at the syntax to be comfortable with configuring the CLI.

You will also notice some more files there :

1. `data.csv` : This file contains some mock data for representation, which will be used for generating PDFs. You should replace this file's contents with another CSV file which has the real data. **Don't forget to keep a backup of the real data if things go wrong.**
2. `signature.png` : This file contains a mock signature which will be inserted into report cards. You should replace this with the real signature of the authority concerned. Make sure that the image is not more than 300x150 pixels in size. **It should be in PNG format only.** If you don't want a signature in the report cards, put a "#" before the signatureFile line in `config/generate.yml`.

## Customising the generator

1. In `config/generate.yml`, change `schoolName`, `examName` to suit your needs. You should also change `name` and `designation` field of `authority` to suit your needs.
2. In `config/marks.yml`, you can add, remove, or change subjects and their marks as needed. You should capitalise the subject name and use the same as the heading for the column of marks of that subject in the CSV file.
3. In `config/email.yml`, you can add or remove emails that are to be added as CC in the email. Note that the option is commented by default. You can un-comment and add emails in it for it to work.
4. Replace `data.csv` with the CSV file with the real data, and rename that file again to `data.csv`. Do the same for `signature.png`, except replace it with the signature of the authority in PNG format.

# Templates

rep uses templates to generate report cards and emails so that you can edit them to whatever type you want. Templates are rendered using Jinja2, so it will be good if you take a look at their [documentation]() if you plan on customising the templates.

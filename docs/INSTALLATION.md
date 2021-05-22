# Install the CLI

## Requirements

You need to have the following things installed on your system:

1. Python 3.8 or any higher, compatible version, along with `pip`, the Python package manager
2. pipenv; To install, run the following command : `pip install pipenv`

I will also be great if you have Git, the versioning system installed on your system.

## Downloading the code

### With Git

Run the following commands to get the CLI downloaded on your system:

```
git clone https://github.com/obnoxiousnerd/automated-marksheet-generator.git

cd automated-marksheet-generator
```

### Without Git

Go to the repository (https://github.com/obnoxiousnerd/automated-marksheet-generator) and click on the "Code" button. Then select "Download ZIP". A ZIP file containing the source code will be downloaded. Unzip the file to a folder and keep a terminal window ready in that folder.

## Setting everything up

### Preparing a virtual environment

To prepare a virtual environment, you need to have `pipenv` installed on your system. To check if you have `pipenv` installed, run the command :

```
pipenv --version
```

If the command gives an error, you can use the following command to install `pipenv`:

```
pip install pipenv
```

After these steps, we are ready to create the virtual environment. Make sure a terminal window is open inside the folder where the code is. To create a virtual environment, run the command:

```
pipenv shell
```

Make sure that you're connected to the Internet for the next step. To install all dependencies required, run the following command:

```
pipenv install
```

This might take several minutes, so wait for it to finish

You have successfully created a virtual environment! Now every time when you open a new terminal window in the folder to use the CLI, make sure you run that command before using the CLI.

## Using the CLI

Move on to the [Usage](./USAGE.md) section to read the guide on how to use the CLI.

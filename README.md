# KTP Extractor Using Python and Tesseract

## Installation

Install Tesseract and Indonesian Tesseract Language Model on your machine

See : https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html

Clone this repository and enter the folder:

```sh
cd ktp-extractor
```

Create virtual environment:

```sh
python -m venv env
```

Run virtual environment (for Windows user):

```sh
env\Scripts\activate.bat
```

Run virtual environment (for Unix user):

```sh
source ./env/bin/activate
```

Install dependencies:

```sh
pip install -r requirements.txt
```

Set FLASK_APP (for Windows user only):

```sh
set FLASK_APP=app.py
```

Run project:

```sh
python -m flask run
```

## Endpoint Documentation

| URL          | Parameter | Type                   |
| ------------ | --------- | ---------------------- |
| /extract_ktp | img       | image (jpg, jpeg, png) |

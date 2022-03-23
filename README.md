# KTP Extractor Using Python and Tesseract

## Installation

Clone this repository and enter the folder:

```sh
cd ktp-extractor
```

Create virtual environment:

```sh
python -m venv env
```

Run virtual environment:

```sh
env\Scripts\activate.bat
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

| URL | Parameter | Type |
| --- | --------- | ---- |
| /extract_ktp | img | image (jpg, jpeg, png) |

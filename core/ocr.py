import json
from flask import request, Response

from ktpocr.extractor import KTPOCR

def allowed_format(filename):
    allow = ["JPEG", "JPG", "PNG"]

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in allow:
        return True
    else:
        return False

def extract_ktp():
    if request.method == "POST":
        image = request.files["img"]

        if image.filename == "":
            return {
                'success': False,
                'message': 'Empty Fields!'
            }

        if allowed_format(image.filename):
            temp_path = '/tmp/image.png'
            image.save(temp_path)

            ocr = KTPOCR(temp_path)

            data = {
                'success': True,
                'message': "Extracted successfully",
                'data': ocr.res()
            }

            return return_json(data)

        else:
            data = {
                'success': False,
                'message': 'File not allowed!'
            }

            return return_json(data)

    else:
        data = {
            'success': False,
            'message': 'Method not allowed!'
        }

        return return_json(data)

def return_json(data):
    json_data = json.dumps(data, sort_keys=False)
    return Response(json_data, content_type='application/json')
import cv2
import numpy as np
from flask import request, jsonify
import pytesseract as pt
import re


def allowed_format(filename):
    allow = ["JPEG", "JPG", "PNG"]

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in allow:
        return True
    else:
        return False


def word_to_number_converter(word):
    word_dict = {
        "L": "1",
        'l': "1",
        'O': "0",
        'o': "0",
        '?': "7"
    }

    res = ''
    for letter in word:
        if letter in word_dict:
            res += word_dict[letter]
        else:
            res += letter
    return res


def extract_ktp():
    if request.method == "POST":
        image = request.files["img"]

        if image.filename == "":
            return {
                'success': False,
                'code': '91',
                'message': 'Empty Fields!'
            }

        if allowed_format(image.filename):
            img = cv2.imdecode(np.fromstring(
                image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            threshed = cv2.threshold(
                gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            noised = cv2.medianBlur(threshed, 5)
            result = pt.image_to_string((noised))
            # result.replace('\n', ' ')

            if 'NIK' in result and 'Nama' in result and 'Lahir' in result and 'Jenis kelamin' in result and 'Alamat' in result:
                for word in result.split("\n"):
                    if "NIK" in word:
                        word = word.split(':')
                        nik = word_to_number_converter(
                            word[-1].replace(" ", ""))
                        continue
                    if "Nama" in word:
                        word = word.split(':')
                        nama = word[-1]
                    if "Lahir" in word:
                        word = word.split(':')
                        tgl_lahir = re.search(
                            "([0-9]{2}\-[0-9]{2}\-[0-9]{4})", word[-1])[0]
                        tmp_lahir = word[-1].replace(tgl_lahir, '')
                        continue
                    if 'Darah' in word:
                        jenis_kelamin = re.search(
                            "(LAKI-LAKI|LAKI|LELAKI|PEREMPUAN)", word)[0]
                        word = word.split(':')

                return jsonify({
                    'success': True,
                    'file': image.filename,
                    'data': {
                        'nik': nik,
                        'nama': nama,
                        'tanggal_lahir': tgl_lahir,
                        'tempat_lahir': tmp_lahir,
                        'jenis_kelamin': jenis_kelamin
                    }
                })

            elif 'NIK' in result:
                return jsonify({
                    'success': False,
                    'code': '92',
                    'message': 'Image blur or less resolution!',
                    'rawData': result
                })
            else:
                return jsonify({
                    'success': False,
                    'code': '93',
                    'message': 'File not readable!'
                })

        else:
            return jsonify({
                'success': False,
                'code': '94',
                'message': 'File not allowed!'
            })

    else:
        return jsonify({
            'success': False,
            'code': '99',
            'message': 'Method not allowed!'
        })

import core.ocr as model
from flask import jsonify


class Router:
    @staticmethod
    def run(app):
        @app.route('/')
        def home():
            return jsonify({
                'success': True,
                'code': '00',
                'message': 'KTP Extractor'
            })

        @app.route('/api/v1/extract_ktp', methods=['POST'])
        def extract_ktp():
            return model.extract_ktp()

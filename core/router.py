import core.ocr as model
from flask import jsonify

class Router:
    @staticmethod
    def run(app):
        @app.route('/api/v1')
        def home():
            return jsonify({
                'success': True,
                'message': 'KTP Extractor'
            })

        @app.route('/api/v1/extract_ktp', methods=['POST'])
        def extract_ktp():
            return model.extract_ktp()

import logging
from flask import Flask
from core.router import Router
from flask_cors import CORS

logging.basicConfig(filename='app.log', level=logging.DEBUG)

app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

Router.run(app)

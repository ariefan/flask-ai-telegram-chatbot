from flask import Flask
from dotenv import load_dotenv
from os import environ
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

from .home import *

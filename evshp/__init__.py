from flask import Flask
from pymongo import MongoClient
import os

app = Flask(__name__)
app.config.update(
    TESTING=True,
    SECRET_KEY=os.environ.get("SECRET_KEY")
)
db = MongoClient().evshp

import evshp.views
import evshp.backend.api_v1
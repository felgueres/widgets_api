from flask import Flask, render_template
from dotenv import load_dotenv
from flask_cors import CORS
from widgets import core_bp
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
CORS(app)

app.register_blueprint(core_bp)

@app.errorhandler(404)
@app.errorhandler(400)
def page_not_found(_):
    return render_template('404.html')
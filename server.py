import os
import diff
from difflib import Differ

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

UPLOADS_FOLDER = 'uploads/'

load_dotenv()
app = Flask(__name__)


def fetch_file(file):
    file_path = os.path.join(UPLOADS_FOLDER, secure_filename(file.filename))
    file.save(file_path)
    with open(file_path) as f:
         text = f.read()
    return text


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    data = request.form.to_dict()
    html_diff = diff.textDiff(**data)
    return render_template('index.html', html1=data['html1'], html2=data['html2'], html_diff=html_diff)


if __name__ == '__main__':
    host = os.environ.get('HOST')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port, debug=True)

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
        with open(os.path.join(UPLOADS_FOLDER, 'txt1.html')) as f:
            html1 = f.read()
        with open(os.path.join(UPLOADS_FOLDER, 'txt2.html')) as f:
            html2 = f.read()
        html_diff = diff.textDiff(html1, html2)
        return render_template('index.html', html1=html1, html2=html2, html_diff=html_diff)
    file1 = request.files['file1']
    file2 = request.files['file2']
    if secure_filename(file1.filename) == '' or secure_filename(file2.filename) == '':
        return render_template('index.html', err='Please choose two files for comparing')
    html1 = fetch_file(file1)
    html2 = fetch_file(file2)
    html_diff = diff.textDiff(html1, html2)
    return render_template('index.html', html1=html1, html2=html2, html_diff=html_diff)

if __name__ == '__main__':
    host = os.environ.get('HOST')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port, debug=True)


from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
FLIPBOOK_FOLDER = 'static/flipbooks'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FLIPBOOK_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf = request.files['pdf_file']
        title = request.form['title'].strip().replace(" ", "_")
        if pdf and title:
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{title}.pdf")
            pdf.save(pdf_path)

            output_dir = os.path.join(FLIPBOOK_FOLDER, title)
            os.makedirs(output_dir, exist_ok=True)
            subprocess.run(['pdf2htmlEX', pdf_path, os.path.join(output_dir, 'index.html')])

            return redirect(url_for('gallery'))
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    flipbooks = {}
    for name in os.listdir(FLIPBOOK_FOLDER):
        index_path = os.path.join(FLIPBOOK_FOLDER, name, "index.html")
        if os.path.exists(index_path):
            flipbooks[name.replace("_", " ")] = f"/static/flipbooks/{name}/index.html"
    return render_template('gallery.html', flipbooks=flipbooks)

if __name__ == '__main__':
    app.run(debug=True)

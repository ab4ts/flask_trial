from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route to render the file upload form
@app.route('/')
def index():
    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload a file</h1>
    <form method="POST" action="/upload" enctype="multipart/form-data">
      <input type="file" name="file" multiple>
      <input type="submit" value="Upload">
    </form>
    '''

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    files = request.files.getlist('file')
    
    if not files:
        return "No selected file"
    
    for file in files:
        if file.filename == '':
            return "No selected file"
        
        # Save file securely
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

    return "Files successfully uploaded!"

if __name__ == '__main__':
    app.run(debug=True)

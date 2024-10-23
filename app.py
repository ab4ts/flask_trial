import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

# Set up the app and the upload folder path
app = Flask(__name__)
UPLOAD_FOLDER = '/app/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allow specific file extensions (optional)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    
    # If no file is selected
    if file.filename == '':
        return 'No selected file', 400

    # Save the file if it's allowed
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f'File {filename} uploaded successfully!', 200
    
    return 'File type not allowed', 400

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload folder exists
    app.run(host='0.0.0.0', port=5000)

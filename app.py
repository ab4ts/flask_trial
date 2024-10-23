import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Use the Railway-mounted volume path for uploads
UPLOAD_FOLDER = '/mnt/volume/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists within the mounted volume
if not os.path.exists(UPLOAD_FOLDER):
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    except PermissionError as e:
        print(f"Permission error: {e}")
        UPLOAD_FOLDER = '/tmp/uploads'  # Fallback to a temporary directory if there's a permission issue
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        
        # Save the file to the volume or temporary directory
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

    return "Files successfully uploaded!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Get the PORT from Railway environment
    app.run(debug=True, host='0.0.0.0', port=port)

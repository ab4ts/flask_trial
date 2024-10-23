import os
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Dynamically set the upload folder based on the environment
if 'RAILWAY_ENVIRONMENT' in os.environ:
    UPLOAD_FOLDER = '/mnt/volume/uploads'  # Use the mounted volume in production
else:
    UPLOAD_FOLDER = 'uploads'  # Use a local folder in development

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    <h2><a href="/files">View Uploaded Files</a></h2>
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
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

    return "Files successfully uploaded!"

# Route to list uploaded files
@app.route('/files')
def list_files():
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        if not files:
            return "No files uploaded yet."
        file_list = '<br>'.join([f'<a href="/download/{file}">{file}</a>' for file in files])
        return f"<h1>Uploaded Files</h1><br>{file_list}"
    except FileNotFoundError:
        return "Uploads directory not found."

# Route to download a file
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)

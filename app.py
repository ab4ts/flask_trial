import os
from flask import Flask, request, send_from_directory, redirect, url_for, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set upload folder based on environment
if 'RAILWAY_ENVIRONMENT' in os.environ:
    UPLOAD_FOLDER = '/mnt/volume/uploads'
else:
    UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route to handle file upload and rendering
@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    file_list = ''.join([f'''
        <li>
            {file} - 
            <strong>Size:</strong> {os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], file)) / 1024:.2f} KB | 
            <strong>Type:</strong> {file.split('.')[-1]} - 
            <a href="/download/{file}">Download</a> | 
            <a href="/delete/{file}">Delete</a> | 
            <a href="/view/{file}">View</a>
        </li>''' for file in files])
    return f'''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload a file</h1>
    <form id="uploadForm" enctype="multipart/form-data" method="POST" action="/upload">
      <input type="file" name="file" multiple>
      <input type="submit" value="Upload">
    </form>
    <h2>Uploaded Files:</h2>
    <ul>{file_list}</ul>
    '''
@app.route('/view/<filename>')
def view_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_extension = filename.split('.')[-1].lower()

    # Handle text files
    if file_extension in ['txt', 'html']:
        with open(file_path, 'r') as f:
            file_content = f.read()
        return render_template_string(f'<h1>Viewing: {filename}</h1><pre>{file_content}</pre><br><a href="/">Back</a>')

    # Handle images
    elif file_extension in ['jpg', 'jpeg', 'png', 'gif']:
        return f'<h1>Viewing: {filename}</h1><img src="/download/{filename}" style="max-width:800px"><br><a href="/">Back</a>'

    # Handle video files
    elif file_extension in ['mp4', 'webm', 'ogg']:
        return f'''
        <h1>Viewing: {filename}</h1>
        <video width="640" controls>
          <source src="/download/{filename}" type="video/{file_extension}">
          Your browser does not support the video tag.
        </video>
        <br><a href="/">Back</a>
        '''

    # Other file types
    else:
        return f'<h1>Viewing not supported for {filename}</h1><br><a href="/">Back</a>'

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    files = request.files.getlist('file')
    for file in files:
        if file.filename == '':
            continue
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

    return redirect(url_for('index'))

# Route to download a file
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route to delete a file
@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('index'))

# Route to view a file
@app.route('/view/<filename>')
def view_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_extension = filename.split('.')[-1].lower()

    # Handle text files
    if file_extension in ['txt', 'html']:
        with open(file_path, 'r') as f:
            file_content = f.read()
        return render_template_string(f'<h1>Viewing: {filename}</h1><pre>{file_content}</pre><br><a href="/">Back</a>')

    # Handle images
    elif file_extension in ['jpg', 'jpeg', 'png', 'gif']:
        return f'<h1>Viewing: {filename}</h1><img src="/download/{filename}" style="max-width:800px"><br><a href="/">Back</a>'

    # Other file types
    else:
        return f'<h1>Viewing not supported for {filename}</h1><br><a href="/">Back</a>'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

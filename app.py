from flask import Flask, request, send_from_directory, jsonify
import os
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

# Route to render the main page
@app.route('/')
def index():
    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload a file</h1>
    <form id="uploadForm" enctype="multipart/form-data">
      <input type="file" name="file" multiple>
      <input type="submit" value="Upload">
    </form>
    <h2>Uploaded Files:</h2>
    <div id="fileList">
      <!-- Files will be listed here -->
    </div>
    <script>
      document.getElementById('uploadForm').addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const response = await fetch('/upload', {
          method: 'POST',
          body: formData
        });
        const files = await response.json();
        const fileList = document.getElementById('fileList');
        fileList.innerHTML = files.map(file => `<a href="/download/${file}">${file}</a><br>`).join('');
      });

      async function fetchFiles() {
        const response = await fetch('/files');
        const files = await response.json();
        const fileList = document.getElementById('fileList');
        fileList.innerHTML = files.map(file => `<a href="/download/${file}">${file}</a><br>`).join('');
      }

      // Fetch files on page load
      fetchFiles();
    </script>
    '''

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify([])

    files = request.files.getlist('file')

    uploaded_files = []
    for file in files:
        if file.filename == '':
            return jsonify([])

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        uploaded_files.append(filename)

    # Return the list of all files after the upload
    return jsonify(os.listdir(app.config['UPLOAD_FOLDER']))

# Route to list uploaded files
@app.route('/files')
def list_files():
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return jsonify(files)
    except FileNotFoundError:
        return jsonify([])

# Route to download a file
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

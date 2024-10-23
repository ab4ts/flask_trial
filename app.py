from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import logging

app = Flask(__name__)

# Set the upload folder to the mounted volume path
UPLOAD_FOLDER = '/app/uploads'

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Ensure the 'uploads' directory exists in the persistent storage path
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure Flask to use the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route to render the home page with an image upload form
@app.route('/')
def home():
    return render_template('upload.html')

# Route to handle image upload
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Ensure a file is uploaded
        if 'file' not in request.files:
            logging.error("No file part in the request")
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            logging.error("No selected file")
            return jsonify({'error': 'No selected file'}), 400

        # Save the uploaded file in the 'uploads' folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        logging.info(f"Saving file to {file_path}")
        file.save(file_path)

        # Return a response with a full file URL
        base_url = request.host_url
        return jsonify({'message': 'File uploaded successfully', 'file_path': f"{base_url}uploads/{file.filename}"}), 200
    except Exception as e:
        logging.error(f"Error during file upload: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    try:
        logging.info(f"Attempting to serve file: {filename}")
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        logging.error(f"Error while serving file {filename}: {str(e)}")
        return jsonify({'error': 'File could not be served'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

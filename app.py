from flask import Flask, request, render_template, jsonify, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# Ensure the 'uploads' directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the uploaded file in the 'uploads' folder
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Return a response with a file URL
        return jsonify({'message': 'File uploaded successfully', 'file_path': f"/uploads/{file.filename}"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

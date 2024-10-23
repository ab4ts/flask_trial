from flask import Flask, request, render_template, jsonify, send_from_directory
import os

app = Flask(__name__)

# Ensure the 'uploads' directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

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

        # Save the uploaded file
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Return a URL to access the uploaded file
        return jsonify({'message': 'File uploaded successfully', 'file_url': f"/uploads/{file.filename}"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

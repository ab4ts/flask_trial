from flask import Flask, request, jsonify
import cv2
import numpy as np
import yolov11  # Assuming you have a YOLOv11 library or implementation installed
import os

app = Flask(__name__)

# Load YOLOv11 model
model = yolov11.load_model("path/to/yolov11_weights.pth")

@app.route('/test-railway', methods=['POST'])
def test_railway():
    try:
        # Ensure a file is uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Read image from the uploaded file
        npimg = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Run YOLOv11 inference on the image
        results = model.detect(image)

        # Process detection results
        detected_objects = []
        for result in results:
            x, y, w, h, confidence, class_id = result
            detected_objects.append({
                'class_id': class_id,
                'confidence': confidence,
                'bounding_box': [x, y, w, h]
            })

        return jsonify({'detections': detected_objects}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

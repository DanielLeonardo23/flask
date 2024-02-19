from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload():
    try:
        print(request)
        image_data = request.data

    
        if not image_data:
            return jsonify({'error': 'No se han recibido datos'}), 400

        
        with open(os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg'), 'wb') as f:
            f.write(image_data)
        
        return jsonify({'message': 'Imagen subida correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/upload', methods=['GET'])
def get_upload():
    try:
        with open(os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg'), 'rb') as f:
            image_data = f.read()
        
        return image_data
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import os
import cloudinary
import cloudinary.uploader
from flask_cors import CORS  # Importa CORS

app = Flask(__name__)
# Definir la ruta raíz
@app.route('/')
def home():
    return "¡Bienvenido a la aplicación!"

CORS(app, resources={r"/*": {"origins": "*"}})  

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuración de Cloudinary
cloudinary.config(
    cloud_name='duruqbipv',  
    api_key='857167242619486',  
    api_secret='POaaiNhqAICv8t91AXXD-ABx-D4'  
)

@app.route('/upload', methods=['POST'])
def upload():
    try:
   
        image_data = request.data

        if not image_data:
            return jsonify({'error': 'No se han recibido datos'}), 400

     
        local_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')
        with open(local_image_path, 'wb') as f:
            f.write(image_data)

        result = cloudinary.uploader.upload(local_image_path, resource_type='auto')

    
        return jsonify({
            'message': 'Imagen subida correctamente',
            'url': result['secure_url'],
            'filename': result['public_id']
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/upload', methods=['GET'])
def get_upload():
    try:
  
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')
        
        if not os.path.exists(image_path):
            return jsonify({'error': 'Imagen no encontrada'}), 404

       
        with open(image_path, 'rb') as f:
            image_data = f.read()

      
        return image_data, 200, {'Content-Type': 'image/jpeg'}

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
   
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)

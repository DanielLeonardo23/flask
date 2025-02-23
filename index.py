from flask import Flask, request, jsonify
import os
import cloudinary
import cloudinary.uploader
from flask_cors import CORS  # Importa CORS

app = Flask(__name__)

# Configuración de CORS para permitir solicitudes de cualquier origen
CORS(app, resources={r"/*": {"origins": "*"}})  # Permite solicitudes de cualquier origen

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuración de Cloudinary
cloudinary.config(
    cloud_name='duruqbipv',  # Tu nombre de Cloudinary
    api_key='857167242619486',  # Tu API Key
    api_secret='POaaiNhqAICv8t91AXXD-ABx-D4'  # Tu API Secret
)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Obtener los datos binarios de la solicitud
        image_data = request.data

        if not image_data:
            return jsonify({'error': 'No se han recibido datos'}), 400

        # Guardar la imagen localmente en el servidor
        local_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')
        with open(local_image_path, 'wb') as f:
            f.write(image_data)

        # Subir la imagen a Cloudinary
        result = cloudinary.uploader.upload(local_image_path, resource_type='auto')

        # Respondemos con la URL de la imagen subida a Cloudinary
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
        # Ruta del archivo guardado
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')
        
        if not os.path.exists(image_path):
            return jsonify({'error': 'Imagen no encontrada'}), 404

        # Leemos la imagen almacenada
        with open(image_path, 'rb') as f:
            image_data = f.read()

        # Devolvemos la imagen como datos binarios
        return image_data, 200, {'Content-Type': 'image/jpeg'}

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Asegurarse de que la aplicación escuche en todas las direcciones
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)

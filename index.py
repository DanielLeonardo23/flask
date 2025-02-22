from flask import Flask, request, jsonify, render_template
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
import stripe

# Definir las credenciales directamente en el código
CLOUD_NAME = 'duruqbipv'
API_KEY = '857167242619486'
API_SECRET = 'POaaiNhqAICv8t91AXXD-ABx-D4'
STRIPE_SECRET_KEY = 'sk_test_51Qol4rAkA9dBfeWxx5RjKhKauUxCpbR0gB5RwA21Cu0b316epbVrq9PUcvL0J5JqHfaAbKG0m3U1B5mVw5ngTatw00MAeQuK40'

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)

# Configuración de Stripe
stripe.api_key = STRIPE_SECRET_KEY

app = Flask(__name__)

# Lista para almacenar los links de las imágenes subidas
uploaded_images = []

# Ruta principal que muestra el formulario para cargar imágenes
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar la carga de imágenes
@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Obtén la imagen de los datos recibidos a través de 'form-data'
        if 'image' not in request.files:
            return jsonify({'error': 'No se ha recibido una imagen'}), 400
        
        image_file = request.files['image']

        # Si no se ha recibido un archivo
        if image_file.filename == '':
            return jsonify({'error': 'No se ha seleccionado un archivo'}), 400

        # Sube la imagen a Cloudinary
        response = cloudinary.uploader.upload(image_file, 
                                              resource_type="auto",  # Detecta automáticamente el tipo de archivo
                                              folder="uploads")  # Carpeta en Cloudinary para almacenar las imágenes

        # Obtén la URL de la imagen subida
        image_url = response.get('secure_url')

        # Almacenar el link de la imagen
        uploaded_images.append(image_url)

        return jsonify({'message': 'Imagen subida correctamente', 'image_url': image_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta para ver las imágenes subidas
@app.route('/upload', methods=['GET'])
def get_upload():
    try:
        # Si hay imágenes subidas, devolverlas en formato JSON
        if uploaded_images:
            return jsonify({'image_urls': uploaded_images}), 200
        else:
            return jsonify({'message': 'No hay imágenes subidas.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)

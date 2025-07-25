import os
from flask import Flask, request, render_template, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from color_extractor import ColorExtractor
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files')
    n_colors = int(request.form.get('n_colors', 5))
    
    if not files or all(file.filename == '' for file in files):
        return jsonify({'error': 'No files selected'}), 400
    
    valid_files = []
    temp_paths = []
    
    try:
        for file in files:
            if file and allowed_file(file.filename):
                # Create temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                file.save(temp_file.name)
                temp_paths.append(temp_file.name)
                valid_files.append(file.filename)
        
        if not temp_paths:
            return jsonify({'error': 'No valid image files uploaded'}), 400
        
        # Extract colors
        extractor = ColorExtractor(n_colors=n_colors)
        palette = extractor.get_color_palette(temp_paths)
        
        return jsonify({
            'success': True,
            'palette': palette,
            'files_processed': valid_files,
            'n_colors': n_colors
        })
    
    except Exception as e:
        return jsonify({'error': f'Error processing images: {str(e)}'}), 500
    
    finally:
        # Clean up temporary files
        for temp_path in temp_paths:
            try:
                os.unlink(temp_path)
            except:
                pass

@app.route('/extract', methods=['POST'])
def extract_colors():
    try:
        data = request.get_json()
        if not data or 'image_urls' not in data:
            return jsonify({'error': 'No image URLs provided'}), 400
        
        image_urls = data['image_urls']
        n_colors = data.get('n_colors', 5)
        
        # For now, this endpoint expects local file paths
        # In future iterations, this could handle remote URLs
        extractor = ColorExtractor(n_colors=n_colors)
        palette = extractor.get_color_palette(image_urls)
        
        return jsonify({
            'success': True,
            'palette': palette,
            'n_colors': n_colors
        })
    
    except Exception as e:
        return jsonify({'error': f'Error extracting colors: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
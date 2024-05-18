from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import matlab.engine
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Call MATLAB function
        texto_filtrado = call_matlab_function(filepath)
        return render_template('result.html', texto_filtrado=texto_filtrado)
    return render_template('upload.html')

@app.route('/formulario/<path:filename>')
def serve_formulario_file(filename):
    return send_from_directory('formulario', filename)

def call_matlab_function(image_path):
    eng = matlab.engine.start_matlab()
    eng.addpath('ProgramaTexto2.m', nargout=0)
    texto_filtrado = eng.ProgramaTexto2(image_path, nargout=1)
    eng.quit()
    return texto_filtrado

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)

from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
import os
from werkzeug.utils import secure_filename
from assistant import Assistant
from config import PATH_TO_BOOK, MODEL
import shutil
import atexit

app = Flask(__name__)

# Set a secret key for sessions
app.secret_key = 'asdfghjkl'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

assistant = Assistant(PATH_TO_BOOK, MODEL)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_updated_path():
    path = []
    for filename in os.listdir(UPLOAD_FOLDER):
        path.append(os.path.join(UPLOAD_FOLDER, filename))
    return path

def get_response(msg):
    response = assistant.process_question(msg)
    return response

def clear_uploads_directory():
    folder = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

atexit.register(clear_uploads_directory)

@app.post("/chat")
def chat():
    text = request.get_json().get("message")
    response_chat = get_response(text)
    message = {"answer": response_chat}
    return jsonify(message)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['pdf']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        path = get_updated_path()
        global assistant
        assistant = Assistant(path, MODEL)
        # session['assistant_initialized'] = True  # Set flag to True after upload
        flash('File successfully uploaded')
        return redirect(url_for('index'))
    else:
        flash('Allowed file types are .pdf')
        return redirect(request.url)

@app.route('/', methods=['GET', 'POST'])
def index():

    # if 'assistant_initialized' not in session:
    #     session['assistant_initialized'] = False

    # if  session['assistant_initialized'] == True:
    #     assistant = Assistant(PATH_TO_BOOK, MODEL)
    #     session['assistant_initialized'] = False

    if request.method == 'POST':
        user_question = request.form['question']
        response = assistant.process_question(user_question)
        session['response'] = response
        session['visited'] = False
        return redirect(url_for('index'))
    else:
        if session.get('visited'):
            session.clear()
        session['visited'] = True
    return render_template('index.html', response=session.get('response', ""))

if __name__ == '__main__':
    app.run()
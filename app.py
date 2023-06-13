from flask import Flask, request, render_template, send_from_directory
import logging
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Set the path where the uploaded files will be saved
DATA_DIR = os.environ.get('DATA_DIR', "~/data/training/images")
#app.config['UPLOAD_FOLDER'] = os.path.expanduser(DATA_DIR)


def get_file_list(unique_token, folder_name):
    folder_path = os.path.join(DATA_DIR, unique_token, 'image', folder_name)
    files = os.listdir(folder_path)
    return files


@app.route('/', methods=['GET', 'POST'])
def upload_files():
    folder_name = None
    magic_number = None
    unique_token = None
    regular_token = None
    files_saved = []

    if request.method == 'POST':
        magic_number = request.form['magic_number']
        unique_token = request.form['unique_token']
        regular_token = request.form.get('regular_token')  # This field is optional


        # Create the folder name
        if regular_token:
            folder_name = f"{magic_number}_{unique_token} {regular_token}"
        else:
            folder_name = f"{magic_number}_{unique_token}"

        # Create the folder if it doesn't exist
        folder_path = os.path.join(DATA_DIR, unique_token, 'image', folder_name)
        os.makedirs(folder_path, exist_ok=True)

        files = request.files.getlist('file')
        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder_path, filename))

        files_saved = get_file_list(unique_token, folder_name)


    return render_template('home.html', folder_name=folder_name, unique_token=unique_token, files_saved=files_saved)


@app.route('/files/<unique_token>/<folder>/<filename>')
def get_file(unique_token, folder, filename):
    folder_path = os.path.join(DATA_DIR, unique_token, 'image', folder)
    return send_from_directory(folder_path, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
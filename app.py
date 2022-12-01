from debugpy import connect
from flask import Flask
from flask import redirect, render_template, url_for, request
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import vision_func


UPLOAD_FOLDER = './static/image'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    load_dotenv()
    connect_str = '*****'

    container_name = 'artists'
    # .envがロードされる前に読み込まれる？
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    if request.method == 'POST':
        fs = request.files['file']
        filename = 'test.png'
        filepath = './static/image/' + filename
        fs.save(filepath)

        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob='test.png'
        )
        upload_blob = blob_client.upload_blob(filepath, overwrite=True)

        properties = blob_service_client.get_blob_client(
            container=container_name, blob='test.png')

        # URLがプロパティにいない…？
        print(properties.get_blob_properties())

        # # テキスト抽出関数にURLを渡す
        word = vision_func.get_word()
        print(word)
        return render_template('result.html', word=word)

    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True

import string, random, os, redis
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from azure.storage.blob import BlockBlobService

load_dotenv()
account = os.environ.get('ACCOUNT', None)
key = os.environ.get('STORAGE_KEY', None)
container = os.environ.get('CONTAINER', None)

redis_host = os.environ.get('REDIS_HOST', None)
redis_port = os.environ.get('REDIS_PORT', None)
redis_password = os.environ.get('REDIS_PASSWORD', None)

redis_client = None
if redis_password:
    redis_client = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
    )
else:
    redis_client = redis.Redis(
        host=redis_host,
        port=redis_port,
    )

app = Flask(__name__)
app.config['CORS_ALLOW_HEADERS'] = 'Content-Type'
app.config['CORS_EXPOSE_HEADERS'] = 'Content-Type'
app.config['CORS_SUPPORTS_CREDENTIALS'] = True

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

CORS(app, resources={r"*": {"origins": "*"}})

blob_service = BlockBlobService(account_name=account, account_key=key)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/api/upload', methods=['POST'])
def hello():
    # check if the post request has the file part
    if 'photo' not in request.files:
        return jsonify({"error": "No photo given"})

    file = request.files['photo']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({"error": "No filename given"})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        fileextension = filename.rsplit('.',1)[1]
        Randomfilename = id_generator()
        filename = Randomfilename + '.' + fileextension
        try:
            blob_service.create_blob_from_stream(container, filename, file)
        except Exception:
            return jsonify({"error": "Error during upload"})
        ref = 'https://'+ account + '.blob.core.windows.net/' + container + '/' + filename
        redis_client.set(ref, 'Loading')
        redis_client.publish('insert', ref)
        return jsonify({ "url": ref, "filename": filename })
    return jsonify({"error": "Not uploaded"})


@app.route('/api/conversion', methods=['GET'])
def conversion():
    filename = request.args.get('filename')
    if not filename:
        return {"error": "Requires filename"}
    ref = 'https://'+ account + '.blob.core.windows.net/' + container + '/' + filename
    stored_value = redis_client.get(ref)
    if not stored_value:
        return {"error": "No message saved"}
    url = stored_value.decode("utf-8")
    if url == 'Loading':
        return {"error": "Still loading"}
    filename = url.split('/')[-1]
    return { "url": url, "filename": filename }

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=4000)

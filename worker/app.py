import string, random, os, redis, time, requests
from dotenv import load_dotenv
from io import BytesIO
import numpy as np
from PIL import Image
from albumentations.augmentations.transforms import ElasticTransform
from azure.storage.blob import BlockBlobService

load_dotenv()

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

account = os.environ.get('ACCOUNT', None)
key = os.environ.get('STORAGE_KEY', None)
container = os.environ.get('CONTAINER', None)

IMAGE_WIDTH = 200
IMAGE_HEIGHT = 200

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def convert_file(url):
    image = Image.open(BytesIO(requests.get(url).content)).resize((IMAGE_WIDTH, IMAGE_HEIGHT))
    image_array = np.array(image)

    augmentation = ElasticTransform()
    data = {"image": image_array}
    augmented = augmentation(**data)
    image = augmented["image"]

    blob_service = BlockBlobService(account_name=account, account_key=key)

    img = Image.fromarray(image)

    imagefile = BytesIO()
    img.save(imagefile, format='PNG')
    imagefile.seek(0)

    Randomfilename = id_generator()
    filename = Randomfilename + '.png'

    blob_service.create_blob_from_stream(container, filename, imagefile)

    ref =  'https://'+ account + '.blob.core.windows.net/' + container + '/' + filename
    redis_client.set(url, ref)

def main():
    p = redis_client.pubsub()
    p.subscribe('insert')
    while True:
        message = p.get_message()
        if not message:
            time.sleep(5)
        else:
            url = None
            try:
                url = message['data'].decode("utf-8")
            except Exception as e:
                continue
            convert_file(url)
            time.sleep(5)
main()

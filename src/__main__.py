import hashlib
import os
import multiprocessing
from banhammer import Generator
from base64 import urlsafe_b64encode
from urllib.parse import unquote
from cleanup import Cleanup
from sanic import Sanic
from sanic.exceptions import abort
from sanic.response import file, text

app = Sanic(name='banhammer')
cleanup = Cleanup()
main = Generator()

def hash(string: str):
    m = hashlib.sha256()
    m.update(string.encode('utf-8'))
    digest = m.digest()
    return urlsafe_b64encode(digest).decode('utf-8')

@app.route('/<input_str>')
async def banhammer(request, input_str):
    cleaned = unquote(input_str)
    hash_check = hash(cleaned.upper())
    file_name = f'./output/{hash_check}.gif'

    if (os.path.isfile(file_name) == False):
        buf = main.image_gen(cleaned)

        if not os.path.exists('./output'):
            os.makedirs('./output')

        with open(file_name, 'wb') as f:
            f.write(buf.getbuffer())

    resp = await file(file_name)
    cleanup.clean()

    return resp


if __name__ == '__main__':
    cores = multiprocessing.cpu_count()
    app.run(host='0.0.0.0', port=8080, workers=cores)

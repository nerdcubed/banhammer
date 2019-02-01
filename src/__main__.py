import os
import multiprocessing
from urllib.parse import unquote
from generator import Generator
from sanic import Sanic
from sanic.exceptions import abort
from sanic.response import file, text

app = Sanic()
main = Generator()

@app.route('/')
async def index(request):
    return await file('index.txt')

@app.route('/favicon.ico')
async def favicon(request):
    return text('Not Found', status=404)

@app.route('/api/v1.0/banhammer/<input_str>')
async def banhammer(request, input_str):
    cleaned = unquote(input_str)
    hash_check = main.hash(cleaned.upper())
    file_name = f'./output/{hash_check}.gif'
    
    if (os.path.isfile(file_name) == False):
    file_name = main.image_gen(cleaned)

    resp = await file(file_name)
    return resp

if __name__ == '__main__':
    cores = multiprocessing.cpu_count()
    app.run(host='0.0.0.0', port=8080, workers=cores)

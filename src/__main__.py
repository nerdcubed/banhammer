from PIL import Image, ImageFont, ImageDraw
import io
import os
import numpy
import imageio
import json
import requests
import uuid
import redis
import time

class Generator:
    """HAMMER DOWN!"""

    def __init__(self):
        self.url = os.environ['BAN_URL']
        self.headers = json.loads(os.environ['HEADERS'])
        self.redis = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=6379, db=0)
        self.size_check = 10
        self.target_size = (1200, 225)
        self.frames = sorted(os.listdir('./frames/'))
        self.form_name = os.environ['FORM_NAME']
        with open('frames.json') as f:
            j = json.load(f)
            self.metadata = {}
            for key, coords in j.items():
                cset = []
                for c in coords:
                    cset.append(tuple(c))
                self.metadata[key] = cset
    
    # From https://stackoverflow.com/a/53092540
    def find_coeffs(self, source_coords, target_coords):
        matrix = []
        for s, t in zip(source_coords, target_coords):
            matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
            matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])
        A = numpy.matrix(matrix, dtype=numpy.float)
        B = numpy.array(source_coords).reshape(8)
        res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
        return numpy.array(res).reshape(8)

    def multiply_coords(self, coords):
        """Used for antialiasing text."""
        new = []
        for t in coords:
            new.append(tuple(i * 2 for i in t))
        return new

    def draw_outline(self, draw_obj, text, x, y, font):
        """Adds an outline to the text."""
        draw_obj.text((x-3, y-3), text,(159,115,110,255),font=font)
        draw_obj.text((x+3, y-3), text,(159,115,110,255),font=font)
        draw_obj.text((x+3, y+3), text,(159,115,110,255),font=font)
        draw_obj.text((x-3, y+3), text,(159,115,110,255),font=font)
        draw_obj.text((x, y), text, (255,153,126,255), font=font)
        return
    
    def image_gen(self, text: str):
        """Generates the GIF."""
        text = text.upper()
        size_check = self.size_check
        while True:
            test_font = ImageFont.truetype(font='./assets/Teko-Bold.ttf', size=size_check)
            font_size = test_font.getsize(text)
            if font_size[0] > self.target_size[0] or font_size[1] > self.target_size[1]:
                break
            else:
                font = test_font
                size_check += self.size_check
        
        text_img = Image.new('RGBA', self.target_size, (0,0,0,0))

        d = ImageDraw.Draw(text_img)
        self.draw_outline(d, text, 3, 3, font)

        black = Image.new('RGBA', text_img.size)
        cropped = Image.composite(text_img, black, text_img)
        final_text = text_img.crop(text_img.getbbox()) 

        frame = 0
        output = str(uuid.uuid4().hex)
        with imageio.get_writer(f'./output/{output}.gif', mode='I', duration=0.04) as writer:
            for filename in self.frames:
                path = f'./frames/{filename}'
                coords = self.metadata.get(str(frame + 1), {})
                if coords:
                    f = Image.open(path).convert('RGBA')
                    coeffs = self.find_coeffs([(0,0), (final_text.size[0],0), (final_text.size[0],final_text.size[1]), (0, final_text.size[1])], self.multiply_coords(coords))
                    new_im = final_text
                    new_im = new_im.transform(tuple(i * 2 for i in f.size), Image.PERSPECTIVE, coeffs, Image.BILINEAR)
                    new_im = new_im.resize(f.size, Image.ANTIALIAS)
                    f.paste(new_im, mask=new_im)
                    imgbytes = io.BytesIO()
                    f.save(imgbytes, format='GIF')
                    imgbytes.seek(0)
                    image = imageio.imread(imgbytes, format='gif')
                    writer.append_data(image)
                else:
                    image = imageio.imread(path)
                    writer.append_data(image)
                frame += 1
        
        files = {'files[]': open(f'./output/{output}.gif', 'rb')}
        r = requests.post(self.url, files=files, headers=self.headers)
        os.remove(f'./output/{output}.gif')
        return r.json()
    
    def pubsub(self):
        """Responds to any Pub/Sub events."""
        p = self.redis.pubsub(ignore_subscribe_messages=True)
        p.subscribe('mod.bans')
        while True:
            message = p.get_message()
            if message:
                if message['type'] == 'message':
                    c = message['channel'].decode('utf-8')
                    if c == 'mod.bans':
                        d = json.loads(message['data'].decode('utf-8'))
                        id = d['id']
                        name = d['name']
                        resp = self.image_gen(name)
                        self.redis.publish(f'mod.bans.{id}', resp)
            time.sleep(0.01)

if __name__ == "__main__":
    main = Generator()
    main.pubsub()

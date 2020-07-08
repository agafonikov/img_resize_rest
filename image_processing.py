from PIL import Image

import uuid
import os

from config import Config


class ImgManager:
    @staticmethod
    def init(image: str):
        allowed_formats = ('jpg', 'png', 'jpeg')

        img_format = image.split('.')[-1]
        if img_format.lower() not in allowed_formats:
            raise ValueError('Wrong file format: %s', img_format)

        process_id = uuid.uuid4().int
        new_img_name = uuid.uuid4().hex + '.' + img_format
        img_name = image
        return {'process_id': process_id, 'img_name': img_name, 'new_img_name': new_img_name}

    @staticmethod
    def resize(width, height, img_name, new_img_name):
        img = Image.open(os.path.join(Config.UPLOAD_DIR, img_name))

        out_img_name = os.path.join(Config.THUMB_DIR, str(new_img_name))
        new_img = img.resize((width, height), Image.ANTIALIAS)
        new_img.save(out_img_name)

        return out_img_name

    @staticmethod
    def delete(image_name):
        img = os.path.join(Config.THUMB_DIR, image_name)
        if os.path.isfile(img):
            os.remove(img)
        else:
            raise FileNotFoundError("Image %{self.new_img_name} does not exist")
        return True

from tasks import resize
from db import DB

import uuid
import json


class ImgManager:
    def __init__(self, task_db: DB, image: str):
        self.allowed_formats = ('jpg', 'png', 'jpeg')

        img_format = image.split('.')[-1]
        if img_format.lower() not in self.allowed_formats:
            raise ValueError('Wrong file format: %s', img_format)
        self.process_id = uuid.uuid4().int
        self.new_img_name = uuid.uuid4().hex + '.' + img_format
        self.db = task_db
        self.img_name = image

    def resize(self, width, height):
        """
        Add new task to database and task queue
        """
        self.db.set_task(str(self.process_id), json.dumps({'status': 'pending', 'image_name': self.new_img_name}))
        return resize(self, width, height)

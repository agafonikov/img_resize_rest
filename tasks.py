from celery import Celery
from PIL import Image

import os
import redis
import json

# TODO: import from config
UPLOAD_DIR = os.path.join(os.path.curdir, 'static', 'images', 'uploaded')
THUMB_DIR = os.path.join(os.path.curdir, 'static', 'images', 'thumbnails')

# TODO: import broker and backend from config
celery_app = Celery('tasks', broker='redis://127.0.0.1:6379', backend='redis://127.0.0.1:6379')
db = redis.Redis()


@celery_app.task
def resize(manager, width, height):
    img = Image.open(os.path.join(UPLOAD_DIR, manager.img_name))

    out_img_name = os.path.join(THUMB_DIR, str(manager.new_img_name))
    new_img = img.resize((width, height), Image.ANTIALIAS)
    new_img.save(out_img_name)

    task = json.loads(manager.db.get_task(manager.process_id))
    task.update({'status': 'done'})
    manager.db.set_task(manager.process_id, json.dumps(task))
    return out_img_name

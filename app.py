from flask import Flask, request

from db import RedisDB
from image_processing import ImgManager

import json
import logging
import os
import config
from app_views import register_resize_api

# TODO: Create custom config
# TODO: Implement logger

DEFAULT_IMG_NAME = 'tiger.jpg'

app = Flask(__name__)
logger = logging.Logger('flask-app')
logger.setLevel('DEBUG')

app.config.from_object(config.DebugConfig)

task_db = RedisDB()


register_resize_api(app, '/resize', task_db)


# TODO: delete later
@app.route('/download/<task_id>', methods=['GET'])
def load_img(task_id):
    task = json.loads(str(task_db.get_task(str(task_id))))
    if task['status'] == 'done':
        return app.send_static_file(os.path.join('images', 'thumbnails', task['image_name'])), 200, {'content-type': 'image/jpeg'}


if __name__ == '__main__':
    app.run()

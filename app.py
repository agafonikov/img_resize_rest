from flask import Flask, request
from env_setup import app, task_db

from db import RedisDB

import logging
import config
from app_views import register_resize_api

DEFAULT_IMG_NAME = 'tiger.jpg'

logger = logging.Logger('flask-app')

app.config.from_object(config.DebugConfig)


register_resize_api(app, '/resize', task_db)


if __name__ == '__main__':
    app.run()

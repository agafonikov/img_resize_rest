from flask import Config

import os


class DebugConfig(Config):
    UPLOAD_DIR = os.path.join(os.path.curdir, 'static', 'images', 'uploaded')
    THUMB_DIR = os.path.join(os.path.curdir, 'static', 'images', 'thumbnails')
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
    DEFAULT_IMG_NAME = 'tiger.jpg'
    ADDR = '127.0.0.1:5000'
    DEBUG = True


Config = DebugConfig

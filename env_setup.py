from celery import Celery
from db import RedisDB
from flask import Flask

from config import Config

app = Flask(__name__)
celery_app = Celery('tasks', broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)
task_db = RedisDB()

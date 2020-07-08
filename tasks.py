from image_processing import ImgManager
from env_setup import celery_app, task_db

import json


@celery_app.task
def resize(width, height, img_name, new_img_name):
    ImgManager.resize(width, height, img_name, new_img_name)


@celery_app.task
def delete(img_name):
    ImgManager.delete(img_name)


@celery_app.task
def set_pending(task_id, **kwargs):
    db_value = kwargs
    db_value.update({'status': 'pending'})
    task_db.set_task(task_id, json.dumps(db_value))


@celery_app.task
def set_done(task_id, **kwargs):
    db_value = kwargs
    db_value.update({'status': 'done'})
    task_db.set_task(task_id, json.dumps(db_value))


@celery_app.task
def log():
    pass

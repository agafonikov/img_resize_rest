from flask import Flask, jsonify

import pytest
import json
import time
import os

from app_views import register_resize_api
from db import RedisDB
import config


def test_task_setting():
    app = Flask(__name__)
    app.config.from_object(config.DebugConfig)
    db = RedisDB()
    url = '/resize'
    register_resize_api(app, url, db)
    client = app.test_client()

    # must be OK
    response = client.post(url, data=json.dumps({'w': 100, 'h': 100}), content_type='application/json')
    assert response.status_code == 201

    # parameters not set
    response = client.post(url, data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

    # width > 9999
    response = client.post(url, data=json.dumps({'w': 10000, 'h': 100}), content_type='application/json')
    assert response.status_code == 400

    # height > 9999
    response = client.post(url, data=json.dumps({'w': 100, 'h': 10000}), content_type='application/json')
    assert response.status_code == 400

    # width < 1
    response = client.post(url, data=json.dumps({'w': 0, 'h': 100}), content_type='application/json')
    assert response.status_code == 400

    # height < 1
    response = client.post(url, data=json.dumps({'w': 100, 'h': 0}), content_type='application/json')
    assert response.status_code == 400

    # TODO: delete task from db


def test_status_check():
    app = Flask(__name__)
    app.config.from_object(config.DebugConfig)
    db = RedisDB()
    url = '/resize'
    register_resize_api(app, url, db)
    client = app.test_client()

    response = client.post(url, data=json.dumps({'w': 100, 'h': 100}), content_type='application/json')
    data = json.loads(response.data)
    status_url = os.path.join(url, data["status_link"].split('/')[-1])
    task_status_response = client.get(status_url)
    task_status_data = json.loads(task_status_response.data.decode('utf-8'))

    assert task_status_response.status_code == 200

    if task_status_data['status'] == 'done':
        assert task_status_data.get('image_name') is not None
    else:
        assert task_status_data['status'] == 'pending'
        time.sleep(3)
        assert task_status_data['status'] == 'done'
        assert task_status_data.get('image_name') is not None

    # TODO: delete task from db

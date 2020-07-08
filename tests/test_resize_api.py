from flask import Flask

import pytest
import json
import time
import os

from app_views import register_resize_api
from db import RedisDB
import config


@pytest.fixture(scope='function')
def test_app():
    app = Flask(__name__)
    app.config.from_object(config.DebugConfig)
    db = RedisDB()
    url = '/resize'
    register_resize_api(app, url, db)

    return {
        'app': app,
        'db': db,
        'url': url
    }


def test_task_setting(test_app):
    client = test_app['app'].test_client()

    # must return CREATED
    response = client.post(test_app['url'], data=json.dumps({'w': 100, 'h': 100}), content_type='application/json')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 201
    assert data.get('task_id') is not None

    # parameters not set
    response = client.post(test_app['url'], data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

    # width > 9999
    response = client.post(test_app['url'], data=json.dumps({'w': 10000, 'h': 100}), content_type='application/json')
    assert response.status_code == 400

    # height > 9999
    response = client.post(test_app['url'], data=json.dumps({'w': 100, 'h': 10000}), content_type='application/json')
    assert response.status_code == 400

    # width < 1
    response = client.post(test_app['url'], data=json.dumps({'w': 0, 'h': 100}), content_type='application/json')
    assert response.status_code == 400

    # height < 1
    response = client.post(test_app['url'], data=json.dumps({'w': 100, 'h': 0}), content_type='application/json')
    assert response.status_code == 400


def test_status_check(test_app):
    client = test_app['app'].test_client()

    response = client.post(test_app['url'], data=json.dumps({'w': 100, 'h': 100}), content_type='application/json')
    data = json.loads(response.data)
    status_url = os.path.join(test_app['url'], str(data['task_id']))
    task_status_response = client.get(status_url)
    task_status_data = json.loads(task_status_response.data.decode('utf-8'))

    assert task_status_response.status_code == 200

    if task_status_data['status'] == 'done':
        assert task_status_data.get('image_name') is not None
    else:
        assert task_status_data['status'] == 'pending'

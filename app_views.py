import json
import os

import celery
from flask.views import MethodView, request

from image_processing import ImgManager
from tasks import resize, set_done, set_pending, delete

from config import Config


class ResizeTaskAPI(MethodView):
    def post(self):
        params = request.get_json()
        if params.get('w') is None or params.get('h') is None:
            return json.dumps({'error': 'width or/and height are not set'}), 400, {
                'content-type': 'application/json'
            }
        width, height = params['w'], params['h']
        if width < 1 or height < 1 or \
                width > 9999 or height > 9999:
            return json.dumps({'error': 'parameters must be in range 1-9999'}), 400, {
                'content-type': 'application/json'
            }

        img_params = ImgManager.init(Config.DEFAULT_IMG_NAME)

        celery.chain(
            set_pending.si(img_params['process_id'], image_name=img_params['new_img_name']),
            resize.si(width, height, img_params['img_name'], img_params['new_img_name']),
            set_done.si(img_params['process_id'], image_name=img_params['new_img_name'])
        )()

        return json.dumps({
            'task_id': img_params['process_id']
        }), 201, {'ContentType': 'application/json'}

    def get(self, task_db, task_id):
        task = json.loads(str(task_db.get_task(str(task_id))))
        if task['status']:
            return json.dumps(task), 200, {'content-type': 'application/json'}
        else:
            return json.dumps('task does not exist'), 404, {'content-type': 'application/json'}


# noinspection PyArgumentList
def register_resize_api(app, url, task_db):
    resize_img = ResizeTaskAPI.as_view('resize_task')
    app.add_url_rule(
        url, methods=['POST'],
        view_func=resize_img
    )
    app.add_url_rule(
        os.path.join(url, '<task_id>'),
        methods=['GET'],
        defaults={'task_db': task_db},
        view_func=resize_img,
    )

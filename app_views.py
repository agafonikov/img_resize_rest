from flask.views import MethodView, request

from image_processing import ImgManager

import os, json

DEFAULT_IMG_NAME = 'tiger.jpg'


class ResizeTaskAPI(MethodView):
    def post(self, task_db, app):
        params = request.get_json()
        if params.get('w') is None or params.get('h') is None:
            return json.dumps({'error': 'width or/and height are not set'}), 400, {
                'content-type': 'application/json'}
        width, height = params['w'], params['h']
        if width < 1 or height < 1 or \
                width > 9999 or height > 9999:
            return json.dumps({'error': 'parameters must be between 1 and 9999'}), 400, {
                'content-type': 'application/json'}

        manager = ImgManager(task_db, DEFAULT_IMG_NAME)
        manager.resize(width, height)

        return json.dumps({
            'status_link': os.path.join(app.config['ADDR'], str(manager.process_id))
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
    app.add_url_rule(url, methods=['POST'], defaults={'app': app, 'task_db': task_db}, view_func=resize_img)
    app.add_url_rule(
        os.path.join(url, '<task_id>'),
        methods=['GET'],
        defaults={'task_db': task_db},
        view_func=resize_img,
    )

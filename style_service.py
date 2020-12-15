import os
import time
from asyncio import new_event_loop
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from queue import Queue
from typing import Callable

from flask import Flask, request, jsonify, send_file, Response
from werkzeug.middleware.proxy_fix import ProxyFix

from stylize import stylize_video, stylize_image, videos_dir, image_dir, cache_dir


class StyleServer(Flask):

    def __init__(self) -> None:

        super(StyleServer, self).__init__(__name__)
        self.wsgi_app = ProxyFix(self.wsgi_app)
        self.add_url_rule(rule='/stylize/<style>', view_func=self.stylize, methods=['POST'])
        self.add_url_rule(rule='/check', view_func=self.check, methods=['GET'])
        self.add_url_rule(rule='/content', view_func=self.content, methods=['GET'])
        self.available = True
        self.queue = Queue()
        self.running = set()
        self.id_to_filename = {}
        self.i = 1
        for directory in [videos_dir, image_dir, cache_dir]:
            if not os.path.isdir(directory):
                os.makedirs(directory)

    @staticmethod
    def generate_filename():
        t = datetime.now() - datetime(1, 1, 1)
        return str(t.days * 24 * 3600 * 1000 + t.seconds * 1000 + t.microseconds)

    def stylize(self, style: str) -> Response:

        file = request.files['file']
        extention = file.filename.split('.')[-1]

        task_id = self.i
        self.i += 1
        self.running.add(task_id)
        filename = self.generate_filename() + '.' + extention
        self.id_to_filename[task_id] = filename

        if filename.endswith('.mp4'):
            file.save(f'{videos_dir}/{filename}')
            method = stylize_video
        else:
            file.save(f'{image_dir}/{filename}')
            method = stylize_image

        if style == 'mock':
            self.running.remove(task_id)
            return jsonify({'id': task_id})

        else:

            self.queue.put((task_id, style))

            pool = ThreadPoolExecutor(max_workers=1)
            loop = new_event_loop()
            loop.run_in_executor(pool, self.run_stylize, method)

            return jsonify({'id': task_id})

    def run_stylize(self, method: Callable[[str, str], None]) -> None:

        while not self.available:
            time.sleep(15)

        self.available = False

        task_id, style = self.queue.get()
        filename = self.id_to_filename[task_id]

        # TODO: specify exceptions
        try:
            method(filename, style)
        except:
            pass
        finally:
            self.running.remove(task_id)
            self.available = True

    def check(self) -> Response:

        taks_id = int(request.args.get('id'))
        status = taks_id not in self.running
        return jsonify({'finished': status})

    def content(self) -> Response:

        taks_id = request.args.get('id')
        filename = self.id_to_filename[int(taks_id)]
        return send_file(f'{videos_dir}/{filename}', attachment_filename=filename)


if __name__ == '__main__':

    server = StyleServer()
    server.run(host='0.0.0.0', port=9999, debug=True)

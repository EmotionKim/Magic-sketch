import os
import sys
import base64
import logging
import socket
import signal
import subprocess

from tornado import ioloop, options, web

import color_to_grey
import test
LABEL_FOLDER = os.path.join(os.path.dirname(__file__), "dataset/label")
STATIC_IMG_FOLDER = os.path.join(os.path.dirname(__file__), "img")


def parse_static_filepath(filepath):
    split_filepath = filepath.split('/')
    while len(split_filepath) > 2:
        split_filepath.pop(0)

    return '/'.join(split_filepath)


def copy_file(old, new):
    command_string = "cp " + old + " " + new
    subprocess.check_output(command_string.split(" "))


def make_processable(greyscale_fname, output_color_file):
    ouptut_greyscale_file = INST_FOLDER + "/" + greyscale_fname
    print(output_color_file, ouptut_greyscale_file)

    color_to_grey.convert_rgb_image_to_greyscale(
        output_color_file,
        ouptut_greyscale_file
    )

    copy_file(ouptut_greyscale_file, LABEL_FOLDER + "/" + greyscale_fname)
    copy_file(ouptut_greyscale_file, IMG_FOLDER + "/" + greyscale_fname)


class UploadHandler(web.RequestHandler):
    def post(self, name=None):
        self.application.logger.info("Recieved a file")
        color_fname = "color.png"
        img_data = base64.b64decode(str(self.request.body).split(",")[1])
        output_color_file = STATIC_IMG_FOLDER + "/" + color_fname

        with open(output_color_file, "wb+") as out_f:
            out_f.write(img_data)

        greyscale_fname = "greyscale.png"
        make_processable(greyscale_fname, output_color_file)

        export_image_location = test.run(greyscale_fname)
        print(export_image_location)
        static_image_location = parse_static_filepath(export_image_location)
        print(static_image_location)

        self.write({
            "result": "success",
            "location": "image_location"
        })


class MainHandler(web.RequestHandler):
    def get(self, name=None):
        self.render("index.html")


class MainApplication(web.Application):
    is_closing = False

    def signal_handler(self):
        logging.info('exiting...')
        self.is_closing = True

    def try_exit(self):
        if self.is_closing:
            ioloop.IOLoop.instance().stop()
            logging.info('exit success')

    def __init__(self, **settings):
        web.Application.__init__(self, **settings)

        self.port = settings.get('port', 80)
        self.address = settings.get('address', "0.0.0.0")
        self.ioloop = ioloop.IOLoop.instance()
        self.logger = logging.getLogger()

        self.add_handlers(".*", [
            (r"/", MainHandler),
            (r"/upload", UploadHandler),
        ])

    def run(self):
        try:
            signal.signal(signal.SIGINT, self.signal_handler)
            self.listen(self.port, self.address)
            ioloop.PeriodicCallback(self.try_exit, 100).start()
        except socket.error as e:
            self.logger.fatal("Unable to listen on {}:{} = {}".format(self.address, self.port, e))
            sys.exit(1)
        self.ioloop.start()


if __name__ == "__main__":
    options.define("debug", default=False, help="debug")
    options.define('port', default=80, help='port')
    options.define('address', default="0.0.0.0", help='url')
    options.define('template_path', default=os.path.join(
        os.path.dirname(__file__), "templates"), help='path')
    options.parse_command_line()
    options = options.options.as_dict()

    print("options:", options)

    app = MainApplication(**options)
    app.run()

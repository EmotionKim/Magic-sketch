import os
import sys
import logging
import socket
import signal

from tornado import ioloop, options, web

IMG_FOLDER = os.path.join(os.path.dirname(__file__), "dataset/image")
INST_FOLDER = os.path.join(os.path.dirname(__file__), "dataset/instance")
LABEL_FOLDER = os.path.join(os.path.dirname(__file__), "dataset/label")


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
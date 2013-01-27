import tornado.ioloop
import tornado.web

from handlers.meeting_request_handler import MeetingRequestHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r'/test/([a-zA-Z0-9-]*)', MainHandler),
    (r'/meeting/*([a-zA-Z0-9-]*)', MeetingRequestHandler),
])

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
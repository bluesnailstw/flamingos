from tornado.options import options, define, parse_command_line
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
from manager.wsgi import application
from django.conf import settings
from deploy.notify import NotifyHandler, SaltEventHandler


define('port', type=int, default=80)
define('host', type=str, default='0.0.0.0')


def main():
    parse_command_line()
    wsgi_app = tornado.wsgi.WSGIContainer(application)
    tornado_app = tornado.web.Application(
        [
            (r'/ws', NotifyHandler),
            (r'/events', SaltEventHandler),
            ('/static/rest_framework/(.*)', tornado.web.StaticFileHandler,
             dict(path='/usr/local/lib/python3.7/site-packages/rest_framework/static/rest_framework')),
            ('/static/(.*)', tornado.web.StaticFileHandler,
             dict(path=settings.STATICFILES_DIRS[0])),
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port, address=options.host)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()

"""
@file
@brief Defines a Tornado application.
Tutorial `chat <https://github.com/tornadoweb/tornado/tree/stable/demos/chat>`_.
"""
import os
from tornado.web import Application
from tornado.web import StaticFileHandler
from .handlersml import TemplateHandler


class MainHandler(TemplateHandler):
    """
    Handlers for the main page.
    """

    def __init__(self, application, request, **kwargs):
        """
        Constructor.
        """
        TemplateHandler.__init__(
            self, application, "index.fr.html", request, **kwargs)


class LightMLBoard(Application):
    """
    Overloads a :epkg:`tornado:Application`.
    """

    def __init__(self, handlers=None, default_host=None, transforms=None,
                 **settings):
        """
        Constructor.
        See `wep.py <https://github.com/tornadoweb/tornado/blob/master/tornado/web.py>`_.
        """
        Application.__init__(self, handlers=handlers, default_host=default_host,
                             transforms=transforms, **settings)

    @staticmethod
    def make_app():
        """
        Creates a LightMLBoard application.

        @return     @see cl LightMLBoard
        """
        this = os.path.dirname(__file__)
        st = os.path.join(this, "static")
        return LightMLBoard([
            (r"/", MainHandler),
            (r'/static/(.*)', StaticFileHandler, {'path': st}),
        ])

    @staticmethod
    def start_app(port=8897):
        """
        Starts the application.
        """
        import tornado.ioloop
        app = LightMLBoard.make_app()
        app.listen(port)
        tornado.ioloop.IOLoop.current().start()

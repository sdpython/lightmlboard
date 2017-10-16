"""
@file
@brief Defines handlers for a Tornado application.
"""
from tornado.web import RequestHandler


class TemplateHandler(RequestHandler):
    """
    Defines the main page handler.
    """

    def __init__(self, application, tmpl_name, request, **kwargs):
        """
        Constructor.
        See `web.py <https://github.com/tornadoweb/tornado/blob/master/tornado/web.py>`_.
        """
        RequestHandler.__init__(self, application, request, **kwargs)
        self._tmpl_name = "templates/{0}".format(tmpl_name)
        self._tmpl_context = {'style': 'static/style.css',
                              'icon': 'static/icon.ico',
                              'image': 'static/icon.png'}

    def get(self):
        """
        Returns the content page.
        """
        return self.render(self._tmpl_name, **self._tmpl_context)

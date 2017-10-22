"""
@file
@brief Defines a Tornado application.
Tutorial `chat <https://github.com/tornadoweb/tornado/tree/stable/demos/chat>`_.
"""
import importlib
import logging
import os
import pprint
import sys
from tornado.web import Application
from tornado.web import StaticFileHandler
from tornado.log import enable_pretty_logging
from .handlersml import MainHandler, LoginHandler, LogoutHandler
from .default_options import LightMLBoardDefaultOptions


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
        if "login_url" not in settings:
            settings['login_url'] = "/login"
        if "xsrf_cookies" not in settings:
            settings["xsrf_cookies"] = True

        Application.__init__(self, handlers=handlers, default_host=default_host,
                             transforms=transforms, **settings)
        app_log = logging.getLogger("tornado.application")
        app_log.info('[LightMLBoard] {0}'.format(settings))

    @staticmethod
    def read_options(config):
        """
        Reads configuration from a file or a dictionary.
        """
        config_options = {}
        if config is not None:
            if isinstance(config, dict):
                config_options.update(config)
            elif isinstance(config, str) and os.path.exists(config):
                app_log = logging.getLogger("tornado.application")
                app_log.info("[LightMLBoard] read file '{0}'".format(config))
                obj = None
                fname = os.path.splitext(config)[0]
                path, name = os.path.split(fname)
                if path:
                    sys.path.append(path)
                    mod = importlib.import_module(name)
                    del sys.path[-1]
                else:
                    mod = importlib.import_module(name)
                for k, v in mod.__dict__.items():
                    if isinstance(v, LightMLBoard.__class__):
                        obj = v
                        break
                if obj is None:
                    raise ValueError(
                        "Unable to read configuration '{0}'.".format(config))
                for k, v in obj.__dict__.items():
                    if not k.startswith('_'):
                        config_options[k] = v
            else:
                raise ValueError(
                    "Unable to interpret config\ncwd: '{0}'\n{1}".format(os.getcwd(), config))
        return config_options

    def update_options(config_options):
        """
        Returns updated options, includes the default ones.
        """
        context = {}
        lang = None
        debug = False
        cookie_secret = None
        enablelog = False
        for opts in [LightMLBoardDefaultOptions.__dict__,
                     config_options]:
            for k, v in opts.items():
                if not k.startswith("_"):
                    if k == 'cookie_secret':
                        cookie_secret = v
                    elif k == "lang":
                        lang = v
                    elif k == "debug":
                        debug = debug
                    elif k == "logging":
                        enablelog = v
                    elif k == "allowed_users":
                        context[k] = v
                    else:
                        context["tmpl_" + k] = v
        app_options = dict(lang=lang, debug=debug, enablelog=enablelog,
                           cookie_secret=cookie_secret)
        return context, app_options

    @staticmethod
    def read_users(filename):
        """
        Reads users definition.
        """
        import pandas
        df = pandas.read_csv(filename)
        cols = list(sorted(df.columns))
        df = df[cols]
        exp = "login,mail,pwd,team".split(",")
        has = list(df.columns)
        if exp != has:
            raise ValueError(
                "Users should be defined in CSV file with columns: {0}, not {1}".format(exp, has))
        users = {}
        for i in range(0, df.shape[0]):
            login, mail, pwd, team = df.loc[i, 'login'], df.loc[i,
                                                                'mail'], df.loc[i, 'pwd'], df.loc[i, 'team']
            if login in users:
                raise ValueError("Duplicated user: '{0}'.".format(login))
            users[login] = dict(mail=mail, pwd=pwd, team=team)
        return users

    @staticmethod
    def make_app(config=None, logged=None):
        """
        Creates a LightMLBoard application.

        @param      config      configuration file
        @param      logged      to log one user
        @return                 @see cl LightMLBoard
        """
        this = os.path.dirname(__file__)
        st = os.path.join(this, "static")

        # Update the context for static files.
        updated_context = {}
        updated_context.update({'path': st})

        # Options.
        config_options = LightMLBoard.read_options(config)
        context, local_context = LightMLBoard.update_options(config_options)
        allowed = context["allowed_users"]
        if allowed is None:
            raise ValueError("No allowed users.\n{0}".format(
                pprint.pformat(context)))
        users = LightMLBoard.read_users(allowed)
        del context['allowed_users']

        # Specifies a logged user.
        if logged:
            context["ut_logged"] = logged
            updated_context["ut_logged"] = logged

        context_users = context.copy()
        context_users['users'] = users

        # Logging.
        if local_context['debug'] or local_context['enablelog']:
            enable_pretty_logging()

        pages = [
            (r"/", MainHandler, context),
            (r'/login', LoginHandler, context_users),
            (r'/logout', LogoutHandler, context),
            (r'/static/(.*)', StaticFileHandler, updated_context),
        ]

        args = dict(lang=local_context["lang"], debug=local_context['debug'])
        if 'cookie_secret' in local_context:
            args['cookie_secret'] = local_context['cookie_secret']
        return LightMLBoard(pages, **args)

    @staticmethod
    def start_app(port=8897, **kwargs):
        """
        Starts the application.

        @param      port        port to listen
        @param      kwargs      @see me make_app
        """
        import tornado.ioloop
        app = LightMLBoard.make_app(**kwargs)
        app.listen(port)
        tornado.ioloop.IOLoop.current().start()

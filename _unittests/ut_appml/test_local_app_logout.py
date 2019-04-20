# -*- coding: utf-8 -*-
"""
@brief      test log(time=33s)
"""
import os
import unittest
from tornado.testing import AsyncHTTPTestCase
from pyquickhelper.pycode import get_temp_folder
from lightmlboard.appml import LightMLBoard
from lightmlboard.static import copy_static


class TestLocalAppLogout(AsyncHTTPTestCase):

    def get_app(self):
        this = os.path.dirname(__file__)
        config = os.path.join(this, "this_default_options.py")
        return LightMLBoard.make_app(config=config, logged=dict(user='xd', pwd='pwd'))

    def test_local_logout(self):
        response = self.fetch('/logout')
        self.assertEqual(response.code, 200)
        self.assertIn(b"Python pour un data scientist", response.body)
        temp = get_temp_folder(__file__, "temp_local_logout")
        page = os.path.join(temp, "logout.html")
        with open(page, "wb") as f:
            f.write(response.body)
        copy_static(temp)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""
@brief      test log(time=33s)
"""
import os
import unittest
from tornado.testing import AsyncHTTPTestCase
from lightmlboard.appml import LightMLBoard


class TestLocalApp(AsyncHTTPTestCase):

    def get_app(self):
        this = os.path.dirname(__file__)
        config = os.path.join(this, "this_default_options.py")
        return LightMLBoard.make_app(config=config)

    def test_local_login(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertIn(b"LightMLBoard", response.body)


if __name__ == "__main__":
    unittest.main()

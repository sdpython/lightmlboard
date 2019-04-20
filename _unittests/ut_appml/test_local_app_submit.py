# -*- coding: utf-8 -*-
"""
@brief      test log(time=33s)
"""
import os
import unittest
from tornado.testing import AsyncHTTPTestCase
from lightmlboard.appml import LightMLBoard


class TestLocalAppSubmit(AsyncHTTPTestCase):

    def get_app(self):
        this = os.path.dirname(__file__)
        config = os.path.join(this, "this_default_options.py")
        return LightMLBoard.make_app(config=config, logged=dict(user='xd', pwd='pwd'))

    def test_local_submit(self):
        response = self.fetch('/submit?cpt_value=0')
        self.assertEqual(response.code, 200)
        self.assertIn(b"<h2>Upload</h2>", response.body)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import unittest
import tornado
from tornado.testing import AsyncTestCase
from tornado.httpclient import AsyncHTTPClient


class TestHttp(AsyncTestCase):

    @tornado.testing.gen_test
    def test_http_fetch(self):
        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch("http://www.xavierdupre.fr")
        self.assertIn(b"Xavier", response.body)


if __name__ == "__main__":
    unittest.main()

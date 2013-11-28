#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from zina_uploader import ZinaClient
import json
import os

LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))


class TestZinaUploader (unittest.TestCase):

    def setUp(self):
        self.nfe_id = 150

    def test_zina_url_add_http(self):
        uz = ZinaClient(upload_file=None,
                        zina_id=self.nfe_id,
                        zina_url='www.test.com',
                        config_file=os.path.join(LOCAL_PATH, 'flowbot.json'))
        self.assertTrue(uz.zina_url, 'http://www.test.com')

    def test_zina_url_no_add_http(self):
        uz = ZinaClient(upload_file=None,
                        zina_id=self.nfe_id,
                        zina_url='http://www.test.com',
                        config_file=os.path.join(LOCAL_PATH, 'flowbot.json'))
        self.assertTrue(uz.zina_url, 'http://www.test.com')

    def test_config_file_raise_error(self):
        self.assertRaises(ValueError, lambda: ZinaClient(upload_file=None,
                                                zina_id=self.nfe_id,
                                                zina_url='http://www.test.com',
                                                config_file=''))

    def test_if_check_value_is_valid(self):
        "Test check value need have Django Piston API runserver"
        uz = ZinaClient(upload_file=None,
                        zina_id=self.nfe_id,
                        zina_url='127.0.0.1:8000/nfe/api/',
                        config_file=os.path.join(LOCAL_PATH, 'flowbot.json'))

        json_info = uz.get_nfe()
        self.assertTrue(json.loads(json_info), json_info)

    def test_upload_file(self):
        "Test upload need have Django Piston API runserver"
        uz = ZinaClient(upload_file=os.path.join(LOCAL_PATH, 'flowbot.json'),
                        zina_id=self.nfe_id,
                        zina_url='127.0.0.1:8000/nfe/api/',
                        config_file=os.path.join(LOCAL_PATH, 'flowbot.json'))

        json_info = uz.send_file()
        self.assertEqual(json_info, 'SUCCESS')

    def test_invalid_register(self):
        uz = ZinaClient(upload_file=os.path.join(LOCAL_PATH, 'flowbot.json'),
                        zina_id=999999,
                        zina_url='127.0.0.1:8000/nfe/api/',
                        config_file=os.path.join(LOCAL_PATH, 'flowbot.json'))

        json_info = uz.send_file()
        self.assertEqual(json_info, 'ERROR: NFe matching query does not exist.')

    def test_invalid_url_value(self):
        uz = ZinaClient(upload_file=os.path.join(LOCAL_PATH, 'flowbot.json'),
                        zina_id=self.nfe_id,
                        zina_url='127.0.0.1:8000/nfe/api123123123/',
                        config_file=os.path.join(LOCAL_PATH, 'flowbot.json'))

        json_info = uz.send_file()
        self.assertEqual(json_info, 'ERROR: HTTP Error 500: INTERNAL SERVER ERROR')

    def test_invalid_register_url(self):
        uz = ZinaClient(upload_file=os.path.join(LOCAL_PATH, 'flowbot.json'),
                        zina_id=self.nfe_id,
                        zina_url='127.0.0.1:8000/nfe/api/23123123',
                        config_file=os.path.join(LOCAL_PATH, 'flowbot.json'))

        json_info = uz.send_file()
        self.assertEqual(json_info, 'ERROR: HTTP Error 500: INTERNAL SERVER ERROR')

    def test_invalid_zina_url_send_file(self):
        uz = ZinaClient(upload_file=os.path.join(LOCAL_PATH, 'flowbot.json'),
                        zina_id=self.nfe_id,
                        zina_url='http://www.terra.com.br/',
                        config_file=os.path.join(LOCAL_PATH, 'flowbot.json'))

        json_info = uz.send_file()
        self.assertTrue('ERROR' in json_info)

    def test_invalid_zina_url_get_register(self):
        uz = ZinaClient(upload_file=None,
                        zina_id=self.nfe_id,
                        zina_url='http://www.terra.com.br/',
                        config_file=os.path.join(LOCAL_PATH, 'flowbot.json'))

        json_info = uz.get_nfe()
        self.assertTrue('ERROR' in json_info)

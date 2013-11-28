# -*- coding: utf-8 -*-
import os
import sys
import urllib2
import MultipartPostHandler
import base64
import ConfigParser


def http_auth(username, password):
    credentials = base64.encodestring('%s:%s' % (username, password)).strip().replace('\n', '')
    auth_string = 'Basic %s' % credentials
    return auth_string


class ZinaClient(object):
    """
    USAGE EXAMPLE
    -------------

    CHECK CONNECTION:
    zina_uploader 0 http://zinasite.com/api/'

    SEND FILE:
    zina_uploader file.zip 1 http://zinasite.com/api/'

    CHECK ONE REGISTER:
    zina_upload 1 http://zinasite.com/api/

    USER/PASSWORD:
    Save user information on flowbot.ini in same diretory

    """
    __version__ = "0.6.6"
    __auth__ = 'Valder Gallo <valdergallo@gmail.com>'
    _zina_url = None

    def __init__(self, upload_file, zina_id, zina_url, config_file='flowbot.ini'):
        self.upload_file = upload_file
        self.zina_url = zina_url
        self.zina_id = (zina_id > 0) and zina_id or 0
        self.config_file = config_file

        if not os.path.exists(self.config_file):
            raise ValueError('ERROR: Config file error - %s' % self.config_file)

        config = ConfigParser.RawConfigParser()
        config.read(self.config_file)
        self.flowbot = config

        upload_suport = MultipartPostHandler.MultipartPostHandler

        if self.flowbot.has_option('config', 'proxy'):
            proxy_support = urllib2.ProxyHandler(self.flowbot.get('config', 'proxy'))
        else:
            proxy_support = urllib2.ProxyHandler({})

        self.opener = urllib2.build_opener(proxy_support,
                                           upload_suport)

        urllib2.install_opener(self.opener)

    @property
    def zina_url(self):
        return self._zina_url

    @zina_url.setter
    def zina_url(self, value):
        if 'http://' not in value:
            self._zina_url = 'http://' + value
        else:
            self._zina_url = value

    def open(self, request_url, params=None):
        if params:
            request = urllib2.Request(request_url, params)
        else:
            request = urllib2.Request(request_url)

        request.add_header('Authorization', http_auth(self.flowbot.get('user', 'username'),
                            self.flowbot.get('user', 'password')))

        try:
            response = urllib2.urlopen(request)
            response = response.read()
            if not '<body' in response:
                return response
            else:
                raise ValueError('INTERNAL SERVER ERROR')
        except ValueError, e:
            return u'ERROR: 500 %s' % e
        except urllib2.HTTPError, e:
            return urllib2.HTTPError(u'ERROR: %s' % e)
        except urllib2.URLError, e:
            return urllib2.URLError(u'ERROR: %s' % e)

    def get_nfe(self):
        if self.flowbot.get('config', 'debug'):
            print 'Checking...', ('FILE: %s' % self.upload_file, 'ZINA_ID: %s' % self.zina_id, 'URL: %s' % self.zina_url)

        if self.zina_id:
            zina_url = self.zina_url + str(self.zina_id)
        else:
            zina_url = self.zina_url
        try:
            response = self.open(zina_url)
        except urllib2.URLError, e:
            return urllib2.URLError("ERROR: ", e)
        except urllib2.URLError, e:
            return urllib2.URLError("ERROR: ", e)

        return response

    def send_file(self):
        if self.flowbot.get('config', 'debug'):
            print 'Sending...', ('FILE: %s' % self.upload_file, 'ZINA_ID: %s' % self.zina_id, 'URL: %s' % self.zina_url)
        abs_path = os.path.abspath(self.upload_file)
        if not os.path.exists(abs_path):
            return ImportError('ERROR: Invalid File - %s' % abs_path)

        params = {
            'zipfile': open(self.upload_file, 'rb'),
            'id': str(self.zina_id),
        }

        response = self.open(self.zina_url, params)
        return response

if __name__ == '__main__':
    sys_args = dict(enumerate(sys.argv))
    upload_file = None

    if not sys_args.get(1):
        print "    Version: " , ZinaClient.__version__
        print "    Created by: " , ZinaClient.__auth__
        print ZinaClient.__doc__
    else:
        try:
            zina_id = int(sys_args.get(1))
            zina_url = sys_args.get(2)
        except ValueError:
            upload_file = sys_args.get(1)
            zina_id = int(sys_args.get(2))
            zina_url = sys_args.get(3)

        if not upload_file:
            cl = ZinaClient(upload_file=None, zina_id=zina_id, zina_url=zina_url)
            print cl.get_nfe()
        elif upload_file:
            cl = ZinaClient(upload_file=upload_file, zina_id=zina_id, zina_url=zina_url)
            print cl.send_file()

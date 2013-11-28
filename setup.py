""" Setup to create zina_uploader.exe
"""
from distutils.core import setup
import py2exe
import sys
from zina_uploader.zina_uploader import ZinaClient

sys.argv.append('py2exe')

install_requires = [
    'MultipartPostHandler',
    'grennlet',
    'eventlet',
]

setup(
    name='Zina Uploader',
    version=ZinaClient.__version__,
    author=ZinaClient.__auth__,
    description='ZINA Flowbot uploader',
    console=['zina_uploader/zina_uploader.py'],
    packages=['zina_uploader'],
    py_modules=['zina_uploader'],
    data_files=['zina_uploader/flowbot.ini'],
    bundle_files=1,
    optimize=2,
    zipfile=None,
    install_requires=install_requires,
    test_suite='zina_uploader.runtests',
)

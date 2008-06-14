import ez_setup
ez_setup.use_setuptools()
from setuptools import setup

setup(
    name='phpserialize',
    author='Armin Ronacher',
    author_email='armin.ronacher@active-4.com',
    version='1.1',
    url='http://dev.pocoo.org/hg/phpserialize-main',
    py_modules=['phpserialize'],
    description='a port of the serialize and unserialize '
                'functions of php to python.',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: PHP',
        'Programming Language :: Python'
    ]
)

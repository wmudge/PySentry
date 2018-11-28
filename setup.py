from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pysentry',
    version='1.0.0.dev1',
    description='Python wrapper for the Sentry Thrift specs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Webster Mudge',
    author_email='wmudge@cloudera.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries'
        'License :: OSI Approved :: Apache Software License'
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    keywords='apache sentry hadoop security governance',
    packages=find_packages(),
    install_requires=['thrift', 'sasl', 'thrift_sasl'],

)

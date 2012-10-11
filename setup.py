#!/usr/bin/env python

from setuptools import setup

setup(
      name='Wordcount',
      version='1.0',
      description='Wordcount client side application',
      author=['Rickert Mulder', 'Rainer Dreyer'],
      author_email=['circlingthesun@gmail.com', 'rdrey1@gmail.com'],
      url='http://www.circlngthesun.co.za',
      packages=['wclient', 'wserver'],
      install_requires=[
        'pySide',
        'python-dateutil',
        'flask',
        'fabric',
        #'python-ntlm',
      ],
)

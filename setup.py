# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from django_clement import VERSION
 
setup(
    name='django_clement',
    version=VERSION,
    description='Collection of django helpers',
    author='Clément Nodet',
    author_email='clement.nodet@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)

#!/usr/bin/env python

# from distutils.core import setup, Extension
from setuptools import setup, Extension

#Copied from wheel package


long_desc = "".join(open("README.md").readlines())


setup(
    name='delaunayextrapolation',
    version='0.1',
    description='Delaunay Extrapolation.',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
    ],
    author='Masakazu Matsumoto',
    author_email='vitroid@gmail.com',
    url='https://github.com/vitroid/delaunayextrapolation/',
    keywords=['Delaunay', 'extrapolation', 'scatter'],

    install_requires=['scipy', ],
    py_modules=['delaunayextrapolation'],
    license='MIT',
)

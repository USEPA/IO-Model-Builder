import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="openio",
    version="0.0.1",
    author="Michael Srocka",
    author_email="michael.srocka@greendelta.com",
    description="openio is a library for creating input-output models",
    license="MIT",
    keywords="example documentation tutorial",
    url="http://packages.python.org/openio",
    packages=['openio'],
    install_requires=['numpy', 'pandas', 'matplotlib'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ]
)

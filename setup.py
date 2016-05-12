import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="iomb",
    version="0.0.1",
    author="msrocka",
    author_email="michael.srocka@greendelta.com",
    description="iomb is a package for creating environmentally extended input-output models",
    license="MIT",
    keywords="example documentation tutorial",
    url="http://packages.python.org/iomb",
    packages=['iomb'],
    install_requires=['numpy', 'pandas', 'matplotlib'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ]
)

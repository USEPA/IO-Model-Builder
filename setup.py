from setuptools import setup

setup(
    name="iomb",
    version="0.0.1",
    author="msrocka",
    author_email="michael.srocka@greendelta.com",
    description="iomb is a package for creating environmentally extended input-output models",
    license="MIT",
    keywords="converter lca",
    url="http://packages.python.org/iomb",
    packages=['iomb'],
    install_requires=['numpy', 'pandas', 'matplotlib'],
    long_description=open('README.md').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Topic :: Utilities",
    ]
)

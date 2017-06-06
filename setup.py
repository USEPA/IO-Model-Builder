from setuptools import setup

setup(
    name="iomb",
    version="1.0",
    author="msrocka",
    author_email="michael.srocka@greendelta.com",
    description="iomb is a package for creating environmentally extended "
                "input-output models",
    license="CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
    keywords="converter lca",
    url="http://packages.python.org/iomb",
    packages=['iomb'],
    package_data={'iomb': ["data/*.*"]},
    install_requires=['numpy', 'pandas', 'matplotlib', 'flask'],
    long_description=open('README.md').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Programming Language :: Python :: 3.5",
        "Topic :: Utilities",
    ]
)

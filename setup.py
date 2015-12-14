# -*- coding: utf-8 -*-
__author__ = 'idbord'
from setuptools import setup

setup(
    name='tsl',
    version="1.0.6",
    keywords=('tsl', 'translate', 'baidu', 'dict', 'baidu api'),
    description="tsl is ready. It is for translation work on linux platform and it can autoly translate words or article between Chinese and English. Also, it provides Baike category for extended need.",
    license='MIT',
    author='idbord',
    author_email='byzone482@gmail.com',
    url="https://github.com/idbord/trans",
    packages=[
        'trans'
    ],
    install_requires=[
        'requests>=2.2.1'
    ],
    platforms="linux",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        "Operating System :: POSIX :: Linux"
    ],
    entry_points={
        'console_scripts': [
            'tsl=trans.Trans:run'
        ]
    }
)

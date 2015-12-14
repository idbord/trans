# -*- coding: utf-8 -*-
__author__ = 'idbord'
from setuptools import setup

setup(
    name='tsl',
    version="0.0.1",
    keywords=('tsl', 'translate', 'baidu', 'dict', 'baidu api'),
    description="适用于在linux终端通过百度api查询单词或者翻译词句",
    license='MIT',
    author='idbord',
    author_email='byzone482@gmail.com',
    url="https://github.com/idbord/trans",
    packages=[
        'trans'
    ],
    install_requires=[

    ],
    platforms="linux",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        "Operating System :: POSIX :: Linux"
    ],
    entry_points={
        'console_scripts': [
            'tsl=trans.Trans:run'
        ]
    }
)

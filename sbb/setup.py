from setuptools import setup

setup(
    name='train',
    py_modules=['sbb'],
    install_requires=['requests', 'docopt', 'prettytable', 'datetime','bs4','logging'],
    entry_points={
        'console_scripts': ['train=sbb:cli']
    }
)
from setuptools import setup

setup(
    name = 'services',
    version = '0.0.1',
    description = 'microservices extension for flask',
    py_modules = [
        'services',
    ],
    install_requires = [
        'requests'
    ]
)

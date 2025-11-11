from setuptools import setup

requires = [
    'pyramid',
    'pyramid_jinja2',
    'deform',
    'colander',
]

setup(
    name='tutorial',
    install_requires=requires,
)

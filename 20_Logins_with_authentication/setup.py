from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the SetuptoolsDevelop egg_info writer
requires = [
    'pyramid',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid_deform',
    'waitress',
    'sqlalchemy',
    'zope.sqlalchemy',
    'bcrypt',
    'pyramid_bcrypt',
]

setup(
    name='tutorial',
    install_requires=requires,
)

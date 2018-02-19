"""Setup script for django_use_email_as_username."""
import os
import re

from setuptools import setup


def get_version(*file_paths):
    """Retrieve the version from given file."""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version('django_use_email_as_username', '__init__.py')

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-use-email-as-username',
    version=version,
    description="""A Django app to use email as username for user authentication.""",
    long_description=readme + '\n\n' + history,
    author='Federico Jaramillo Martínez',
    author_email='federicojaramillom@gmail.com',
    url='https://github.com/jmfederico/django-use-email-as-username',
    packages=[
        'django_use_email_as_username',
    ],
    include_package_data=True,
    install_requires=['django>=1.11'],
    license="BSD License",
    zip_safe=False,
    keywords='django-use-email-as-username',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

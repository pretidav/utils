import mycatalog
from setuptools import setup, find_packages

NAME = 'catalog'
VERSION = '8.0.1' 


setup(
    name=NAME,
    version=VERSION,
    description='Catalog',
    author='David Preti',
    packages=find_packages(include=['mycatalog', 'mycatalog.*']),
    python_requires='>=3.6',
    include_package_data=True,
    package_data={'': ['folder1/*','folder2/*']})

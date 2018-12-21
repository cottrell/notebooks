from setuptools import setup

setup(name='extractors',
      version='0.1',
      description='extracting data',
      install_requires=['ratelimit'],
      packages=['extractors', 'quandl'],
      zip_safe=False)

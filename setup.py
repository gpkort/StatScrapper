from setuptools import setup

setup(name='prostatscrapper',
      version='0.1',
      description='Package to download NFL stats',
      url='http://github.com/gpkort/statscraper',
      author='Greg Korthuis',
      author_email='gpkort@gmail.com',
      license='Apache 2.0 License',
      packages=['prostatscrapper'],
      zip_safe=False, install_requires=['requests', 'bs4', 'pandas'])

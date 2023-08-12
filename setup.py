from setuptools import setup, find_namespace_packages

setup(name='ContactBook',
      version='1.0',
      description='bot assistant',
      url='https://github.com/Laplas00/ContactBook',
      author='Bogdan Gaidarzhy, Mykola Prystash, Vasiliy Hlushchenko, Daniil Zubov',
      author_email='msprystash@gmail.com, Gluschenkov88@gmail.com, danielzubov12@gmail.com, 20helllucifer02@gmail.com',
      license='MIT',
      include_package_data=True,
      packages=find_namespace_packages(),
      entry_points={'console_scripts': [
          'bot = ContactBook.main:main']},
      )

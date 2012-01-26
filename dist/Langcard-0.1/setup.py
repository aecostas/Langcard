from distutils.core import setup
setup(name='Langcard',
      version='0.1',
      description='Custom languages cards ',
      author='Andres Estevez-Costas',
      author_email='aecostas@gmail.com',
      packages=['langcard'],
      package_dir={'langcard': 'src/langcard'},
#      package_data={'langcard': ['js/*.js','db/*','css/*']},
      package_data={'langcard': ['js/*.js']},
      )

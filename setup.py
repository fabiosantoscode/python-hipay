from distutils.core import setup
setup(name='hipay',
      version='1.0',
      description='MAPI implementation for hipay secure online payment',
      author='Ousmane Wilane',
      author_email='ousmane@wilane.org',
      url='https://github.com/cyrilb/python-hipay',
      py_modules=['hipay'],
      data_files=[('share/hipay', ['mapi.xsd']),],
      )

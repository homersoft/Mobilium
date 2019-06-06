from setuptools import setup, find_packages

setup(name='mobilium-server',
      version='0.0.1',
      description='Mobilium Server',
      url='https://github.com/homersoft/Mobilium',
      license='MIT',
      packages=find_packages(),
      tests_require=[
          'pytest'
      ],
      install_requires=[
          'python-socketio == 4.0.3',
          'aiohttp == 3.5.4',
          'websockets == 7.0'
      ])

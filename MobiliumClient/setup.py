from setuptools import setup, find_packages

setup(name='mobilium-client',
      version='0.0.1',
      description='Mobilium Client',
      url='https://github.com/homersoft/Mobilium',
      license='MIT',
      packages=find_packages(),
      setup_requires=[
          'pytest-runner'
      ],
      tests_require=[
          'pytest'
      ],
      install_requires=[
          'python-socketio[client] == 4.0.3',
          'aiohttp == 3.5.4',
          'websockets == 7.0',
          'mobilium-proto-messages == 0.0.1'
      ],
      entry_points={
          'console_scripts': [
              'mobilium-client = mobilium_client.client:main'
          ]
      })

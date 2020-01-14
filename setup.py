from setuptools import setup, find_packages
import subprocess


def install_subpackages():
    subpackages = ['MobiliumProtoMessages', 'MobiliumClient', 'MobiliumServer']
    for subpackage in subpackages:
        subprocess.check_call(['pip install ./{}'.format(subpackage)], shell=True)


install_subpackages()
setup(
    name='mobilium',
    version='0.0.1',
    description='Mobilium',
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
        'tornado == 6.0.3',
        'protobuf == 3.9.0',
        'mobilium-proto-messages == 0.0.1',
        'mobilium-client == 0.0.1',
        'mobilium-server == 0.0.1'
    ]
)

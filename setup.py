from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import subprocess


class GenerateProtoMessagesCommand(build_py):

    def run(self):
        build_py.run(self)
        command = "protoc --python_out=./MobiliumProtoMessages/mobilium_proto_messages/proto " \
                  "--proto_path=./proto messages.proto"
        subprocess.check_call([command], shell=True)


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
        'protobuf == 3.9.0'
    ],
    cmdclass={
        'build_py': GenerateProtoMessagesCommand
    }
)

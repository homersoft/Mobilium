from setuptools import setup, find_packages
import subprocess

generate_messages_command = "protoc --python_out=./MobiliumProtoMessages/mobilium_proto_messages/proto " \
                            "--proto_path=./proto messages.proto"
install_requirements_command = 'pip install -r requirements.txt'
subprocess.check_call([generate_messages_command], shell=True)
subprocess.check_call([install_requirements_command], shell=True)

setup(
    name='mobilium',
    version='0.0.1',
    description='Mobilium',
    url='https://github.com/homersoft/Mobilium',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
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

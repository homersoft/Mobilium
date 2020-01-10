from setuptools import setup, find_packages

setup(
    name='mobilium-proto-messages',
    version='0.0.1',
    description='Mobilium Proto Messages',
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
        'protobuf == 3.9.0'
    ]
)

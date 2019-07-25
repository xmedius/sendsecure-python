from setuptools import setup

setup(
    name='sendsecure',
    version='2.0.0',
    description='The sendsecure Python module for XMediusSENDSECURE (SendSecure)',
    long_description='See https://github.com/xmedius/sendsecure-python for more information',
    url='https://github.com/xmedius/sendsecure-python/',
    author='XMedius R&D',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.7'
    ],
    packages=['sendsecure'],
    package_data={'sendsecure': ['cacert.pem']},
)


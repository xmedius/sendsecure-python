from setuptools import setup

setup(
    name='sendsecure',
    version='1.0.0',
    description='The sendsecure Python module for XMediusSENDSECURE (SendSecure)',
    long_description='See https://github.com/xmedius/sendsecure-python for more information',
    url='https://github.com/xmedius/sendsecure-python/',
    author='XMedius R&D',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    packages=['sendsecure'],
    package_data={'sendsecure': ['cacert.pem']},
    install_requires=['pycurl']
)


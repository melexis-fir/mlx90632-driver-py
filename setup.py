from setuptools import setup
import sys
import platform

version='0.0.0'

requires = ['bincopy>=17.8.0',
            'pyftdi>=0.51.2',
            'ctypes-callable>=1.0.0',
            # LinuxPC
            'hid>=1.0.4; platform_machine=="x86_64"',
            # Rasberry Pi
            'RPi.GPIO>=0.7.0 ; platform_machine=="armv7l"',
            'smbus2>=0.3.0; platform_machine=="armv7l"',
            'hid>=1.0.4; platform_machine=="armv7l"',
            # Jetson Nano
            'Jetson.GPIO>=2.0.8 ; platform_machine=="aarch64"',
            'smbus2>=0.3.0; platform_machine=="aarch64"',
            'hid>=1.0.4; platform_machine=="aarch64"',
            ]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mlx90632-driver',
    version=version,
    description='Python library for MLX90632',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License, Version 2.0',
    entry_points = {'console_scripts': ['mlx90632-dump = examples.mlx90632_dump:main']},
    install_requires=requires,
    url = 'https://github.com/melexis-fir/mlx90632-driver-py',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/melexis-fir/mlx90632-driver-py/archive/V'+version+'.tar.gz',
    packages=['mlx90632','mlx90632/pympt','examples'],
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
	'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
)

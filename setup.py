from __future__ import absolute_import, division, print_function

from setuptools import setup, find_packages


setup(
    name='wannier90-utils',
    version='0.1.0',
    description='Wannier90 utility library',
    author='Jamal I. Mustafa',
    author_email='jimustafa@gmail.com',
    license='BSD',
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'numpy',
        'scipy',
    ],
    tests_require=['pytest'],
)

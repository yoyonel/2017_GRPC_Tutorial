# -*- encoding: utf-8 -*-
from distutils.command.build_py import build_py as _build_py
from distutils.command.sdist import sdist as _sdist

import setuptools
from setuptools import find_packages
from setuptools import setup
from setuptools.command.develop import develop as _develop

# Find if user has grpc available
try:
    from grpc_tools import command

    GRPC_INSTALLED = True
except ImportError:
    GRPC_INSTALLED = False


class BuildPackageProtos(setuptools.Command):
    """Command to generate project *_pb2.py modules from proto files."""

    description = 'build grpc protobuf modules'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if GRPC_INSTALLED:
            command.build_package_protos(self.distribution.package_dir[''])
        else:
            raise ModuleNotFoundError("grpcio-tools is needed in order to "
                                      "generate the proto classes")


class BuildPyCommand(_build_py):
    """Custom build command."""

    def run(self):
        self.run_command('build_proto_modules')
        _build_py.run(self)


class DevelopCommand(_develop):
    """Custom develop command."""

    def run(self):
        self.run_command('build_proto_modules')
        _develop.run(self)


class SDistCommand(_sdist):
    """Custom sdist command."""

    def run(self):
        self.run_command('build_proto_modules')
        _sdist.run(self)


setup(
    name='tutorial-grpc-geodatas',
    version='0.1.0',
    license='None',
    description='',
    author=['Lionel ATTY'],
    author_email=['yoyonel@hotmail.com'],
    url='',
    # packages=['tutorial.grpc.geodatas'],
    packages=['tutorial.{}'.format(x) for x in find_packages('src/tutorial')],
    package_dir={'': 'src'},
    package_data={'': ['*.proto']},
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords=[

    ],
    install_requires=[
        "grpcio"
    ],
    cmdclass={
        'sdist': SDistCommand,
        'build_proto_modules': BuildPackageProtos
    },
    entry_points={
        'console_scripts': [
            'search_server = tutorial.grpc.geodatas.search_server:main',
            'search_client = tutorial.grpc.geodatas.search_client:main',
        ]
    },
    # https://github.com/pypa/sample-namespace-packages/issues/6
    zip_safe=False
)

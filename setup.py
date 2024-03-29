from setuptools import setup
import os


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
        s = fp.read()
    return s


def get_version(path):
    with open(path, "r") as fp:
        lines = fp.read()
    for line in lines.split("\n"):
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name='bwsample',
    version=get_version("bwsample/__init__.py"),
    description='Sampling algorithm for best-worst scaling sets.',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url='http://github.com/ulf1/bwsample',
    author='Ulf Hamster',
    author_email='554c46@gmail.com',
    license='Apache License 2.0',
    packages=['bwsample'],
    install_requires=[
        'numpy>=1.21.6,<2',
        'scipy>=1.7.3,<2',
        'scikit-learn>=1,<2'
    ],
    python_requires='>=3.7',
    zip_safe=True
)

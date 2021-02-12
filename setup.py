from setuptools import setup


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_version(path):
    with open(path, "r") as fp:
        lines = fp.read()
    for line in lines.split("\n"):
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(name='bwsample',
      version=get_version("bwsample/__init__.py"),
      description='Sampling algorithm for best-worst scaling sets.',
      # long_description=read('README.md'),
      # long_description_content_type='text/markdown',
      url='http://github.com/ulf1/bwsample',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='Apache License 2.0',
      packages=['bwsample'],
      install_requires=[
          'setuptools>=40.0.0',
          'numpy>=1.19.5',
          'scipy>=1.5.4',
          # 'numba>=0.52.0'
      ],
      python_requires='>=3.6',
      zip_safe=True)

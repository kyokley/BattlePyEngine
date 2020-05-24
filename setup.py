from setuptools import find_packages, setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='BattlePy',
    version='0.3.1',
    description='Battleship AI Engine',
    long_description=readme(),
    packages=find_packages('src', exclude=['tests']),
    package_dir={'': 'src'},
    url='http://github.com/kyokley/BattlePy',
    author='Kevin Yokley',
    author_email='kyokley2@gmail.com',
    license='MIT',
    install_requires=['blessings', 'tabulate'],
    tests_require=['pytest', 'pytest-mock'],
    zip_safe=False,
)

from setuptools import setup, find_packages

setup(
    name="equilibrium",
    version="0.5.0",
    author="Tal Elburg",
    description="Implementation of a Brain-Computer Interface",
    packages=find_packages(),
    install_requires=['click', 'flask'],
    tests_require=['pytest', 'pytest-cov'],
)

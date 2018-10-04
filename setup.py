from setuptools import setup

setup(
    name='tengp',
    version='0.4',
    description='CGP library built for NumPy',
    author='Jaroslav Loebl',
    author_email='jaroslavloebl@gmail.com',
    packages=['tengp'],
    install_requires=[
        'numpy',
        'decorator'
    ]
)

from setuptools import setup

setup(
    name='tengp',
    version='0.3',
    description='CGP library built on NumPy and TensorFlow',
    author='Jaroslav Loebl',
    author_email='jaroslavloebl@gmail.com',
    packages=['tengp'],
    install_requires=[
        'numpy',
        'scipy',
        'sklearn',
#       'tensorflow'
        'deap'
    ]
)

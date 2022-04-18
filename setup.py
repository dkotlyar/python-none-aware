from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='none-aware',
    version='0.0.1',
    author='Dmitry Kotlyar',
    author_email='dm.kotlyar@yandex.ru',
    description='Package provided none-aware wrapper for none-safety object manipulation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dkotlyar/python-none-aware',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

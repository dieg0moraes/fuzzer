import setuptools


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dieg0moraes',
    version='0.1',
    author='Diego Moraes - Gennaro Monneti',
    author_email='dmoraes11cb@gmail.com',
    description='Fuzzig tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dieg0moraes/fuzzer/',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

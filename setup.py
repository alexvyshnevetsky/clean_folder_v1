from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='0.0.1',
    description='This program is used to automatically sort files in a user-defined directory',
    url='https://github.com/alexvyshnevetsky/Sort_program',
    author='Alex Vyshnevetskyi',
    author_email='alexvyshnevetsky@seznam.cz',
    license='MIT',
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['sort_folder = clean_folder.clean:main']}
)
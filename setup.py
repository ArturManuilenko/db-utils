from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='db-utils',
    version='1.4.4',
    description='Python db-utils',
    author='Unic-lab',
    author_email='manuilenkoav@gmail.com',
    url='git@gitlab.neroelectronics.by:unic-lab/libraries/common-python-utils/db-utils.git',
    packages=find_packages(include=['db_utils*']),
    platforms='any',
    package_data={'': ['*.sql'], },
    long_description=long_description,
    classifiers=[
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                "Programming Language :: Python",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
                "Operating System :: OS Independent"
            ],
    include_package_data=True,
    install_requires=[
            "sqlalchemy==1.4.15",
            "flask_sqlalchemy==2.5.1",
            "psycopg2-binary==2.9.1",
            "flask==2.0.0",
            "SQLAlchemy-serializer==1.4.1",
        ]
)
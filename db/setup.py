import setuptools

_about = {}
with open('anfler/db/_about.py') as fp:
    exec(fp.read(), _about)

setuptools.setup(
    name="anfler-db",
    version=_about["__version__"],

    author="Anfler",
    author_email="support@anfler.com",
    description="Helper and utils (logging, configuration)",
    url="https://gitlab.anfler.com.ar:9999/tributosimple/kafka/db.git",

    license="Copyright 2020, Anfler",
    packages=setuptools.find_packages(include=['anfler.db']),
    python_requires='>=3.7',
    install_requires=['pydantic==1.10.14','mysql-connector-python==8.0.22','SQLAlchemy==1.3.22'],
    classifiers=['Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.9'],
    keywords='tools utils logging configuration'
)

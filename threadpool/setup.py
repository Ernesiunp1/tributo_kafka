import setuptools

_about = {}
with open('anfler/mp/_about.py') as fp:
    exec(fp.read(), _about)

setuptools.setup(
    name="anfler-threadpool",
    version=_about["__version__"],
    author="Anfler",
    author_email="support@anfler.com",
    description="Thread Pool Helper",
    url="https://gitlab.anfler.com.ar:9999/tributosimple/kafka/threadpool.git",

    license="Copyright 2020, Anfler",
    packages=setuptools.find_packages(include=['anfler.mp']),
    python_requires='>=3.8',
    install_requires=['psutil==5.7.3'],
    classifiers=['Programming Language :: Python :: 3.8'],
    keywords='tools utils logging configuration'
)


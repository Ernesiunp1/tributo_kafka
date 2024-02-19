import setuptools

_about = {}
with open('app/_about.py') as fp:
    exec(fp.read(), _about)

setuptools.setup(
    name="anfler-tributosimple",
    version=_about["__version__"],
    author="Anfler",
    author_email="support@anfler.com",
    description= _about["__description__"],
    url="https://gitlab.anfler.com.ar:9999/tributosimple/kafka/tributosimple.git",
    packages=setuptools.find_packages(include=['app']),
    license="Copyright 2020, Anfler",
    python_requires='>=3.7',
    install_requires=['anfler-utils>=0.1.0','anfler-kafka>=0.1.0','anfler-db>=0.1.0','anfler-threadpool>=0.1.0'],
    classifiers=['Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.9'],
    keywords='app afip'
)

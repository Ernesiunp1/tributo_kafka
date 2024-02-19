import setuptools

_about = {}
with open('anfler/kafka_wrapper/_about.py') as fp:
    exec(fp.read(), _about)

setuptools.setup(
    name="anfler-kafka",
    version=_about["__version__"],
    author="Anfler",
    author_email="support@anfler.com",
    description="Kafka wrapper",
    url="https://gitlab.anfler.com.ar:9999/tributosimple/kafka/kafka.git",

    license="Copyright 2020, Anfler",
    packages=setuptools.find_packages(include=['anfler.kafka_wrapper']),
    python_requires='>=3.7',
    install_requires=['kafka-python==2.0.2'],
    classifiers=['Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.9'],
    keywords='tools utils logging configuration'
)

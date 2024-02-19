from setuptools import setup, find_packages
from pip._internal.req import parse_requirements

install_req = parse_requirements(filename="requirements.txt", session="hack")

req = [str(x.requirement) for x in install_req]

setup(
    name="anfler_webscrap",
    version="0.1.0",
    author="Anfler",
    author_email="support@anfler.com",
    description="Scrapping",
    url="https://gitlab.anfler.com.ar:9999/tributosimple/pyapi",
    license="Copyright 2020, Anfler",
    py_modules=["servicios_varios"],
    packages=find_packages(exclude=["*.idea", "*.test", "test.*", "test", "driver"],
                           include=["anfler_afip", "anfler_arba", "anfler_agip", "anfler_base",
                                    "exceptions"]),
    python_requires='>=3.8',
    install_requires=req,
    classifiers=['Programming Language :: Python :: 3.9'],
)

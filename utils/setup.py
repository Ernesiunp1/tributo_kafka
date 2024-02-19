import setuptools


_about = {}
with open('anfler/util/_about.py') as fp:
    exec(fp.read(), _about)

setuptools.setup(
    name="anfler-utils",
    version=_about["__version__"],
    author="Anfler",
    author_email="support@anfler.com",
    description="Helper and utils (logging, configuration)",
    url="https://gitlab.anfler.com.ar:9999/tributosimple/kafka/utils.git",

    license="Copyright 2020, Anfler",
    packages=setuptools.find_packages(include=['anfler.util','anfler.util.config','anfler.util.log','anfler.util.msg','anfler.util.jwt']),
    python_requires='>=3.7',
    install_requires=['psutil==5.7.3','pyjwt[crypto]==2.0.1'],
    classifiers=['Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.9'],
    keywords='tools utils logging configuration'
)

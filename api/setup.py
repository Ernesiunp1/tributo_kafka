import setuptools

_about = {}
with open('app/anfler/api/_about.py') as fp:
    exec(fp.read(), _about)

setuptools.setup(
    name="anfler-tributosimple-api",
    version=_about["__version__"],
    author="Anfler",
    author_email="support@anfler.com",
    description= _about["__description__"],
    url="https://gitlab.anfler.com.ar:9999/tributosimple/kafka/api.git",
    packages=setuptools.find_packages(include=['app.*']),
    license="Copyright 2020, Anfler",
    python_requires='>=3.7',
    install_requires=['anfler-utils>=0.1.0','anfler-kafka>=0.1.0','anfler-db>=0.1.0',
                      'fastapi==0.63.0',
                      'uvicorn[standard]==0.13.4'],
    classifiers=['Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.9'],
    keywords='app afip'
)

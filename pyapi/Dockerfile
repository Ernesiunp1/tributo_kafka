FROM python:3.8

# install google chrome and mozilla firefox

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN wget http://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/google-chrome-stable_89.0.4389.82-1_amd64.deb
# RUN wget http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_89.0.4389.82-1_amd64.deb
# RUN apt-get install -y google-chrome-stable
RUN apt-get install nano
RUN apt install ssh-askpass
RUN apt-get -y update
RUN dpkg -i google-chrome-stable_89.0.4389.82-1_amd64.deb || apt-get -f install -y
RUN apt-get -y install firefox-esr

# install chromedriver and geckodriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN wget -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz
RUN tar -xvzf geckodriver.tar.gz -C /usr/local/bin

# set display port to avoid crash

ENV DISPLAY=:99

RUN python -m pip install --upgrade pip

RUN mkdir /app

WORKDIR /app

ADD anfler_webscrap-0.1.0-py3-none-any.whl /app
ADD anfler_utils-0.1.0-py3-none-any.whl /app

# install utils and webscrapp
RUN pip install anfler_utils-0.1.0-py3-none-any.whl anfler_webscrap-0.1.0-py3-none-any.whl
RUN rm anfler_webscrap-0.1.0-py3-none-any.whl anfler_utils-0.1.0-py3-none-any.whl

# files to test
ADD etc /app/etc
ADD factory /app/factory
# ADD logging_test.json /app
# ADD msg-afip-ccma.json /app

# change level openssl 2 for 1
RUN sed 's/CipherString = DEFAULT@SECLEVEL=2/CipherString = DEFAULT@SECLEVEL=1/g' /etc/ssl/openssl.cnf > /etc/ssl/openssl2.cnf
RUN rm /etc/ssl/openssl.cnf
RUN mv /etc/ssl/openssl2.cnf /etc/ssl/openssl.cnf


# instalacion de librerias python y de sistema
# necesarias para funcionamiento de opencv y tesseract
# PROCESAMIENTO DE IMAGENES
RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev libgl1-mesa-glx tesseract-ocr
RUN pip install opencv-python pytesseract opencv-python-headless numpy imutils

CMD ["python", "factory.py"]

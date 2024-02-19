FROM python:3.9-slim

# Doc
LABEL maintener="tributo simple - App <support@anfler.com>"


# Some extra packages and/or update
# Included google chrome for scrapping
RUN apt-get update && apt-get install -y  \
    vim  \
    net-tools \
    procps \
    gcc \
    wget \
    gnupg2 \
    curl \
    unzip \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    tesseract-ocr
    
RUN python -m pip install --upgrade pip
RUN pip install opencv-python pytesseract opencv-python-headless numpy imutils

# START ADDED FOR SCRAPPING
# install google chrome and firefox
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# RUN apt-get update && apt-get install -y google-chrome-stable
# RUN wget http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_89.0.4389.82-1_amd64.deb
RUN wget http://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/google-chrome-stable_89.0.4389.82-1_amd64.deb
RUN apt-get -y update
RUN apt-get -y install libgdk-pixbuf2.0-0
RUN dpkg -i google-chrome-stable_89.0.4389.82-1_amd64.deb || apt-get -f install -y
RUN apt-get -y install firefox-esr

# install chromedriver and geckodriver
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && rm /tmp/chromedriver.zip
RUN wget -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz
RUN tar -xvzf geckodriver.tar.gz -C /usr/local/bin


# set display port to avoid crash
ENV DISPLAY=:99

# change level openssl 2 for 1
RUN sed -i.bak  's/CipherString = DEFAULT@SECLEVEL=2/CipherString = DEFAULT@SECLEVEL=1/g' /etc/ssl/openssl.cnf
RUN google-chrome --headless --no-sandbox
# END ADDED FOR SCRAPPING

#
# Build and install python modules
#
ADD utils/ /src/utils/
ADD kafka/ /src/kafka/
ADD threadpool/ /src/threadpool/
ADD db/ /src/db/
ADD pyapi/ /src/pyapi/
ADD tributosimple/ /src/tributosimple/

RUN cd /src/utils && python setup.py bdist_wheel && pip install dist/*whl && pip list anfler | grep anfler
RUN cd /src/kafka && python setup.py bdist_wheel && pip install dist/*whl && pip list anfler | grep anfler
RUN cd /src/threadpool && python setup.py bdist_wheel && pip install dist/*whl && pip list anfler | grep anfler
RUN cd /src/db && python setup.py bdist_wheel && pip install dist/*whl && pip list anfler | grep anfler
RUN cd /src/pyapi && python setup.py bdist_wheel && pip install dist/*whl && pip list anfler | grep anfler
RUN cd /src/tributosimple && python setup.py bdist_wheel && pip install dist/*whl && pip list anfler | grep anfler
RUN rm -rf /src


#
# App
WORKDIR /app

# Scripts (aux) and configuration files
ADD tributosimple/scripts/* /app/scripts/
ADD tributosimple/etc/* /app/etc/
ADD tributosimple/logs /app/logs
ADD pyapi/etc/*.json /app/etc/


# Environment
ENV APP_HOME=/app
ENV APP_LOG=${APP_HOME}/logs

# These variables allows to override sections from /app/etc/config.json
# For example, to override "pool" section:
# 1- Create a file with the definition:
#   jq -r "{pool:.pool}" /app/etc/config.json > pool.json
# 2- Edit definition in pool.json
# 3- Override using POOL_CONFIG when container start
#    -e POOL_CONFIG=`cat pool.json`
#
ENV KAFKA_CONFIG=
ENV DB_CONFIG=
ENV POOL_CONFIG=

# ENV AFIP_CONFIG=
# ENV ARBA_CONFIG=
# ENV AGIP_CONFIG=


#CMD ["python3", "-m","app.tributosimple", "-c", "/app/etc/config.json", "-l", "/app/etc/logging.json"]
RUN chmod 755 /app/scripts/tributosimple.sh
CMD ["/app/scripts/tributosimple.sh", "start", "out"]


FROM python:3.9

ADD https://chromedriver.storage.googleapis.com/97.0.4692.36/chromedriver_linux64.zip /opt/chrome/

RUN apt-get update \
&& apt-get install -y unzip wget libgl1 \
&& wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add \
&& wget http://dl.google.com/linux/deb/pool/main/g/google-chrome-unstable/google-chrome-unstable_97.0.4692.20-1_amd64.deb \
&& apt-get install -y -f ./google-chrome-unstable_97.0.4692.20-1_amd64.deb \
&& cd /opt/chrome/ \
&& unzip chromedriver_linux64.zip \
&& pip install selenium opencv-python Pillow pretty_midi

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/chrome
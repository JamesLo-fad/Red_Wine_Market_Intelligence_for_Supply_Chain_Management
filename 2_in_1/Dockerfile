FROM python:3.9-bullseye
COPY forex_rate.py forex_rate.py
COPY vivino.py vivino.py
COPY my_wrapper_script.sh my_wrapper_script.sh
COPY requirements.txt requirements.txt
#COPY . .
RUN pip install -r requirements.txt
RUN apt-get install -y wget
RUN apt update && apt-get install firefox-esr -y
#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
#
## Install Chrome.
#RUN apt-get update && apt-get -y install google-chrome-stable

CMD bash my_wrapper_script.sh

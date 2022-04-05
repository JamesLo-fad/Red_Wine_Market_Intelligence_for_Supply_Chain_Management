FROM python:3.9-bullseye
COPY forex_rate.py forex_rate.py
COPY requirements.txt requirements.txt
#COPY . .
RUN pip install -r requirements.txt
RUN apt-get install -y wget
RUN apt update && apt-get install firefox-esr -y
CMD ["python3", "forex_rate.py", "run"]

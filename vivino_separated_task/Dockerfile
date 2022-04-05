FROM python:3.9-bullseye
COPY vivino_revise_ver.py vivino_revise_ver.py
COPY requirements.txt requirements.txt
#COPY . .
RUN pip install -r requirements.txt
RUN apt-get install -y wget
RUN apt update && apt-get install firefox-esr -y
CMD ["python3", "vivino_revise_ver.py", "run"]

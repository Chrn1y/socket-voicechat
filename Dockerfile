FROM python

COPY . .

RUN apt-get update -y && apt-get install -y portaudio19-dev
RUN pip install -r requirements.txt

CMD ["python3", "./server.py"]
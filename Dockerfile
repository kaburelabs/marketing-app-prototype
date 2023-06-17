FROM python:3.7

RUN mkdir /application
WORKDIR /application

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY ./ ./
EXPOSE 8050

CMD ["python", "./index.py"]
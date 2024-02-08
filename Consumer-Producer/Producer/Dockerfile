FROM python:3.11

ENV PYTHONBUFFERED=1

WORKDIR /Producer2

COPY . /Producer2/

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8002" ]
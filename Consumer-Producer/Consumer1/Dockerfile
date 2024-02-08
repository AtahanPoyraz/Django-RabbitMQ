FROM python:3.11

ENV PYTHONBUFFERED=1

WORKDIR /Consumer1

COPY . /Consumer1/

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000" ]
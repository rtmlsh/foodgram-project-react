FROM python:3.7-slim

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY ./ /app
CMD ["gunicorn", "foodgram_api.wsgi:application", "--bind", "0.0.0.0:8000" ]
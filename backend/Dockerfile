FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
COPY arial.ttf venv/Lib/site-packages/reportlab/fonts/
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN flask db upgrade
EXPOSE $PORT
CMD gunicorn -w 4 --bind 0.0.0.0:$PORT 'app:create_app()' --reload

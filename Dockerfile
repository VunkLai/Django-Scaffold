FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY server ./server
COPY .env.example /app/server/.env

RUN python server/manage.py migrate

ENTRYPOINT [ "python", "/app/server/manage.py" ]
CMD [ "runserver", "0.0.0.0:8000" ]

EXPOSE 8000

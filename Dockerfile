FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]


# Для запуска введите две команды:
# docker build . --tag fastapi_app
# docker run --name fastapi_app -p 80:80 fastapi_app

FROM python:3.11.2-slim

WORKDIR /app

COPY requeriments.txt requeriments.txt
RUN pip install -r requeriments.txt

COPY . .

CMD ["python", "main.py"]

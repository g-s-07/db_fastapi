FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8010

CMD ["python3", "main.py", "0.0.0.0", "--port", "8010"]

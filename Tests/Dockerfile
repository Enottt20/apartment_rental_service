FROM python:3.11-slim

WORKDIR /src
COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /src

CMD ["python3", "tests_runner.py"]
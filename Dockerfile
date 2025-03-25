FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY /src/app.py /src/database.py ./src/
COPY /results/database.csv /results/fice_table.csv ./results/

EXPOSE 5000

WORKDIR /app/src

CMD ["python", "app.py"]
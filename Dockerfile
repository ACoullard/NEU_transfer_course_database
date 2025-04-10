FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY /src/app.py /src/database.py ./src/
COPY /results/database.csv /results/fice_table.csv ./results/

EXPOSE 8000

WORKDIR /app/src

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0", "app:app"]
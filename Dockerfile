FROM python

WORKDIR /app

COPY . /app/

RUN pip3 install -r requirements.txt --no-cache-dir --upgrade

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

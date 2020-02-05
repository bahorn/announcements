FROM python:3.7.5
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "backend"]

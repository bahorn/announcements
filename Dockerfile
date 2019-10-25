FROM python:3.7.5
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["flask", "run", "-h","0.0.0.0"]
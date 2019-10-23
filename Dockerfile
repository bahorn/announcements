FROM python
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "app.py", "-h", "0.0.0.0"]
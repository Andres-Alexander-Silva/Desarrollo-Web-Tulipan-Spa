FROM python:3.8-alpine3.15
WORKDIR /website-TulipanSpa
COPY requirements.txt /website-TulipanSpa/
RUN pip install -r requirements.txt
COPY . /website-TulipanSpa/
#EXPOSE 5000
#ENTRYPOINT ["./gunicorn.sh"]
#CMD ["python","app.py"]
#CMD ["flask","run","--host","0.0.0.0:5000"]
#CMD ["gunicorn","-w","2","-b",":8000","app.py"]
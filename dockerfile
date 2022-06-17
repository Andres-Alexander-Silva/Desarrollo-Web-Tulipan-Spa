FROM python:3.8-alpine
WORKDIR /website-TulipanSpa
COPY requirements.txt /website-TulipanSpa/
RUN pip install -r requirements.txt
COPY . /website-TulipanSpa/
#EXPOSE 5500
#ENTRYPOINT ["python","app.py"]
CMD ["python","app.py"]
#CMD ["flask","run","--host","0.0.0.0:5000"]
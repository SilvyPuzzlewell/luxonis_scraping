FROM python:3.9.2
WORKDIR app
RUN mkdir -p /app/database
RUN mkdir -p /app/templates
COPY database /app/database
COPY templates /app/templates
ADD requirements.txt /app
ADD web_server.py /app
RUN pip install pip==22.1.2
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "web_server.py"]

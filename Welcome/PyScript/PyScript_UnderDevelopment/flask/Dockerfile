FROM python:3.10

WORKDIR /app
RUN pip3 install flask

ENV FLASK_DEBUG=true
ENV WERKZEUG_DEBUG_PIN=off

CMD ["python3", "app.py"]
FROM python:3-slim
WORKDIR /usr/src/app
COPY notification.reqs.txt amqp.reqs.txt http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r notification.reqs.txt -r amqp.reqs.txt -r http.reqs.txt
COPY ./notification.py ./amqp_setup.py ./invokes.py ./.env ./
CMD [ "python", "./notification.py" ]
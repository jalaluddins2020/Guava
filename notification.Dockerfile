FROM python:3-slim
WORKDIR /usr/src/app
COPY notification.reqs.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r notification.reqs.txt -r amqp.reqs.txt
COPY ./notification.py ./amqp_setup.py ./
CMD [ "python", "./notification.py" ]
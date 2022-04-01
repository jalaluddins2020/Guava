FROM python:3-slim
WORKDIR /usr/src/app
COPY make_payment.reqs.txt ./
RUN python -m pip install --no-cache-dir -r make_payment.reqs.txt
COPY ./make_payment.py ./invokes.py 
CMD [ "python", "./make_payment.py" ]
FROM python:3-slim
WORKDIR /usr/src/app
COPY listing.reqs.txt ./
RUN python -m pip install --no-cache-dir -r listing.reqs.txt
COPY ./listing.py ./
CMD [ "python", "./listing.py" ]
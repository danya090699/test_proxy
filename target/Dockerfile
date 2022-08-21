FROM python:3
WORKDIR /app
RUN pip install aiohttp
COPY ./target.py .
CMD [ "python", "target.py" ]

FROM python:3
WORKDIR /app
RUN pip install aiohttp
COPY ./proxy.py .
COPY ./targets .
CMD [ "python", "proxy.py" ]

FROM python:3.10.1
WORKDIR /
RUN pip install asyncpg==0.25.0
RUN pip install psutil
COPY . .
CMD python main.py

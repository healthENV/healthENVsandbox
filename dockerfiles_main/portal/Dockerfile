FROM tiangolo/uvicorn-gunicorn-starlette:python3.7
RUN apt-get update -y
# for ping
RUN apt-get install -y iputils-ping
# for ifconfigss
RUN apt install net-tools

WORKDIR /
COPY requirements.txt /
RUN pip install -r requirements.txt
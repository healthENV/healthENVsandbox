FROM python:3-onbuild

EXPOSE 8000

# Using ENTRYPOINT gets the python script running as PID 1. Apparently only PID 1 can catch SIGTERM signals on 'Docker stop'
ENTRYPOINT ["python", "server.py"]

# To test this script
# docker build -t slow-stop .
# docker run -it -e STOP_TIMEOUT=10 -p 8000:8000 slow-stop:latest
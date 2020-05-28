FROM python:3.8
RUN pip install flask furl pymongo
COPY ./equilibrium/equilibrium_pb2.py /equilibrium/
COPY ./equilibrium/api/ /equilibrium/api/
COPY ./equilibrium/utils/ /equilibrium/utils/
ARG host="0.0.0.0"
ENV HOST $host
ARG port=5000
ENV PORT $port
ARG database="mongodb://127.0.0.1:27017"
ENV DATABASE $database
CMD python -m equilibrium.api -t run-server -h $HOST -p $PORT -d $DATABASE > /logs/$(date +%Y-%m-%d_%H-%M-%S).log
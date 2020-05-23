FROM python:3.8
RUN pip install bson flask construct protobuf furl pika
COPY equilibrium/equilibrium_pb2.py /equilibrium/
COPY equilibrium/utils/* /equilibrium/utils/
COPY equilibrium/server/* /equilibrium/server/
ARG host="0.0.0.0"
ENV HOST $host
ARG port="8000"
ENV PORT $port
ARG url="rabbitmq://rabbitmq:5672"
ENV URL $url
CMD python -m equilibrium.server -t run-server -h $HOST -p $PORT $URL > /logs/$(date +%Y-%m-%d_%H-%M-%S).log
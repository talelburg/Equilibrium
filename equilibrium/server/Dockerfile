FROM python:3.8
RUN pip install flask protobuf furl pika
COPY ./equilibrium/equilibrium_pb2.py /equilibrium/
COPY ./equilibrium/server/ /equilibrium/server/
COPY ./equilibrium/utils/ /equilibrium/utils/
ARG host="0.0.0.0"
ENV HOST $host
ARG port="8000"
ENV PORT $port
ARG message_queue="rabbitmq://rabbitmq:5672"
ENV MESSAGE_QUEUE $message_queue
CMD python -m equilibrium.server -t run-server -h $HOST -p $PORT -mq $MESSAGE_QUEUE > /logs/$(date +%Y-%m-%d_%H-%M-%S).log
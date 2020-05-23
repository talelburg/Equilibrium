FROM python:3.8
RUN pip install furl pymongo protobuf click pika
COPY ./equilibrium/equilibrium_pb2.py /equilibrium/
COPY ./equilibrium/saver/ /equilibrium/saver/
COPY ./equilibrium/utils/ /equilibrium/utils/
ARG database="mongodb://mongodb:27017"
ENV DATABASE $database
ARG message_queue="rabbitmq://rabbitmq:5672"
ENV MESSAGE_QUEUE $message_queue
CMD python -m equilibrium.saver -t run-saver -d $DATABASE -mq $MESSAGE_QUEUE > /logs/$(date +%Y-%m-%d_%H-%M-%S).log
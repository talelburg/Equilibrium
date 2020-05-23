FROM python:3.8
RUN pip install requests flask protobuf furl pymongo click pika matplotlib pillow
COPY ./equilibrium/equilibrium_pb2.py /equilibrium/
COPY ./equilibrium/parsers/ /equilibrium/parsers/
COPY ./equilibrium/utils/ /equilibrium/utils/
ARG parser_name
ENV PARSER_NAME $parser_name
ARG message_queue="rabbitmq://rabbitmq:5672"
ENV MESSAGE_QUEUE $message_queue
CMD python -m equilibrium.parsers -t run-parser $PARSER_NAME -mq $MESSAGE_QUEUE > /logs/$(date +%Y-%m-%d_%H-%M-%S).log
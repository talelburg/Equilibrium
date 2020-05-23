FROM python:3.8
RUN pip install construct protobuf click furl pika pillow matplotlib
COPY equilibrium/equilibrium_pb2.py /equilibrium/
COPY equilibrium/utils/* /equilibrium/utils/
COPY equilibrium/queue/* /equilibrium/queue/
COPY equilibrium/sample/* /equilibrium/sample/
COPY equilibrium/parsers/* /equilibrium/parsers/
ARG parser_name
ENV PARSER_NAME $parser_name
ARG url="rabbitmq://rabbitmq:5672"
ENV URL $url
CMD python -m equilibrium.parsers -t run-parser $PARSER_NAME $URL > /logs/$(date +%Y-%m-%d_%H-%M-%S).log